"""
Train the heart-attack risk model used by the app.

Reproduces the final model from the notebook / report:
  StandardScaler -> PolynomialFeatures(2) -> StandardScaler
  -> LogisticRegression(class_weight="balanced")
with the decision threshold chosen to maximise F1 on out-of-fold
predictions from the TRAINING set only (no test leakage).

A plain balanced logistic regression is also trained so the app can
explain which factors push an individual's risk up or down.

Usage:
    python train_model.py                 # expects heart_attack.csv next to this file
    python train_model.py path/to/data.csv
"""
import sys
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import (StratifiedKFold, cross_val_predict,
                                     train_test_split)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

HERE = Path(__file__).parent
TARGET = "HeartDiseaseorAttack"
FEATURES = ["HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke",
            "Diabetes", "PhysActivity", "HvyAlcoholConsump", "MentHlth",
            "PhysHlth", "Sex", "Age", "Education", "Income"]


def metrics(y, pred, proba):
    tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
    return {"Accuracy": accuracy_score(y, pred), "Precision": precision_score(y, pred),
            "Recall": recall_score(y, pred), "F1": f1_score(y, pred),
            "ROC AUC": roc_auc_score(y, proba),
            "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}}


def main(csv_path):
    df = pd.read_csv(csv_path).dropna()
    missing = set(FEATURES + [TARGET]) - set(df.columns)
    if missing:
        raise SystemExit(f"CSV is missing columns: {sorted(missing)}")

    X, y = df[FEATURES], df[TARGET].astype(int)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                              random_state=42, stratify=y)

    make_model = lambda: make_pipeline(
        StandardScaler(), PolynomialFeatures(2, include_bias=False), StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced"))

    # Threshold from out-of-fold training predictions (maximise F1)
    print("Tuning threshold on out-of-fold training predictions ...")
    oof = cross_val_predict(make_model(), X_tr, y_tr,
                            cv=StratifiedKFold(5, shuffle=True, random_state=42),
                            method="predict_proba", n_jobs=-1)[:, 1]
    prec, rec, thr = precision_recall_curve(y_tr, oof)
    f1s = 2 * prec[:-1] * rec[:-1] / (prec[:-1] + rec[:-1] + 1e-9)
    threshold = float(thr[f1s.argmax()])
    print(f"  threshold = {threshold:.3f}")

    print("Fitting final model ...")
    model = make_model().fit(X_tr, y_tr)
    p_te = model.predict_proba(X_te)[:, 1]

    # Interpretable companion model (same as 'LogReg (balanced)' in the report)
    explainer = make_pipeline(StandardScaler(),
                              LogisticRegression(max_iter=1000, random_state=42,
                                                 class_weight="balanced")).fit(X_tr, y_tr)

    test_metrics = {
        "Tuned threshold": metrics(y_te, (p_te >= threshold).astype(int), p_te),
        "Screening (0.5)": metrics(y_te, (p_te >= 0.5).astype(int), p_te),
    }

    # Probability -> how this person ranks against the test population
    ref_scores = np.sort(p_te)

    meta = {
        "features": FEATURES,
        "threshold": threshold,
        "base_rate": float(y.mean()),
        "n_rows": int(len(df)), "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "values": {c: sorted(pd.unique(X[c]).tolist()) for c in FEATURES},
        "ranges": {c: [float(X[c].min()), float(X[c].max())] for c in FEATURES},
        "medians": {c: float(X[c].median()) for c in FEATURES},
        "metrics": test_metrics,
        "coefficients": dict(zip(FEATURES, explainer[-1].coef_[0].round(4).tolist())),
    }
    joblib.dump({"model": model, "explainer": explainer, "ref_scores": ref_scores,
                 "meta": meta}, HERE / "model.joblib")

    print(json.dumps({k: {m: (round(v, 3) if isinstance(v, float) else v)
                          for m, v in d.items()} for k, d in test_metrics.items()}, indent=2))
    print(f"Saved {HERE / 'model.joblib'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "heart_attack.csv")

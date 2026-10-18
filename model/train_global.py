import json, sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import *
from sklearn.model_selection import train_test_split, cross_val_predict, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

df = pd.read_csv(sys.argv[1]).dropna()
ALL = [c for c in df.columns if c != "HeartDiseaseorAttack"]
GLOBAL = [c for c in ALL if c not in ("Education", "Income")]
y = df.HeartDiseaseorAttack.astype(int)
mk = lambda: make_pipeline(StandardScaler(), PolynomialFeatures(2, include_bias=False), StandardScaler(),
                           LogisticRegression(max_iter=3000, random_state=42, class_weight="balanced"))
out = {}
for name, F in [("report15", ALL), ("global13", GLOBAL)]:
    Xtr, Xte, ytr, yte = train_test_split(df[F], y, test_size=.2, random_state=42, stratify=y)
    oof = cross_val_predict(mk(), Xtr, ytr, cv=StratifiedKFold(5, shuffle=True, random_state=42), method="predict_proba", n_jobs=-1)[:, 1]
    p, r, t = precision_recall_curve(ytr, oof); f = 2*p[:-1]*r[:-1]/(p[:-1]+r[:-1]+1e-9); th = float(t[f.argmax()])
    m = mk().fit(Xtr, ytr); pt = m.predict_proba(Xte)[:, 1]; pr = (pt >= th).astype(int)
    res = dict(threshold=th, acc=accuracy_score(yte, pr), prec=precision_score(yte, pr), rec=recall_score(yte, pr),
               f1=f1_score(yte, pr), auc=roc_auc_score(yte, pt), rec50=recall_score(yte, pt >= .5),
               prec50=precision_score(yte, pt >= .5), cm=confusion_matrix(yte, pr).ravel().tolist())
    print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()})
    out[name] = (res, m, pt, Xte, F)

res, m, pt, Xte, F = out["global13"]
# Deployment model: refit on all data, same settings and threshold
final = mk().fit(df[F], y)
s1, poly, s2, lr = final.steps[0][1], final.steps[1][1], final.steps[2][1], final.steps[3][1]
pf = final.predict_proba(df[F])[:, 1]
# Linear explainer (contributions)
ex = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")).fit(df[F], y)
model = {
  "features": F, "mean1": s1.mean_.tolist(), "scale1": s1.scale_.tolist(),
  "powers": poly.powers_.tolist(), "mean2": s2.mean_.tolist(), "scale2": s2.scale_.tolist(),
  "coef": lr.coef_[0].tolist(), "intercept": float(lr.intercept_[0]),
  "threshold": res["threshold"], "base_rate": float(y.mean()),
  "quantiles": np.quantile(pf, np.linspace(0, 1, 201)).tolist(),
  "ex_mean": ex[0].mean_.tolist(), "ex_scale": ex[0].scale_.tolist(), "ex_coef": ex[-1].coef_[0].tolist(),
  "metrics": {k: res[k] for k in ["acc", "prec", "rec", "f1", "auc", "rec50", "prec50", "cm"]},
  "n": int(len(df)),
}
json.dump(model, open("model/model_global.json", "w"))
# sample rows for JS parity test
smp = df[F].sample(20, random_state=1); smp["p"] = final.predict_proba(smp)[:, 1]
smp.to_csv("model/parity_sample.csv", index=False)
print("exported; coef count", len(model["coef"]))

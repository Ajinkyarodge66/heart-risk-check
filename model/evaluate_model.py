"""Model evaluation per blueprint section 11: discrimination with bootstrap CIs, calibration,
sensitivity/specificity/PPV/NPV at both operating points, and subgroup performance.
Usage: python model/evaluate_model.py data/heart_attack.csv  -> writes docs/model-evaluation.json"""
import sys, json, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, brier_score_loss, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

df = pd.read_csv(sys.argv[1]).dropna()
F = [c for c in df.columns if c not in ("HeartDiseaseorAttack", "Education", "Income")]
y = df.HeartDiseaseorAttack.astype(int)
Xtr, Xte, ytr, yte = train_test_split(df[F], y, test_size=.2, random_state=42, stratify=y)
m = make_pipeline(StandardScaler(), PolynomialFeatures(2, include_bias=False), StandardScaler(),
                  LogisticRegression(max_iter=3000, random_state=42, class_weight="balanced")).fit(Xtr, ytr)
s = m.predict_proba(Xte)[:, 1]
base = ytr.mean()
odds = s / (1 - s) * base / (1 - base); prob = odds / (1 + odds)   # prior-corrected, as shown in the app
yv = yte.values
rng = np.random.default_rng(0)
def boot(fn, n=1000):
    v = []
    for _ in range(n):
        i = rng.integers(0, len(yv), len(yv))
        if yv[i].min() == yv[i].max(): continue
        v.append(fn(yv[i], s[i], prob[i]))
    return [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)]
def op(th):
    tn, fp, fn, tp = confusion_matrix(yv, s >= th).ravel()
    return dict(threshold=round(th, 3), sensitivity=round(tp/(tp+fn), 4), specificity=round(tn/(tn+fp), 4),
                ppv=round(tp/(tp+fp), 4), npv=round(tn/(tn+fn), 4), flagged_share=round((tp+fp)/len(yv), 4))
thr = json.load(open("model/model_global.json"))["threshold"]
cal = pd.DataFrame({"p": prob, "y": yv}); cal["bin"] = pd.qcut(cal.p, 10, labels=False, duplicates="drop")
calib = cal.groupby("bin").agg(mean_predicted=("p", "mean"), observed=("y", "mean"), n=("y", "size")).round(4).reset_index(drop=True)
X = Xte.reset_index(drop=True)
groups = {"female": X.Sex == 0, "male": X.Sex == 1, "age 18-44": X.Age <= 5, "age 45-64": (X.Age >= 6) & (X.Age <= 9), "age 65+": X.Age >= 10,
          "diabetes": X.Diabetes == 2, "no diabetes": X.Diabetes == 0}
sub = {}
for k, g in groups.items():
    g = g.values
    sub[k] = dict(n=int(g.sum()), prevalence=round(float(yv[g].mean()), 4), auc=round(roc_auc_score(yv[g], s[g]), 4),
                  sensitivity_at_0_5=round(float((s[g] >= .5)[yv[g] == 1].mean()), 4), mean_predicted=round(float(prob[g].mean()), 4))
out = dict(
    model="Balanced logistic regression, degree-2 interactions, 13 features (no income/education)",
    data="BRFSS 2015 subset, n=%d; stratified 80/20 split, random_state=42; test n=%d, prevalence %.4f" % (len(df), len(yv), yv.mean()),
    auc=round(roc_auc_score(yv, s), 4), auc_95ci=boot(lambda a, b, c: roc_auc_score(a, b)),
    brier_prior_corrected=round(brier_score_loss(yv, prob), 4), brier_95ci=boot(lambda a, b, c: brier_score_loss(a, c)),
    calibration_in_the_large=dict(mean_predicted=round(float(prob.mean()), 4), observed=round(float(yv.mean()), 4)),
    calibration_deciles=calib.to_dict(orient="records"),
    operating_points={"screening_0.5": op(0.5), "tuned_f1": op(thr)},
    subgroups=sub)
json.dump(out, open("docs/model-evaluation.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ["auc", "auc_95ci", "brier_prior_corrected", "calibration_in_the_large", "operating_points"]}, indent=1))
print(pd.DataFrame(sub).T)
print(calib)

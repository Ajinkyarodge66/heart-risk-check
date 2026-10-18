"""
Heart Attack Risk Predictor - Streamlit app.

Run:
    pip install -r requirements.txt
    python train_model.py          # once, creates model.joblib from heart_attack.csv
    streamlit run app.py
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

HERE = Path(__file__).parent
MODEL_PATH = HERE / "model.joblib"

st.set_page_config(page_title="Heart Attack Risk Predictor", page_icon="❤️",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
  .block-container {padding-top: 2rem; max-width: 1200px;}
  h1 {font-weight: 700; letter-spacing: -0.02em;}
  .risk-card {border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: .8rem;
              border: 1px solid rgba(128,128,128,.25);}
  .risk-low  {background: rgba(46,160,67,.10);  border-left: 6px solid #2ea043;}
  .risk-mod  {background: rgba(210,153,34,.12); border-left: 6px solid #d29922;}
  .risk-high {background: rgba(218,54,51,.12);  border-left: 6px solid #da3633;}
  .risk-label {font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; opacity: .75;}
  .risk-value {font-size: 2.2rem; font-weight: 700; line-height: 1.15;}
  .muted {opacity: .7; font-size: .9rem;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- labels
AGE = {1: "18–24", 2: "25–29", 3: "30–34", 4: "35–39", 5: "40–44", 6: "45–49",
       7: "50–54", 8: "55–59", 9: "60–64", 10: "65–69", 11: "70–74", 12: "75–79", 13: "80+"}
EDU = {1: "Never attended / kindergarten", 2: "Grades 1–8", 3: "Grades 9–11",
       4: "High-school graduate", 5: "Some college", 6: "College graduate"}
INC = {1: "Under $10k", 2: "$10k–15k", 3: "$15k–20k", 4: "$20k–25k",
       5: "$25k–35k", 6: "$35k–50k", 7: "$50k–75k", 8: "$75k or more"}
PRETTY = {"HighBP": "High blood pressure", "HighChol": "High cholesterol",
          "CholCheck": "Cholesterol check (5 yrs)", "BMI": "BMI", "Smoker": "Smoker (100+ cigarettes)",
          "Stroke": "Previous stroke", "Diabetes": "Diabetes", "PhysActivity": "Physically active",
          "HvyAlcoholConsump": "Heavy alcohol use", "MentHlth": "Poor mental-health days",
          "PhysHlth": "Poor physical-health days", "Sex": "Sex", "Age": "Age",
          "Education": "Education", "Income": "Income"}


@st.cache_resource
def load_bundle():
    return joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


bundle = load_bundle()

st.title("❤️ Heart Attack Risk Predictor")
st.caption("Screening tool built from the balanced logistic-regression model "
           "(interaction features + tuned threshold) in the accompanying report.")

if bundle is None:
    st.error("No trained model found. Put **heart_attack.csv** next to `app.py` and run "
             "`python train_model.py`, then refresh this page.")
    st.stop()

model, explainer, ref_scores, meta = (bundle["model"], bundle["explainer"],
                                      bundle["ref_scores"], bundle["meta"])
FEATURES, THRESH, BASE = meta["features"], meta["threshold"], meta["base_rate"]
diab_vals = meta["values"]["Diabetes"]
DIAB = ({0: "No", 1: "Pre-diabetes", 2: "Diabetes"} if max(diab_vals) >= 2 else {0: "No", 1: "Yes"})


def score(df):
    """Model score (balanced, used for the decision) and prior-corrected probability."""
    s = model.predict_proba(df[FEATURES])[:, 1]
    s = np.clip(s, 1e-6, 1 - 1e-6)
    # Balanced class weights act like a 50/50 prior; shift odds back to the real prevalence
    odds = s / (1 - s) * BASE / (1 - BASE)
    return s, odds / (1 + odds)


def percentile(s):
    return float(np.searchsorted(ref_scores, s) / len(ref_scores) * 100)


def yn(label, key, default=0, help=None):
    return 1 if st.radio(label, ["No", "Yes"], index=default, horizontal=True,
                         key=key, help=help) == "Yes" else 0


tab_pred, tab_batch, tab_model = st.tabs(["🩺 Predict", "📄 Batch predictions", "📊 About the model"])

# ================================================================ PREDICT
with tab_pred:
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        with st.form("inputs"):
            st.subheader("About you")
            c1, c2 = st.columns(2)
            age = c1.selectbox("Age group", list(AGE), index=8, format_func=AGE.get)
            sex = c2.radio("Sex", ["Female", "Male"], horizontal=True)
            c1, c2 = st.columns(2)
            edu = c1.selectbox("Education", list(EDU), index=4, format_func=EDU.get)
            inc = c2.selectbox("Household income", list(INC), index=5, format_func=INC.get)

            st.subheader("Health conditions")
            c1, c2 = st.columns(2)
            with c1:
                hbp = yn("Told you have high blood pressure?", "hbp")
                hch = yn("Told you have high cholesterol?", "hch")
                stroke = yn("Ever had a stroke?", "stroke")
            with c2:
                chk = yn("Cholesterol checked in last 5 years?", "chk", default=1)
                diab = st.radio("Diabetes", list(DIAB), format_func=DIAB.get, horizontal=True)

            bmi_mode = st.radio("BMI", ["Enter BMI", "Calculate from height & weight"],
                                horizontal=True, label_visibility="collapsed")
            if bmi_mode == "Enter BMI":
                bmi = st.slider("Body-mass index (BMI)", 12.0, 60.0, 27.0, 0.5)
            else:
                c1, c2 = st.columns(2)
                h = c1.number_input("Height (cm)", 120.0, 220.0, 170.0, 1.0)
                w = c2.number_input("Weight (kg)", 30.0, 250.0, 75.0, 0.5)
                bmi = round(w / (h / 100) ** 2, 1)
                st.caption(f"Calculated BMI: **{bmi}**")

            st.subheader("Lifestyle")
            c1, c2 = st.columns(2)
            with c1:
                smk = yn("Smoked at least 100 cigarettes in your life?", "smk")
                pa = yn("Physical activity in the past 30 days (outside work)?", "pa", default=1)
            with c2:
                alc = yn("Heavy drinker?", "alc",
                         help="Men: more than 14 drinks/week. Women: more than 7 drinks/week.")
            c1, c2 = st.columns(2)
            ment = c1.slider("Days of poor mental health (last 30)", 0, 30, 0)
            phys = c2.slider("Days of poor physical health (last 30)", 0, 30, 0)

            submitted = st.form_submit_button("Assess my risk", type="primary",
                                              use_container_width=True)

    person = pd.DataFrame([{
        "HighBP": hbp, "HighChol": hch, "CholCheck": chk, "BMI": float(bmi), "Smoker": smk,
        "Stroke": stroke, "Diabetes": diab, "PhysActivity": pa, "HvyAlcoholConsump": alc,
        "MentHlth": ment, "PhysHlth": phys, "Sex": 1 if sex == "Male" else 0, "Age": age,
        "Education": edu, "Income": inc}])[FEATURES]

    with right:
        if not submitted and "last" not in st.session_state:
            st.info("Fill in the form and press **Assess my risk**.")
        else:
            if submitted:
                st.session_state["last"] = person
            person = st.session_state["last"]
            s, prob = score(person)
            s, prob = float(s[0]), float(prob[0])
            pct = percentile(s)
            rel = prob / BASE
            flagged = s >= THRESH

            if flagged:
                cls, band = "risk-high", "High risk — flagged by the model"
            elif s >= 0.5:
                cls, band = "risk-mod", "Elevated risk — above screening cut-off"
            else:
                cls, band = "risk-low", "Lower risk"

            st.markdown(f"""
            <div class="risk-card {cls}">
              <div class="risk-label">{band}</div>
              <div class="risk-value">{prob:.1%}</div>
              <div class="muted">estimated chance of heart disease / heart attack ·
                 {rel:.1f}× the population average ({BASE:.1%}) ·
                 higher than {pct:.0f}% of people in the test set</div>
            </div>""", unsafe_allow_html=True)

            gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=s * 100,
                number={"suffix": "", "valueformat": ".0f"},
                title={"text": "Model risk score (0–100)", "font": {"size": 14}},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#444"},
                       "steps": [{"range": [0, 50], "color": "rgba(46,160,67,.35)"},
                                 {"range": [50, THRESH * 100], "color": "rgba(210,153,34,.40)"},
                                 {"range": [THRESH * 100, 100], "color": "rgba(218,54,51,.45)"}],
                       "threshold": {"line": {"color": "#da3633", "width": 3},
                                     "value": THRESH * 100}}))
            gauge.update_layout(height=230, margin=dict(l=20, r=20, t=50, b=10))
            st.plotly_chart(gauge, use_container_width=True)
            st.caption(f"Red line = tuned decision threshold ({THRESH * 100:.0f}). "
                       "Scores of 50+ are above the model's default screening cut-off.")

            # ---- factor contributions (balanced linear model, standardised features)
            sc, lr = explainer[0], explainer[-1]
            z = (person.values[0] - sc.mean_) / sc.scale_
            contrib = pd.Series(lr.coef_[0] * z, index=[PRETTY[f] for f in FEATURES])
            contrib = contrib[contrib.abs() > 0.02].sort_values()
            if len(contrib):
                st.markdown("**What's driving your result**")
                fig = go.Figure(go.Bar(
                    x=contrib.values, y=contrib.index, orientation="h",
                    marker_color=["#2ea043" if v < 0 else "#da3633" for v in contrib.values]))
                fig.update_layout(height=40 + 26 * len(contrib), margin=dict(l=10, r=10, t=10, b=30),
                                  xaxis_title="← lowers risk   ·   raises risk →")
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Compared with an average respondent. Age, sex and income can't "
                           "be changed but still shift the baseline.")

            # ---- what-if for modifiable factors
            changes = []
            p0 = person.iloc[0]
            if p0.Smoker: changes.append(("Had never smoked", {"Smoker": 0}))
            if not p0.PhysActivity: changes.append(("Became physically active", {"PhysActivity": 1}))
            if p0.BMI > 25: changes.append(("Reached a BMI of 25", {"BMI": 25.0}))
            if p0.HighBP: changes.append(("Blood pressure under control", {"HighBP": 0}))
            if p0.HighChol: changes.append(("Cholesterol under control", {"HighChol": 0}))
            if p0.HvyAlcoholConsump: changes.append(("Stopped heavy drinking", {"HvyAlcoholConsump": 0}))
            if changes:
                st.markdown("**What-if: modifiable factors**")
                rows = []
                for label, upd in changes:
                    alt = person.copy()
                    for k, v in upd.items():
                        alt[k] = v
                    rows.append({"If you…": label, "Estimated risk": float(score(alt)[1][0])})
                allp = person.copy()
                for _, upd in changes:
                    for k, v in upd.items():
                        allp[k] = v
                rows.append({"If you…": "All of the above", "Estimated risk": float(score(allp)[1][0])})
                wf = pd.DataFrame(rows)
                wf["Change"] = wf["Estimated risk"] - prob
                st.dataframe(wf.style.format({"Estimated risk": "{:.1%}", "Change": "{:+.1%}"}),
                             hide_index=True, use_container_width=True)
                st.caption("Associations learned from survey data, not proof that a change "
                           "will cause this reduction.")

    st.warning("**Not a diagnosis.** This model was trained on self-reported survey data and "
               "supports screening only. If you have chest pain, shortness of breath or other "
               "warning signs, call emergency services now. Talk to a doctor about your heart health.",
               icon="⚠️")

# ================================================================ BATCH
with tab_batch:
    st.subheader("Score a CSV of people")
    st.write("Upload a CSV with these columns (same coding as the training data):")
    st.code(", ".join(FEATURES), language=None)
    up = st.file_uploader("CSV file", type="csv")
    if up is not None:
        data = pd.read_csv(up)
        miss = [c for c in FEATURES if c not in data.columns]
        if miss:
            st.error(f"Missing columns: {', '.join(miss)}")
        else:
            data = data.dropna(subset=FEATURES).copy()
            s, prob = score(data)
            data["RiskScore"] = (s * 100).round(1)
            data["EstimatedRisk"] = prob.round(4)
            data["Flagged"] = (s >= THRESH).astype(int)
            c1, c2, c3 = st.columns(3)
            c1.metric("People scored", f"{len(data):,}")
            c2.metric("Flagged high risk", f"{data.Flagged.sum():,}",
                      f"{data.Flagged.mean():.1%}", delta_color="off")
            c3.metric("Mean estimated risk", f"{data.EstimatedRisk.mean():.1%}")
            st.dataframe(data.sort_values("RiskScore", ascending=False),
                         use_container_width=True, height=380)
            st.download_button("Download results", data.to_csv(index=False).encode(),
                               "heart_risk_predictions.csv", "text/csv")

# ================================================================ MODEL
with tab_model:
    st.subheader("Model")
    st.markdown(f"""
- **Pipeline:** StandardScaler → degree-2 polynomial & interaction features → StandardScaler →
  logistic regression with balanced class weights
- **Decision threshold:** {THRESH:.3f}, chosen to maximise F1 on out-of-fold predictions from the
  training set only
- **Data:** {meta['n_rows']:,} respondents ({meta['n_train']:,} train / {meta['n_test']:,} test,
  stratified); {BASE:.2%} had heart disease or a heart attack
- **Estimated risk** re-scales the balanced model's score back to the real {BASE:.1%} prevalence
""")
    rows = {k: {m: v for m, v in d.items() if m != "confusion"} for k, d in meta["metrics"].items()}
    st.markdown("**Test-set performance**")
    st.dataframe(pd.DataFrame(rows).T.style.format("{:.3f}"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        cm = meta["metrics"]["Tuned threshold"]["confusion"]
        fig = go.Figure(go.Heatmap(
            z=[[cm["tn"], cm["fp"]], [cm["fn"], cm["tp"]]],
            x=["Predicted no", "Predicted yes"], y=["Actual no", "Actual yes"],
            text=[[f"{cm['tn']:,}", f"{cm['fp']:,}"], [f"{cm['fn']:,}", f"{cm['tp']:,}"]],
            texttemplate="%{text}", colorscale="Reds", showscale=False))
        fig.update_layout(title="Confusion matrix (tuned threshold)", height=330,
                          yaxis_autorange="reversed", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        coef = pd.Series(meta["coefficients"]).rename(index=PRETTY).sort_values()
        fig = go.Figure(go.Bar(x=coef.values, y=coef.index, orientation="h",
                               marker_color=["#2ea043" if v < 0 else "#da3633" for v in coef.values]))
        fig.update_layout(title="Standardised coefficients (linear model)", height=420,
                          margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

# Model evaluation (blueprint §11)

**Status: research model.** It has not been clinically validated outside the US survey population. The app labels it "Research model".

## Intended use (research)
- **Target:** whether a person reports ever having coronary heart disease or a heart attack (prevalence, **not** a 10-year forecast).
- **Population:** US adults who answered the 2015 BRFSS telephone survey.
- **Intended action:** prompt a conversation with a health professional and a blood-pressure check. It must not be used to decide treatment or to rule out disease.

## Data and method
- BRFSS 2015 subset, n=129988; stratified 80/20 split, random_state=42; test n=25998, prevalence 0.0935
- **Model:** Balanced logistic regression, degree-2 interactions, 13 features (no income/education).
- **Why no income or education:** both are coded in US-specific bands, so they were dropped for worldwide use. AUC fell only from 0.836 to 0.832.
- **Class balance:** weighted ("balanced"). The app turns scores back into real-world probabilities using the training prevalence of 9.35%.
- **Leakage controls:** the threshold was tuned on out-of-fold training predictions only, and the scalers were fitted on the training data only.
- **Reproduce:** `python model/evaluate_model.py data/heart_attack.csv`

## Discrimination
| Metric | Value | 95% CI (1,000 bootstraps) |
| --- | --- | --- |
| ROC AUC | 0.832 | 0.825 to 0.840 |
| Brier score (calibrated probability) | 0.0717 | 0.0693 to 0.0740 |

## Operating points (test set)
| Mode | Threshold | Sensitivity | Specificity | PPV | NPV | Share flagged |
| --- | --- | --- | --- | --- | --- | --- |
| Screening | 0.50 | 80.3% | 71.4% | 22.5% | 97.2% | 33.4% |
| Balanced (F1-tuned) | 0.705 | 54.3% | 88.0% | 31.9% | 94.9% | 15.9% |

**How to read the PPV:** at the screening threshold, about 1 in 4 people the model flags actually report heart disease. That is acceptable for a prompt to get checked, and not acceptable for a diagnosis.

## Calibration ("X in 100" shown to users)
Calibration-in-the-large: mean predicted 9.40% vs observed 9.35%.

| Decile | Mean predicted | Observed | n |
| --- | --- | --- | --- |
| 1 | 0.2% | 0.3% | 2,601 |
| 2 | 0.6% | 0.8% | 2,599 |
| 3 | 1.2% | 1.4% | 2,604 |
| 4 | 2.1% | 2.0% | 2,595 |
| 5 | 3.4% | 3.2% | 2,600 |
| 6 | 5.5% | 5.1% | 2,602 |
| 7 | 8.7% | 9.0% | 2,597 |
| 8 | 13.5% | 14.2% | 2,600 |
| 9 | 20.8% | 20.9% | 2,600 |
| 10 | 38.0% | 36.5% | 2,600 |

**Finding:** the calibrated probabilities match observed rates closely in every decile, so the "X in 100" wording is supported *within this population*.

## Subgroup performance
| Subgroup | n | Prevalence | AUC | Sensitivity at 0.5 | Mean predicted |
| --- | --- | --- | --- | --- | --- |
| female | 14,679 | 7.0% | 0.833 | 74% | 7.1% |
| male | 11,319 | 12.3% | 0.816 | 85% | 12.4% |
| age 18-44 | 5,463 | 1.5% | 0.816 | 28% | 1.4% |
| age 45-64 | 11,287 | 7.0% | 0.818 | 68% | 6.9% |
| age 65+ | 9,248 | 16.9% | 0.748 | 89% | 17.2% |
| diabetes | 3,565 | 22.7% | 0.727 | 95% | 22.4% |
| no diabetes | 21,954 | 7.1% | 0.830 | 72% | 7.2% |

### Findings and mitigations
1. **People under 45:** sensitivity is only about 28%. A low result could falsely reassure a young person. **Mitigation in the app:** results for ages 18–44 show a warning that a low result does not mean no risk.
2. **People aged 65+ and people with diabetes:** AUC is lower (about 0.73–0.75), because these groups' risk is high across the board and the model separates them less well. Most of them are flagged anyway.
3. **Women vs men:** AUC is similar. Sensitivity is lower in women at the same threshold because heart disease is less common in women in this data.

## Known limitations
- **Self-reported survey data,** from one country (US) and one year (2015). External validation on the intended users (for example in India or Kenya) is required before any clinical claim.
- **Measures having heart disease now,** not future risk.
- **Missing clinical inputs:** no blood pressure values, cholesterol values or ECG. Answers like "Not sure" are handled by averaging over the population rate.
- **Harms to monitor:** false reassurance (false negatives), anxiety (false positives), and over-reliance on the number.

## Release status
Research preview. Moving to a medical claim needs the regulatory gate in `release-gates.md`.

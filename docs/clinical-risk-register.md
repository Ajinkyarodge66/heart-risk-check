# Clinical risk register / hazard log (blueprint §13, ISO 14971 style)

Severity (S) and likelihood (L) are each scored 1–5. Risk = S×L. **These scores need sign-off by a qualified clinical safety officer.**

| ID | Hazard | Cause | S | L | Risk | Controls in the app | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | False reassurance: someone with heart disease gets a low score | Model sensitivity is about 28% under age 45 and 54–80% overall | 5 | 3 | 15 | "Research model" label; under-45 warning; "a low result does not mean no risk" in onboarding and results; symptoms checker independent of the score | 10: needs external validation |
| H2 | Delayed emergency care | User relies on the app instead of calling | 5 | 2 | 10 | SOS on every screen and the lock screen; red-flag checker puts "call now" first; AI rules put emergencies first | 5 |
| H3 | Over-escalation and anxiety | Asymptomatic BP over 180/120 sent to emergency services | 3 | 3 | 9 | Updated to the AHA 2025 wording: without symptoms → doctor today; with symptoms → emergency | 3 |
| H4 | Wrong BP value recorded | Photo misread or typing error | 3 | 3 | 9 | Photo values must be confirmed by the user; range validation; source label; delete and undo | 4 |
| H5 | Unsafe AI advice | Model invents facts or changes doses | 4 | 2 | 8 | Grounded library with citations; no-dose rule; report button; evaluation set | 6: needs evaluation results |
| H6 | Wrong emergency number | Outdated list or wrong country | 5 | 2 | 10 | Region auto-detected; user can choose a country or set their own number; 112 fallback note | 6: re-check quarterly |
| H7 | Loss of health records | Storage cleared or PIN forgotten | 3 | 3 | 9 | Backup and import; warnings; encrypted backups | 6 |
| H8 | Mistranslation | Unreviewed medical wording | 4 | 3 | 12 | Learn library kept in English with a note; UI translations flagged for review | 9: needs native clinical reviewers |
| H9 | Privacy breach | Lost phone or shared backup | 4 | 2 | 8 | App lock, encryption, throttle | 4 |
| H10 | Fraud via blood requests | Scammers ask for money | 3 | 3 | 9 | Built-in "Never send money" warning | 6 |

**Process still needed:** a named clinical safety officer, a complaint and incident route with a target response time, and a review of this log at every release.

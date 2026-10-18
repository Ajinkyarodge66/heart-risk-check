# Product requirements: Heart Risk Check (blueprint §3, §13 P0)

## Intended-purpose statement
Heart Risk Check is a **wellness and self-care app**. It helps adults:
- record blood pressure, medicines, weight and activity, and see their trends
- learn about heart health from reviewed official sources
- prepare for conversations with health professionals
- act quickly in an emergency by calling their local emergency number

It also includes a **research-preview** risk estimate from survey questions. It does **not** diagnose, exclude, treat or monitor any disease, and it makes no clinical decisions.

## Target users (first release)
1. Adults aged 40+ who are tracking their blood pressure, and their caregivers on the same phone.
2. Community health workers screening people for an NGO pilot, using health-worker mode.

## Claims inventory
| Claim we make | Evidence | Status |
| --- | --- | --- |
| Data stays on the device; no account | Architecture: no backend (see `privacy-data-map.md`) | ✅ True |
| Encrypted with AES-256 when app lock is on | `SECURITY.md`, tested | ✅ True |
| Classifies BP readings into categories | AHA categories, reviewed 14 Aug 2025 | ✅ Sourced |
| "X in 100 people like you" | Calibration on the BRFSS test set (`model-evaluation.md`) | ⚠️ Research only, US population |
| Ambulance numbers for 46 countries | Wikipedia list, checked 18 Oct 2026 | ⚠️ Needs re-checking on a schedule |
| Symptom urgency check | Rule-based, using NHS/AHA red flags | ⚠️ Not a triage device; needs clinical review |
| AI coach answers | Grounded in the reviewed library, with citations | ⚠️ Educational only; needs an evaluation set to pass (`ai-safety-evals.md`) |

## Explicitly out of scope (we do not claim these)
- Diagnosis, ruling out disease, treatment or medicine-dose advice.
- Automatic emergency detection or ambulance dispatch.
- Clinically validated risk prediction.
- Live doctor consultations (we link to official services instead).
- Accounts, cloud sync and sharing between phones (future, needs a backend).
- Collecting or trading money (blood donation is voluntary and unpaid; no patient fundraising).

## First-release scope (built)
- Logging and trends (BP with source labels and notes, medicines, weight, activity).
- Reports and exports (doctor report, QR code, CSV, encrypted backup).
- Emergency (SOS numbers, location to family, first aid, urgency check, Medical ID).
- Education (reviewed library) and AI coach (grounded, cited, with a report button).
- Family profiles and health-worker screening mode.
- Privacy and security (consent record, app lock, delete-all, privacy policy).
- 8 languages (UI translations still need native-speaker review).

## Acceptance criteria
A reviewer can see, inside the app (onboarding and About) and in this document, what the app does and what it explicitly does not do.

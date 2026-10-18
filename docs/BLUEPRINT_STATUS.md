# Blueprint compliance status: Heart Risk Check v5.0

Mapped against *Heart Health AI: Advanced Global Product & Engineering Blueprint v2.0* (`Heart_Health_AI_Blueprint.docx`).

**Key:** ✅ done and tested · 🟡 partly done · 🔧 needs a backend · 👥 needs people (clinicians, lawyers, partners, testers)

## §5 Functional requirements
| Requirement | Status | Where |
| --- | --- | --- |
| Secure sign-in, recovery, session revocation | 🔧 | No accounts by design (privacy-first). App lock covers device security |
| Explain intended use, limits, privacy, permissions | ✅ | First-run "Before you start" screen with a consent record |
| Guest experience | ✅ | The whole app works without an account |
| Minimal profile data, documented | ✅ | `privacy-data-map.md` |
| View, correct, export, delete | ✅ | Edit everywhere; CSV, report, QR, encrypted backup; "Delete all my data" |
| Language, unit, accessibility preferences | 🟡 | 8 languages, metric/imperial, dark mode, RTL. Font-size setting not yet added (the browser's text zoom works) |
| Dashboard of recent measurements | ✅ | Today tab |
| Manual vs imported vs derived data labels | ✅ | Every reading labelled Typed or Read from photo; risk labelled derived in CSV |
| Type, value, unit, time, source, notes | ✅ | BP records store all of these |
| Validate ranges; ask, don't silently alter | ✅ | Out-of-range values are refused and the field is focused |
| Trends with units, ranges, missing-data text | ✅ | 30-day chart in mmHg, target band, "N readings on D of 30 days" |
| No single reading presented as a diagnosis | ✅ | Wording and categories only |
| PDF/CSV export | 🟡 | CSV ✅ and text report ✅; PDF not added |
| Optional activity, sleep, nutrition logs | 🟡 | Activity ✅, weight ✅; sleep and nutrition not added |
| Editable goals, reminders, quiet hours | 🟡 | 150-minute goal; medicine schedule. Push reminders and quiet hours need a native app 🔧 |
| Non-judgemental, non-punitive language | ✅ | Badges and streaks only count up; there are no penalties |
| AI: approved library, citations, dates | ✅ | 8 reviewed guides (AHA, NHS, WHO) with review dates; answers cite [n] |
| AI: response policy, refusals, escalation | ✅ | Rules plus emergency-first routing |
| AI: minimal retention | ✅ | Chat in memory only; name never sent |
| AI: report inaccurate answers | ✅ | "Report this answer" button |
| Connected wearables | 🔧 | Health Connect after the Play launch |
| Reports with ranges, units, sources, not-a-diagnosis | ✅ | Doctor report and QR summary |
| Explicit action before sharing | ✅ | Every share or export needs a tap; no public links |
| Help, support, complaints | 🟡 | Feedback and AI-report via GitHub issues; a support inbox is still needed 👥 |
| Admin roles, audit, content versioning | 🔧 | Content versioned in code with review dates; no admin console |

## §6 Non-functional
| Attribute | Status |
| --- | --- |
| Reliability: offline, graceful degradation | ✅ Service worker; AI features hide when unavailable |
| Performance | ✅ Single 330 KB page; no network needed after the first load |
| Accessibility | 🟡 Labels, focus styles, reduced motion, chart text alternatives. Needs screen-reader testing 👥 |
| Maintainability | 🟡 Separate source files and a build step; no automated CI yet |
| Data integrity | ✅ Validation, ISO timestamps in exports, AES-GCM integrity check |
| Safety | ✅ `clinical-risk-register.md` |

## §7–9 Architecture, API, data model
🔧 These describe a backend (FastAPI, identity, health-record service). The current product deliberately has **no backend**, which removes the biggest breach risk. The data model fields (provenance, consent records, timestamps) are already in the on-device records, ready to move to a server later.

## §10 AI design and evaluation
✅ Curated library, citations, scope limits, urgent routing, injection guard, privacy, report button.
🟡 Evaluation suite written (`ai-safety-testset.json`, 16 cases); it must be **run and pass** before the coach is promoted. Human reviewers needed 👥

## §11 Prediction-model governance
✅ Target, population, horizon and intended action documented. Leakage prevention, baseline comparison (4 model families in the report), discrimination, calibration, sensitivity, specificity, PPV and NPV, subgroups and bootstrap CIs (`model-evaluation.md`). The app labels it "Research model" and warns under-45s.
👥 External validation in the target country, plus a harms review with clinicians.

## §12 Security and privacy
✅ Data map, encryption (PBKDF2 600k + AES-256-GCM), throttle, CSP, output encoding, privacy policy, threat model.
👥 DPIA under UK GDPR / DPDP Act before any server; independent penetration test.

## §13 Clinical and regulatory
✅ Intended-purpose statement, claims inventory, hazard log, wellness-only claims, AHA 2025 crisis wording.
👥 A clinical safety officer and MHRA/CDSCO advice before any medical claim.

## §14 Design system
✅ Colour and type tokens, light and dark, RTL, empty, offline and lock states, labelled charts, status shown with words as well as colour.

## §15 Release gates
See `release-gates.md`.

## §16–17 Growth and metrics
✅ Store listing, honest claims, tester invites, share messages without health data, no paid reviews.
👥 Metrics dashboard after launch (privacy-safe, counts only).

## What *nobody else can copy* (the blueprint's real answer)
No feature is uncopyable. What competitors cannot copy quickly:
1. **Local validation data:** run the pilot, then retrain and recalibrate on the target population.
2. **Partnerships:** the NGO, university and health-worker networks you sign first.
3. **Trust:** no account, no tracking, published model evaluation and security documents, honest limits.
4. **Speed of learning:** 12 testers → pilot → fixes every week.

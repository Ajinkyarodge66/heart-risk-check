# Release gates (blueprint §15): status for v5.0

| Gate | Evidence | Status |
| --- | --- | --- |
| Product | `product-requirements.md` (intended use, claims, exclusions) | ✅ Drafted, needs your approval |
| Design | Onboarding, empty, offline, error and lock states; RTL; dark mode; phone screenshots | ✅ Partly. Needs usability testing with 12+ real users |
| Engineering | Python-vs-JS model parity test; scripted end-to-end checks of every flow | ⚠️ No CI yet (add GitHub Actions) |
| Privacy | `privacy-data-map.md`, privacy policy, consent record, export and delete | ✅ For the no-backend design. A DPIA is needed before any server |
| Security | `SECURITY.md`, `threat-model.md`, CSP, encryption, throttle | ⚠️ Needs an independent penetration test before scale |
| AI | `ai-safety-testset.json` defined | ❌ Must be run and pass before promoting the AI coach |
| Clinical/regulatory | `clinical-risk-register.md`, research labelling | ❌ Needs a clinical safety officer and regulatory advice (MHRA/CDSCO) before any medical claim |
| Operational | Feedback channel, rollback by git revert | ⚠️ Needs monitoring and an incident playbook |
| Store | Listing, privacy policy, data-safety answers, 12-tester closed test | ⚠️ Ready to submit; the closed test hasn't started |

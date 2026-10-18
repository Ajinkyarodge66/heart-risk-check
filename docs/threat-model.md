# Threat model (STRIDE) (blueprint §12, security gate)

**Assets:** health records on the device, the PIN-derived key, backup files, the AI prompt and answers, and the integrity of the code served from GitHub Pages.

| Threat | Example | Current control | Residual risk / next step |
| --- | --- | --- | --- |
| **S**poofing | A fake site copying the app | Official URL in README and store listing; HTTPS via GitHub Pages | Medium: register a domain; Play Store listing with a verified developer |
| **T**ampering (code) | A changed library from a CDN | All JavaScript inlined; no third-party scripts; CSP blocks outside scripts | Low: add branch protection and signed commits on GitHub |
| **T**ampering (data) | Editing localStorage | AES-GCM detects any change to encrypted data | Low when the lock is on; medium when it's off |
| **R**epudiation | "I never agreed" | Consent records with policy version and timestamp | Low |
| **I**nformation disclosure (lost phone) | Thief reads the records | App lock with PBKDF2 600k + AES-256-GCM, auto-lock, throttle | Medium with short PINs; recommend 6+ digits plus the phone's own lock |
| **I**nformation disclosure (backup) | Backup file shared by mistake | Encrypted when the lock is on | Medium when the lock is off (users are warned) |
| **I**nformation disclosure (AI) | Name or personal data sent to an AI | Name excluded; data minimised; per-use consent | Low |
| **I**nformation disclosure (XSS) | Malicious text in a name or note | All output HTML-escaped; CSP | Low |
| **D**enial of service | Wiped storage | Encrypted export and import | Medium: browsers may clear storage; urge backups |
| **E**levation (prompt injection) | "Ignore rules" in a question | Data wrapped in tags with an instruction to treat it as data; rules repeated | Medium: needs the evaluation set and regression tests |
| Social engineering | Fake blood requests asking for money | Every request carries a "Never send money" warning | Medium: hospital verification needs a backend |

## Not yet done (required before a backend or real scale)
- An independent penetration test.
- Dependency and secret scanning in CI.
- A written incident-response playbook with named roles.
- A vulnerability disclosure policy with a private channel (currently via GitHub issues).

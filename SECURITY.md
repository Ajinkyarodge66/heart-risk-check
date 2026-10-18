# Security

## How Heart Risk Check protects data

| Layer | What it does |
| --- | --- |
| **No server** | All health data stays in the browser storage of the user's own device. There is no database to breach and no account to steal. |
| **Encryption at rest** (optional app lock) | A 6–12 digit PIN is stretched into a 256-bit key with PBKDF2-HMAC-SHA256 at 600,000 iterations (OWASP 2023), using a random 16-byte salt. Data is sealed with AES-256-GCM and a fresh 12-byte IV on every save. No plain-text copy is kept. |
| **Brute-force throttle** | After 5 wrong PINs, every further attempt waits 30 seconds, and the wait doubles each time up to 1 hour. |
| **Auto-lock** | The key is dropped from memory after 5 minutes in the background. |
| **Encrypted backups** | When app lock is on, exported backups are encrypted with the same key. |
| **No third-party code** | All JavaScript is inside the page, including the QR library, vendored under the MIT licence. The only outside requests are for fonts from Google Fonts. |
| **Content Security Policy** | The GitHub Pages build blocks scripts from other sites, plugins, form posts and base-URL hijacking, and sends no referrer. |
| **Output escaping** | Everything a user types is HTML-escaped before it is shown (XSS protection). |
| **AI privacy** | The AI coach is never sent the user's name, only age band, sex and readings. |

## Known limits (stated honestly)
- **No system is unbreakable.** Someone who has an unlocked phone, or who installs malware on it, can read what the app shows.
- **Short PINs are the weak point.** Someone who copies the encrypted data off the device can try PINs offline. 600,000 rounds slows this down, and the app requires at least 6 digits.
- **Forgotten PINs can't be recovered.** This is deliberate.
- **Without app lock, data is not encrypted.** It is protected only by the phone's own lock and its separation between apps.
- The `'unsafe-inline'` part of the security policy is needed because the app is built as a single file. Moving to external script files with hashes would tighten it further.

## Reporting a vulnerability
Please open a GitHub issue titled **"Security"** without exploit details, and the maintainer will contact you to share them privately. Do not test against other people's devices or data.

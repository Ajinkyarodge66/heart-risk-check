# Privacy data map (blueprint §12 "Data mapping")

**Summary:** no server, no account and no analytics. All personal data is held in the browser's storage on the user's device.

| Data | Why collected | Where stored | Leaves the device? | Retention / deletion |
| --- | --- | --- | --- | --- |
| Name, birth year, sex, height | Personalise the risk model and report | Device local storage (encrypted if app lock is on) | No | Until the user deletes it (Profile → Delete all my data) |
| BP readings (value, time, source, note) | Core tracking | Device | Only if the user exports, shares a report or QR, or uses the AI coach | User-controlled |
| Medicines and dose ticks | Reminders and adherence | Device | Only via a user export or report | User-controlled |
| Weight, activity, risk checks | Trends and reports | Device | Only via a user export or report | User-controlled |
| Medical ID and history | Emergencies and the doctor summary | Device | Only via a user-initiated QR, report or export | User-controlled |
| Blood-donation log | Donor card and badges | Device | No | User-controlled |
| Screening list (health-worker mode) | NGO pilots | Device; uses person codes, not names | Only via CSV export by the worker | The organisation's own policy applies after export |
| Consent records | Proof of informed use | Device | No | Deleted with all data |
| GPS location | SOS message | Not stored | Only inside a message the user sends to their own contact | Never retained |
| AI coach messages | Answer questions | In memory only, never saved | Sent to Claude (Anthropic) on the viewer's own account, without the person's name | Not retained by the app; the provider's terms apply |
| BP monitor photo | Read the numbers | Not stored | Sent to Claude for reading | Not retained by the app |
| IP address | Font loading | n/a | Google Fonts sees it when the app loads | Covered by Google's policy; can be removed by self-hosting the fonts |

## Third parties
- **Google Fonts:** font files only.
- **Claude (Anthropic):** the AI coach and photo reading, available only in the Claude-hosted version, with per-use consent.
- **Links opened by the user:** WhatsApp, maps, official health services and GitHub. Their own policies apply.

## Before collecting data on any server (future)
Complete a DPIA (data protection impact assessment) under UK GDPR / the Data Protection Act 2018 and the target-market laws (for example India's DPDP Act 2023), plus processor contracts, a transfer assessment and a retention schedule.

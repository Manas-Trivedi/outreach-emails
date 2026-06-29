# Internship Outreach - Email Database

Private repository containing all scraped company emails and HR contacts for paid internship outreach.

## Files

- `emails.csv` — 198 companies with general contact emails, categories, priority levels
- `hr_contacts.csv` — 53 named HR/TA/founder contacts with direct emails and LinkedIn profiles
- `make_sheet.py` — Python script to generate formatted Excel spreadsheet

## Stats

- **198** companies (Dubai/UAE + Gandhinagar/GIFT City/Infocity)
- **53** named HR contacts with direct emails
- **~130** High-priority targets
- **~25** verified direct HR/careers/recruitment inboxes

## Regions

- **Rounds 1-3**: Dubai/UAE tech companies (#1-143)
- **Rounds 4-8**: GIFT City, Infocity, Kudasan, Sargasan, Gandhinagar (#144-191)
- **Round 9**: PDPU corridor, Infocity expansion, Arrow/eInfochips (#192-198)

## Categories

Fintech, PropTech, HealthTech, EdTech, AI/ML, SaaS, Web Dev, App Dev, FoodTech, Logistics, Payments, Cybersecurity, Digital Marketing, IoT, Embedded, ERP, SAP

## Usage

```bash
pip install openpyxl
python make_sheet.py
```

Generates `Dubai_Internship_Outreach.xlsx` with 4 sheets:
1. All Companies
2. Priority Dubai Companies (High only)
3. Named HR Contacts
4. Email Template

## Career-page alert system

Monitors company career pages and alerts when **new postings** appear.

- `career_pages.csv` — pages to watch (`Company, URL, Notes`)
- `career_watch.py` — fetches each page, extracts job-like entries, diffs vs `career_state.json`, writes new entries to `career_alerts.md` / `career_alerts.log`
- `.github/workflows/career-watch.yml` — runs every 6h, opens a GitHub **issue** on new entries, commits updated state

```bash
pip install requests
python career_watch.py          # first run seeds state silently
```

Optional email alerts: set repo secrets `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_TO`.

**Known limits**
- Static fetch only — JS-rendered/SPA career pages (e.g. Argusoft, SmartSense) return 0 entries; needs a headless browser (Playwright) to upgrade.
- Heuristic role-keyword matching; per-page state means stable noise won't re-alert.
- Add/maintain URLs in `career_pages.csv`.

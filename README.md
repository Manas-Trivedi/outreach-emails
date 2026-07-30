# Internship Outreach

A database and toolkit for **paid-internship cold outreach**: a curated set of company/HR contacts plus Python scripts that clean, merge, batch, and export them for mail-merge sending, and a scheduled **career-page watcher** that alerts on new entry-level job postings. Designed to streamline internship outreach by combining verified contact data with automated career-page monitoring for faster application opportunities.

> ℹ️ **Contains personal data.** The CSVs hold scraped company emails, named HR/recruiter contacts, and LinkedIn profiles. Use the data responsibly, keep it accurate, and follow anti-spam / consent norms when contacting anyone.

---

## Stats

- **~400** companies (Dubai/UAE, Gandhinagar/GIFT City, and pan-India)
- **~1,300** named HR contacts with direct emails
- **~130** high-priority targets
- **~25** verified direct HR/careers/recruitment inboxes

---

## Contents

| Layer | Files |
|-------|-------|
| **Source data** | `emails.csv`, `hr_contacts.csv`, `extra_contacts.csv`, `career_pages.csv` |
| **Reference / imports** | `location_sheets/`, `all_emails.csv`, `dataniti_contacts.csv`, `*_companies.csv`, `dead_removed.csv` |
| **Scripts** | `gen_csv.py`, `import_external.py`, `add_pasted_batch*.py`, `gen_batches.py`, `gen_city_batches.py`, `make_sheet.py`, `career_watch.py` |
| **Generated output** | `batch_*.csv`, `city_*.csv`, `unsorted_*.csv`, `Dubai_Internship_Outreach.xlsx` |
| **Automation** | `.github/workflows/career-watch.yml`, `career_state.json`, `career_alerts.md/.log` |

---

## Source data

| File | Rows | Schema |
|------|------|--------|
| `emails.csv` | ~400 companies | `#, Company, Website, Category, General Contact Email, Email Type, HR Person Name, HR Person Title, HR Person Direct Email, LinkedIn Profile, Priority, Notes` |
| `hr_contacts.csv` | ~1,300 | `Company, Name, Title, Email, LinkedIn, Action` |
| `extra_contacts.csv` | ~12,900 | `Company, Name, Title, Email, LinkedIn, Action` (externally imported, same schema) |
| `career_pages.csv` | ~1,000 | `Company, URL, Location, EntryLevel, Notes` |

**Categories:** Fintech, PropTech, HealthTech, EdTech, AI/ML, SaaS, Web Dev, App Dev, FoodTech, Logistics, Payments, Cybersecurity, Digital Marketing, IoT, Embedded, ERP, SAP.

**Regions covered:** Dubai/UAE, GIFT City / Gandhinagar / Infocity, and Indian metros (Bengaluru, Delhi NCR, Hyderabad, Pune, Chennai, Mumbai, Lucknow, and more via `location_sheets/`).

### Outreach history

- **Rounds 1–3:** Dubai/UAE tech companies (#1–143)
- **Rounds 4–8:** GIFT City, Infocity, Kudasan, Sargasan, Gandhinagar (#144–191)
- **Round 9:** PDPU corridor, Infocity expansion, Arrow/eInfochips (#192–198)
- **Round 10+:** pan-India expansion — Bengaluru, Hyderabad, Pune, Jaipur, Lucknow, Kota, and other metros (see `city_*.csv` batches)

---

## The pipeline

```
external sheets ──import_external.py──┐
pasted lists ────add_pasted_batch*.py─┤──► extra_contacts.csv
                                      │
emails.csv + hr_contacts.csv + extra_contacts.csv
                                      │
              ┌───────────────────────┼───────────────────────┐
       gen_batches.py          gen_city_batches.py        make_sheet.py
              │                        │                        │
        batch_NN.csv          city_<city>_NN.csv     Dubai_Internship_Outreach.xlsx
     (100/contacts, flat)   (100/contacts, per city)      (4-sheet workbook)
```

| Script | What it does |
|--------|--------------|
| `gen_csv.py` | Regenerates `emails.csv` + `hr_contacts.csv` from the data embedded in `make_sheet.py`. |
| `import_external.py` | Imports external contact files (xlsx/csv) into `extra_contacts.csv`, deduping against existing rows. |
| `add_pasted_batch.py` / `add_pasted_batch2.py` | One-off appenders for hand-pasted email lists → `extra_contacts.csv`. |
| `gen_batches.py` | Splits the merged contact pool into `batch_NN.csv` of 100 each (best email per company: HR/CEO direct if present, else general). |
| `gen_city_batches.py` | Same pool, split **per city** into `city_<city>_NN.csv` for targeted sends. |
| `make_sheet.py` | Builds `Dubai_Internship_Outreach.xlsx` (All Companies · Priority · Named HR Contacts · Email Template). |
| `career_watch.py` | Career-page watcher — see below. |

---

## Setup

```bash
pip install -r requirements.txt
```

Generate the sendable batches / spreadsheet:

```bash
python gen_batches.py        # -> batch_01.csv, batch_02.csv, ...
python gen_city_batches.py   # -> city_bengaluru_01.csv, ...
python make_sheet.py         # -> Dubai_Internship_Outreach.xlsx
```

---

## Career-page alert system

Monitors company career pages and alerts when **new postings** appear, with a focus on **entry-level / fresher** roles.

- `career_pages.csv` — pages to watch (`Company, URL, Location, EntryLevel, Notes`).
- `career_watch.py` — fetches each page, extracts job-like entries, diffs against `career_state.json`, and writes new entries to `career_alerts.md` (consumed by the Action) and `career_alerts.log`.
- `.github/workflows/career-watch.yml` — runs twice a day, opens a GitHub **issue** on new entries, and commits the updated state.

```bash
python career_watch.py          # first run seeds state silently
```

**Entry-level focus** — postings that look like fresher/graduate/trainee/intern/0–1 yr are flagged 🎓. Rows with `EntryLevel=yes` only alert on entry-level postings.

**Rendering JS (SPA / MNC portals)** — static fetch can't read SPA portals (Infosys joblist, TCS iBegin, etc.). The Action installs Playwright and runs with `RENDER=1`. Locally:

```bash
pip install playwright && playwright install chromium
RENDER=1 python career_watch.py
```

**Optional email alerts** — set repo secrets `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_TO`.

**Known limits** — heuristic role-keyword matching; per-page state means stable noise won't re-alert; some portals bot-block (HTTP 403) even with rendering — swap to their public job-search API or an aggregator URL if so.

---

## Best practices

- Personalize your outreach emails for higher response rates.
- Verify contact information before sending.
- Avoid sending bulk or spam emails; respect unsubscribe requests and anti-spam rules.

---

## Notes

- `batch_*.csv`, `city_*.csv`, `unsorted_*.csv`, and the `.xlsx` are **generated** — recreate them any time from the source CSVs with the commands above.
- `dead_removed.csv` tracks contacts pruned as dead/bounced.

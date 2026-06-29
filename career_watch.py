#!/usr/bin/env python3
"""
career_watch.py — Monitor company career pages and alert on NEW entries.

Reads career_pages.csv (Company, URL, Location, EntryLevel, Notes), fetches each
page, extracts job-like entries (anchor text + lines matching role keywords),
and diffs against the saved snapshot in career_state.json. New entries are
written to career_alerts.md (consumed by the GitHub Action to open an issue) and
appended to career_alerts.log. State is updated in place so the next run only
reports genuinely new postings.

Entry-level focus:
  - Entries that look like 0-experience roles (fresher/graduate/trainee/intern/
    entry level/0-1 yr/campus) are flagged with 🎓.
  - If a row sets EntryLevel=yes, ONLY entry-level new entries are alerted.

Rendering:
  - Default: static fetch (requests). Fast, but JS-rendered/SPA career pages
    (most large MNC portals) return 0 entries.
  - Set RENDER=1 (and `pip install playwright && playwright install chromium`)
    to render JavaScript so SPA pages yield listings.

Run:
    pip install requests
    python career_watch.py

Optional email alert (set all five env vars):
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_TO
"""
import csv
import json
import os
import re
import sys
import smtplib
import datetime as dt
from email.mime.text import MIMEText
from html.parser import HTMLParser

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

PAGES_CSV = "career_pages.csv"
STATE_FILE = "career_state.json"
ALERTS_MD = "career_alerts.md"
ALERTS_LOG = "career_alerts.log"

UA = "Mozilla/5.0 (compatible; CareerWatch/1.0; internship-outreach)"
TIMEOUT = 25
RENDER = os.getenv("RENDER") == "1"

ROLE_RE = re.compile(
    r"\b(engineer|developer|intern(ship)?|manager|designer|analyst|lead|architect|"
    r"consultant|executive|associate|specialist|trainee|qa|sde|devops|scientist|"
    r"recruiter|fresher|hiring|vacancy|opening|apply|graduate)\b",
    re.I,
)
# Looks like a 0-experience / early-career role.
ENTRY_RE = re.compile(
    r"\b(fresher|freshers|graduate|trainee|intern(ship)?|entry[ -]?level|"
    r"campus|off[ -]?campus|associate|junior|0[ -]?1\s*year|0\s*-\s*1|"
    r"no experience|0\s*yr|new grad)\b",
    re.I,
)
NOISE_RE = re.compile(
    r"^(home|about|contact|privacy|terms|cookie|login|sign in|menu|careers?|"
    r"life at|why join|benefits|culture|search|apply now|view all|learn more)$",
    re.I,
)


class TextLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks = []
        self._skip = 0
        self._in_a = False
        self._a_text = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self._skip += 1
        if tag == "a":
            self._in_a = True
            self._a_text = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self._skip:
            self._skip -= 1
        if tag == "a" and self._in_a:
            self._in_a = False
            t = " ".join(self._a_text).strip()
            if t:
                self.chunks.append(t)

    def handle_data(self, data):
        if self._skip:
            return
        text = data.strip()
        if not text:
            return
        if self._in_a:
            self._a_text.append(text)
        else:
            self.chunks.append(text)


def normalize(s):
    return re.sub(r"\s+", " ", s).strip()


def extract_entries(html):
    parser = TextLinkExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass
    entries = set()
    for raw in parser.chunks:
        s = normalize(raw)
        if not (3 < len(s) < 140):
            continue
        if NOISE_RE.match(s):
            continue
        if ROLE_RE.search(s):
            entries.add(s)
    return sorted(entries)


def is_entry_level(s):
    return bool(ENTRY_RE.search(s))


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False, sort_keys=True)


def read_pages():
    with open(PAGES_CSV, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r.get("URL", "").strip()]


def fetch_static(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text


def fetch_rendered(url):
    """Render JS with Playwright if available; else fall back to static."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return fetch_static(url)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent=UA)
        page.goto(url, wait_until="networkidle", timeout=TIMEOUT * 1000)
        html = page.content()
        browser.close()
        return html


def fetch(url):
    return fetch_rendered(url) if RENDER else fetch_static(url)


def truthy(v):
    return str(v).strip().lower() in ("yes", "true", "1", "y")


def send_email(subject, body):
    if not all(os.getenv(k) for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS", "ALERT_TO")):
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("ALERT_TO")
    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", "587"))) as s:
        s.starttls()
        s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        s.sendmail(msg["From"], [msg["To"]], msg.as_string())
    return True


def main():
    now = dt.datetime.now().isoformat(timespec="seconds")
    state = load_state()
    pages = read_pages()
    alerts = []   # (label, url, [(entry, entry_level_bool)])
    errors = []

    for row in pages:
        company = row.get("Company", "").strip() or row["URL"]
        location = row.get("Location", "").strip()
        label = f"{company} — {location}" if location else company
        url = row["URL"].strip()
        entry_only = truthy(row.get("EntryLevel", ""))

        try:
            entries = extract_entries(fetch(url))
        except Exception as e:
            errors.append((label, url, str(e)[:120]))
            continue

        prev = set(state.get(url, {}).get("entries", []))
        first_run = url not in state
        new = [e for e in entries if e not in prev]
        if entry_only:
            new = [e for e in new if is_entry_level(e)]

        if new and not first_run:
            alerts.append((label, url, [(e, is_entry_level(e)) for e in new]))

        state[url] = {
            "company": company,
            "location": location,
            "entry_only": entry_only,
            "entries": entries,
            "count": len(entries),
            "last_checked": now,
        }

    save_state(state)

    md_lines = []
    if alerts:
        md_lines.append(f"# 🔔 New career-page entries — {now}\n")
        for label, url, items in alerts:
            md_lines.append(f"## {label}\n<{url}>\n")
            for entry, entry_lvl in items:
                md_lines.append(f"- {'🎓 ' if entry_lvl else ''}{entry}")
            md_lines.append("")
    md = "\n".join(md_lines)

    with open(ALERTS_MD, "w", encoding="utf-8") as f:
        f.write(md)

    if alerts:
        with open(ALERTS_LOG, "a", encoding="utf-8") as f:
            f.write(md + "\n")
        total = sum(len(i) for _, _, i in alerts)
        sent = send_email(f"[CareerWatch] {total} new posting(s)", md)
        print(f"ALERT: {total} new entries across {len(alerts)} pages"
              f"{' (emailed)' if sent else ''}")
    else:
        print("No new entries.")

    for label, url, err in errors:
        print(f"  ! fetch failed: {label} <{url}> — {err}", file=sys.stderr)

    mode = "RENDER" if RENDER else "static"
    print(f"Checked {len(pages)} pages ({mode}), {len(errors)} errors, {now}")


if __name__ == "__main__":
    main()

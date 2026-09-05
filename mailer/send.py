#!/usr/bin/env python3
"""
Simple CSV -> email mail-merge sender.

Point it at a CSV of recipients and a template; it renders the template once per
row and sends over SMTP. Dry run is the default: nothing leaves the machine
unless you pass --send.

Usage:
  python send.py --file recipients.csv                 # dry-run preview
  python send.py --file recipients.csv --send          # actually send
  python send.py --file recipients.csv --limit 20 --send
  python send.py --file recipients.csv --template followup --send

Credentials come from the environment or a local .env (see .env.example):
  SMTP_USER, SMTP_PASS, and optionally SMTP_HOST (default smtp.gmail.com) and
  SMTP_PORT (default 465).

CSV columns: at minimum `email`. Any other columns (first_name, company, ...)
plus the constants under "template_vars" in settings.json are available to the
template as {first_name}, {company}, {your_name}, etc.
"""
import argparse
import csv
import json
import os
import smtplib
import ssl
import time
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent


def load_env(path: Path = ROOT / ".env") -> None:
    """Load KEY=VALUE lines from a local .env, without overriding real env vars."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_settings() -> dict:
    path = ROOT / "settings.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def render(template_text: str, context: dict) -> tuple[str, str]:
    """First 'Subject:' line becomes the subject; the rest is the body."""
    lines = template_text.splitlines()
    subject, start = "", 0
    if lines and lines[0].lower().startswith("subject:"):
        subject = lines[0].split(":", 1)[1].strip()
        start = 1
        if start < len(lines) and not lines[start].strip():
            start += 1
    body = "\n".join(lines[start:])
    try:
        return subject.format(**context), body.format(**context)
    except KeyError as exc:
        raise SystemExit(
            f"template uses {{{exc.args[0]}}} but neither the CSV nor "
            f"settings.template_vars provides it"
        )


def already_sent(log_path: Path) -> set:
    if not log_path.exists():
        return set()
    with log_path.open(encoding="utf-8") as fh:
        return {
            (r.get("email") or "").strip().lower()
            for r in csv.DictReader(fh)
            if r.get("email")
        }

def load_suppressed_emails(dns_audit_path, hard_bounce_path):
    suppressed = set()

    if dns_audit_path.exists():
        with dns_audit_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)

            for row in reader:
                email = (row.get("email") or "").strip().lower()
                status = (row.get("status") or "").strip()

                if email and status in {"INVALID_FORMAT", "NO_MX"}:
                    suppressed.add(email)

    if hard_bounce_path.exists():
        with hard_bounce_path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)

            for row in reader:
                email = (row.get("email") or "").strip().lower()
                if email:
                    suppressed.add(email)

    return suppressed

def sent_today(log_path: Path) -> int:
    if not log_path.exists():
        return 0

    today = time.strftime("%Y-%m-%d")
    count = 0

    with log_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            ts = row.get("ts")
            if not ts:
                continue

            if time.strftime("%Y-%m-%d", time.localtime(int(ts))) == today:
                count += 1

    return count


def main() -> None:
    ap = argparse.ArgumentParser(description="Send a CSV mail-merge. Dry-run by default.")
    ap.add_argument("--file", required=True, help="recipients CSV (needs an 'email' column)")
    ap.add_argument("--template", default=None, help="template name in templates/ (no .txt)")
    ap.add_argument("--limit", type=int, help="cap the number of recipients this run")
    ap.add_argument("--delay", type=float, help="seconds to wait between sends")
    ap.add_argument("--send", action="store_true", help="actually send (default is dry-run)")
    args = ap.parse_args()

    load_env()
    settings = load_settings()
    template_vars = settings.get("template_vars", {})

    tpl_name = args.template or settings.get("default_template", "default")
    tpl_path = ROOT / "templates" / f"{tpl_name}.txt"
    if not tpl_path.exists():
        raise SystemExit(f"no template at {tpl_path}")
    template_text = tpl_path.read_text(encoding="utf-8")

    csv_path = Path(args.file)
    if not csv_path.exists():
        raise SystemExit(f"no CSV at {csv_path}")
    with csv_path.open(encoding="utf-8") as fh:
        raw_rows = list(csv.DictReader(fh))

    rows = []
    for r in raw_rows:
        # Normalize the repository's batch schema to the mailer's schema.
        if not r.get("email"):
            r["email"] = r.get("Email", "")

        if not r.get("first_name"):
            r["first_name"] = r.get("Person", "")

        if not r.get("company"):
            r["company"] = r.get("Company", "")

        if r.get("email", "").strip():
            rows.append(r)

    log_path = ROOT / "sent_log.csv"
    dns_audit_path = REPO_ROOT / "state" / "email_dns_audit.csv"
    hard_bounce_path = REPO_ROOT / "state" / "hard_bounces.csv"
    suppressed = load_suppressed_emails(
        dns_audit_path,
        hard_bounce_path,
    )

    seen = already_sent(log_path)

    # Suppress known-invalid / hard-bounced addresses first.
    before_suppression = len(rows)
    rows = [
        r for r in rows
        if r["email"].strip().lower() not in suppressed
    ]
    suppressed_count = before_suppression - len(rows)
    print(f"suppressed by DNS/bounce list: {suppressed_count}")

    # Skip addresses we've already successfully sent to.
    before_sent_filter = len(rows)
    rows = [
        r for r in rows
        if r["email"].strip().lower() not in seen
    ]
    already_sent_count = before_sent_filter - len(rows)
    print(f"already sent: {already_sent_count}")

    daily_cap = settings.get("max_daily_sends", 100)
    remaining_today = max(0, daily_cap - sent_today(log_path))

    if remaining_today == 0:
        print(f"daily send limit reached ({daily_cap}).")
        return

    if args.limit:
        rows = rows[: args.limit]

    rows = rows[:remaining_today]

    print(f"template: {tpl_name} | recipients ready to send: {len(rows)}")

    if not rows:
        print("nothing to send.")
        return

    if not args.send:
        subject, body = render(template_text, {**template_vars, **rows[0]})
        print("\n--- DRY RUN (pass --send to actually mail) ---")
        print(f"to (first of {len(rows)}): {rows[0]['email'].strip()}")
        print(f"subject: {subject}\n")
        print(body[:600])
        return

    user, password = os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASS")
    if not user or not password:
        raise SystemExit("SMTP_USER and SMTP_PASS must be set (see .env.example)")
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    from_name = settings.get("from_name", user)
    attachments = [ROOT / a for a in settings.get("attachments", [])]
    delay = args.delay if args.delay is not None else settings.get("delay_seconds", 5)

    sent = 0
    with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as server:
        server.login(user, password)
        with log_path.open("a", newline="", encoding="utf-8") as logf:
            writer = csv.writer(logf)
            if log_path.stat().st_size == 0:
                writer.writerow(["email", "subject", "ts"])
            for i, row in enumerate(rows):
                subject, body = render(template_text, {**template_vars, **row})
                msg = EmailMessage()
                msg["From"] = f"{from_name} <{user}>"
                msg["To"] = row["email"].strip()
                if settings.get("reply_to"):
                    msg["Reply-To"] = settings["reply_to"]
                msg["Subject"] = subject
                msg.set_content(body)
                for att in attachments:
                    if att.exists():
                        msg.add_attachment(
                            att.read_bytes(),
                            maintype="application",
                            subtype="octet-stream",
                            filename=att.name,
                        )
                server.send_message(msg)
                writer.writerow([row["email"].strip(), subject, int(time.time())])
                logf.flush()
                sent += 1
                print(f"  sent {sent}/{len(rows)}: {row['email'].strip()}")
                if i < len(rows) - 1 and delay:
                    time.sleep(delay)
    print(f"done. sent {sent}.")


if __name__ == "__main__":
    main()
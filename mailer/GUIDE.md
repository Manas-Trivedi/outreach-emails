# mailer - simple CSV to email sender

A small mail-merge. Point it at a CSV of recipients and a template, and it sends
one personalized email per row over SMTP. **Dry run is the default**, so nothing
is sent until you explicitly pass `--send`.

## Setup

1. To actually send, copy the env template and fill in your SMTP credentials:
   ```bash
   cp mailer/.env.example mailer/.env
   ```
   For Gmail, `SMTP_PASS` is an **App Password** (16 chars), not your account
   password: myaccount.google.com -> Security -> 2-Step Verification -> App
   passwords. `.env` is gitignored; never commit it.

2. Edit `mailer/settings.json`:
   - `from_name`, `reply_to`
   - `attachments` (e.g. your resume: put the file in `mailer/` and list its name)
   - `template_vars` (your name, headline, contact line, availability). These fill
     the `{your_name}`-style placeholders in the templates.

3. Edit the templates in `mailer/templates/` to your own words.

## Recipients CSV

A CSV with at least an `email` column. Any other column is available to the
template. Example (`sample_recipients.csv`):

```
email,first_name,company
careers@example.com,Team,Example Labs
```

`{first_name}` and `{company}` in the template come from these columns; things
like `{your_name}` come from `template_vars` in settings.

## Sending

```bash
# preview what would go out (default; sends nothing):
python mailer/send.py --file mailer/sample_recipients.csv

# actually send:
python mailer/send.py --file path/to/recipients.csv --send

# cap the run and pick a template:
python mailer/send.py --file recipients.csv --limit 20 --template followup --send
```

## Behavior

- **Dry run by default.** `--send` is the only thing that puts mail on the wire.
- **No double-sends.** Every send is appended to `sent_log.csv` (gitignored);
  addresses already in it are skipped next run.
- **Rate limiting.** `delay_seconds` in settings (default 8) spaces out sends.

## Please use this responsibly

Only email people who would reasonably expect to hear from you (for example a
public `careers@` address about a role), personalize it, and honor any opt-out.
Sending bulk mail to addresses gathered without consent can violate your email
provider's terms and anti-spam laws, and it is the fast way to get an account
suspended. This tool ships with a synthetic sample only; bring your own list and
keep it out of any public repository.
# Contributing to outreach-emails

Thank you for taking the time to contribute! This document outlines how to participate in this project effectively and responsibly.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Development Setup](#development-setup)
- [Data & Privacy Guidelines](#data--privacy-guidelines)
- [Coding Standards](#coding-standards)
- [Commit Message Style](#commit-message-style)
- [Issue Labels](#issue-labels)

---

## Code of Conduct

This project follows a simple rule: **be respectful**. Harassment, discrimination, or hostile communication of any kind will not be tolerated. Violations may result in being banned from contributing.

---

## How to Contribute

### Reporting Bugs

If you find a bug, please [open an issue](https://github.com/eeshsaxena/outreach-emails/issues/new) with:

1. **A clear, descriptive title** — e.g., `[Bug] add_pasted_batch.py does not write output to CSV`
2. **Steps to reproduce** — exact commands, inputs, and environment
3. **Expected behaviour** — what should have happened
4. **Actual behaviour** — what actually happened, including error messages/tracebacks
5. **File & line number** — pinpoint the location of the bug
6. **Suggested fix** (optional) — if you already know the fix

> [!TIP]
> Before filing a new issue, search existing issues to avoid duplicates.

### Suggesting Enhancements

Open an issue with the label `enhancement` and describe:
- What problem the enhancement solves
- Your proposed solution
- Any alternatives you considered

### Submitting a Pull Request

1. **Fork** the repository and create a branch from `master`:
   ```bash
   git checkout -b fix/your-fix-description
   ```

2. **Make your changes** — keep each PR focused on a single fix or feature.

3. **Test your changes** locally before pushing.

4. **Ensure no sensitive data** is included (see [Data & Privacy Guidelines](#data--privacy-guidelines)).

5. **Push** your branch and open a Pull Request against `master`.

6. Fill in the PR template:
   - What does this PR change?
   - Which issue(s) does it fix? (use `Closes #<issue-number>`)
   - How was it tested?

7. A maintainer will review your PR. Please be responsive to feedback.

---

## Development Setup

### Prerequisites

- Python 3.10+
- `pip`

### Install dependencies

```bash
pip install requests playwright openpyxl
playwright install --with-deps chromium
```

### Running scripts locally

```bash
# Generate the Excel outreach sheet
python make_sheet.py

# Add a new batch of emails
python add_pasted_batch.py

# Run the career page monitor manually
python career_watch.py
```

---

## Data & Privacy Guidelines

> [!IMPORTANT]
> This repository handles **real personal email addresses**. Please follow these rules strictly.

1. **Never commit credentials** — API keys, tokens, or passwords must never appear in source files or CSVs. Use environment variables or GitHub Secrets.

2. **Email validation is mandatory** — Any script that writes emails to a CSV must validate them first. Use the helper below or an equivalent:

   ```python
   import re
   EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

   def is_valid_email(email: str) -> bool:
       return bool(EMAIL_RE.match(email.strip()))
   ```

3. **Deduplication is mandatory** — Always check for existing entries before appending. Do not let the same email appear in a file more than once.

4. **No junk/placeholder data** — Strings like `yyo`, `test`, `example@` must not appear in any CSV or email list.

5. **If in doubt, leave it out** — When unsure whether an email belongs or is valid, skip it and document why.

6. **`.gitignore` hygiene** — Do not commit local state files (e.g., `career_state.json`, `known_domains.txt`). Add them to `.gitignore`.

---

## Coding Standards

All Python contributions must follow these guidelines:

### Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) — use `black` for auto-formatting:
  ```bash
  pip install black
  black .
  ```
- Maximum line length: **100 characters**
- Use **type hints** for function signatures where reasonable
- Use **f-strings** for string formatting (not `.format()` or `%`)

### Scripts that write CSVs

Every script that reads/writes CSV files must:
1. Use `newline=""` when opening files with the `csv` module
2. Validate all emails before writing
3. Deduplicate against existing entries
4. Print a summary on completion: rows written, rows skipped, reasons

Example template:

```python
import csv
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
OUTPUT_FILE = "extra_contacts.csv"

EMAILS = """
# paste emails here
"""

def load_existing(filepath: str) -> set[str]:
    existing = set()
    try:
        with open(filepath, newline="") as f:
            for row in csv.reader(f):
                if row:
                    existing.add(row[0].strip().lower())
    except FileNotFoundError:
        pass
    return existing

def main():
    existing = load_existing(OUTPUT_FILE)
    written, skipped_invalid, skipped_dup = 0, 0, 0

    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        for line in EMAILS.strip().splitlines():
            email = line.strip()
            if not email or email.startswith("#"):
                continue
            if not EMAIL_RE.match(email):
                print(f"[INVALID]   {email}")
                skipped_invalid += 1
            elif email.lower() in existing:
                print(f"[DUPLICATE] {email}")
                skipped_dup += 1
            else:
                writer.writerow([email])
                existing.add(email.lower())
                written += 1

    print(f"\nDone. Written: {written}, Invalid: {skipped_invalid}, Duplicates: {skipped_dup}")

if __name__ == "__main__":
    main()
```

### GitHub Actions Workflows

- Every workflow step must have a **`name`** and a **`run`** command
- Always set `timeout-minutes` to prevent hung jobs from consuming Actions minutes
- Add comments explaining billing trade-offs if changing cron schedules
- Never hard-code secrets — always use `${{ secrets.GITHUB_TOKEN }}` or custom secrets

---

## Commit Message Style

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short summary>
```

| Type | When to use |
|------|-------------|
| `fix` | Bug fixes |
| `feat` | New features |
| `data` | Adding/updating CSV data |
| `chore` | Maintenance tasks, dependency updates |
| `docs` | Documentation changes |
| `ci` | GitHub Actions / workflow changes |
| `refactor` | Code changes that don't fix bugs or add features |

**Examples:**
```
fix(batch): remove junk 'yyo' entry from add_pasted_batch.py
feat(batch): add email validation and deduplication logic
data(bangalore): add 20 new startup contacts from batch 144
ci(career-watch): fix truncated run step in workflow YAML
docs(readme): correct file references and fix truncated sentence
```

---

## Issue Labels

| Label | Meaning |
|-------|---------|
| `bug` | Something isn't working correctly |
| `enhancement` | New feature or request |
| `data` | CSV data quality issue |
| `ci/cd` | GitHub Actions workflow issue |
| `docs` | Documentation improvement |
| `good first issue` | Great for newcomers |
| `help wanted` | Extra attention needed |
| `invalid` | Not a valid issue |
| `wontfix` | Will not be addressed |

---

## Questions?

If you have a question that isn't answered here, open a [Discussion](https://github.com/eeshsaxena/outreach-emails/discussions) or comment on an existing issue.

---

*Happy contributing! 🚀*

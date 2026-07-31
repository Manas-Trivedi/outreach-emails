import csv, re, os

_HERE = os.path.dirname(os.path.abspath(__file__))
_IND = os.path.join(_HERE, "..", "industry")

with open(os.path.join(_HERE, "make_sheet.py"), encoding="utf-8") as f:
    src = f.read()

def extract_list(src, varname):
    match = re.search(varname + r"\s*=\s*\[", src)
    start = src.index("[", match.start())
    depth, i = 1, start + 1
    while depth > 0:
        if src[i] == "[":
            depth += 1
        elif src[i] == "]":
            depth -= 1
        i += 1
    return eval(src[start:i])

companies = extract_list(src, "companies")
hr_contacts = extract_list(src, "hr_contacts")

with open(os.path.join(_IND, "emails.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["#","Company","Website","Category","General Contact Email","Email Type","HR Person Name","HR Person Title","HR Person Direct Email","LinkedIn Profile","Priority","Notes"])
    for c in companies:
        w.writerow(c)

with open(os.path.join(_IND, "hr_contacts.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Company","Name","Title","Email","LinkedIn","Action"])
    for h in hr_contacts:
        w.writerow(h)

print(f"emails.csv: {len(companies)} rows")
print(f"hr_contacts.csv: {len(hr_contacts)} rows")

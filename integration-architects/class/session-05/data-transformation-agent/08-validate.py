import json, re
from pathlib import Path

BASE = Path(__file__).resolve().parent
if BASE.name == "reference":
    BASE = BASE.parent

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ID = re.compile(r"^C\d{4}$")
PHONE = re.compile(r"^\+91-\d{10}$")
KNOWN_STATES = {"Maharashtra", "Karnataka", "Delhi"}

def normalize_records(payload):
    if isinstance(payload, dict):
        for key in ("transformed", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
        if payload:
            return [v for v in payload.values() if isinstance(v, dict)]
        return []
    if isinstance(payload, list):
        return payload
    return []


def validate(records):
    counts = {}
    for r in records:
        if not isinstance(r, dict):
            continue
        counts[r.get("customerId")] = counts.get(r.get("customerId"), 0) + 1

    valid, invalid = [], []
    for r in records:
        errors = []
        cid = r.get("customerId")
        if not isinstance(cid, str) or not ID.match(cid):
            errors.append("INVALID_CUSTOMER_ID")
        if counts.get(cid, 0) > 1:
            errors.append("DUPLICATE_CUSTOMER_ID")
        if not r.get("fullName"):
            errors.append("MISSING_FULL_NAME")
        email = r.get("email")
        if email and not EMAIL.match(email):
            errors.append("INVALID_EMAIL")
        phone = r.get("phone")
        if phone and not PHONE.match(phone):
            errors.append("INVALID_PHONE")
        if r.get("state") not in KNOWN_STATES:
            errors.append("UNKNOWN_STATE")
        (invalid if errors else valid).append({"record": r, "errors": errors} if errors else r)
    return valid, invalid

def main():
    payload = json.loads((BASE/"output"/"transformed.json").read_text())
    records = normalize_records(payload)
    valid, invalid = validate(records)
    (BASE/"output"/"valid.json").write_text(json.dumps(valid, indent=2))
    (BASE/"output"/"invalid.json").write_text(json.dumps(invalid, indent=2))
    print(f"Valid={len(valid)} Invalid={len(invalid)}")
    for item in invalid:
        print(item["record"].get("customerId"), "->", ", ".join(item["errors"]))

if __name__ == "__main__":
    main()

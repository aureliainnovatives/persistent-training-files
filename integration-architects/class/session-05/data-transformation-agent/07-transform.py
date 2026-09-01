import json
import re
from pathlib import Path
from typing import Any


INPUT_PATH = Path(__file__).with_name("04-source-data.json")
OUTPUT_PATH = Path(__file__).with_name("output") / "transformed.json"

STATE_CODE_MAP = {
    "MH": "Maharashtra",
    "KA": "Karnataka",
    "DL": "Delhi",
}
CUSTOMER_ID_PATTERN = re.compile(r"^C[0-9]{4}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _trim(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def _normalized_text(value: Any) -> Any:
    value = _trim(value)
    return value.lower() if isinstance(value, str) else value


def _combine_names(first_name: Any, last_name: Any) -> Any:
    first_name = _trim(first_name)
    last_name = _trim(last_name)
    names = [name for name in (first_name, last_name) if isinstance(name, str) and name]
    if names:
        return " ".join(names)
    return first_name


def _normalize_phone(value: Any) -> Any:
    value = _trim(value)
    if isinstance(value, str) and re.fullmatch(r"[0-9]{10}", value):
        return f"+91-{value}"
    return value


def transform_customer(source: dict[str, Any]) -> dict[str, Any]:
    """Apply only the approved field mappings to one source customer."""
    source_state = _trim(source.get("state"))
    return {
        "customerId": _trim(source.get("cust_no")),
        "fullName": _combine_names(source.get("first_name"), source.get("last_name")),
        "email": _normalized_text(source.get("mail")),
        "phone": _normalize_phone(source.get("mobile")),
        "state": STATE_CODE_MAP.get(source_state, source_state),
    }


def validate_customer(customer: dict[str, Any], seen_ids: set[str]) -> list[str]:
    """Return validation errors without changing the transformed customer."""
    errors = []
    customer_id = customer.get("customerId")
    if not isinstance(customer_id, str) or not CUSTOMER_ID_PATTERN.fullmatch(customer_id):
        errors.append("BR-01: customerId is missing or does not match ^C[0-9]{4}$")
    elif customer_id in seen_ids:
        errors.append("BR-09: duplicate customerId")

    full_name = customer.get("fullName")
    if not isinstance(full_name, str) or not full_name:
        errors.append("BR-02: fullName is missing or empty")

    email = customer.get("email")
    if email not in (None, "") and (
        not isinstance(email, str) or not EMAIL_PATTERN.fullmatch(email)
    ):
        errors.append("BR-03: supplied email is invalid")

    phone = customer.get("phone")
    if phone not in (None, "") and (
        not isinstance(phone, str)
        or not re.fullmatch(r"[0-9]{10}", phone)
        and not re.fullmatch(r"\+91-[0-9]{10}", phone)
    ):
        errors.append("BR-04: supplied phone is not exactly 10 digits")

    state = customer.get("state")
    if state not in STATE_CODE_MAP.values():
        errors.append("BR-05/BR-08: state is missing or contains an unknown value")

    return errors


def transform_records(source_records: list[dict[str, Any]]) -> dict[str, list[Any]]:
    transformed_records = [transform_customer(source) for source in source_records]
    id_counts: dict[str, int] = {}
    for customer in transformed_records:
        customer_id = customer.get("customerId")
        if isinstance(customer_id, str):
            id_counts[customer_id] = id_counts.get(customer_id, 0) + 1

    valid_records = []
    quarantine_records = []
    for source, customer in zip(source_records, transformed_records):
        customer_id = customer.get("customerId")
        seen_ids = {
            value for value, count in id_counts.items() if count > 1
        }
        errors = validate_customer(customer, seen_ids)
        if isinstance(customer_id, str) and id_counts.get(customer_id, 0) > 1:
            errors = [error for error in errors if not error.startswith("BR-09:")]
            errors.append("BR-09: duplicate customerId")

        if errors:
            quarantine_records.append(
                {
                    "source": source,
                    "transformed": customer,
                    "errors": errors,
                }
            )
        else:
            valid_records.append(customer)

    return {
        "transformed": valid_records,
        "quarantine": quarantine_records,
    }


def main() -> None:
    source_records = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    result = transform_records(source_records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
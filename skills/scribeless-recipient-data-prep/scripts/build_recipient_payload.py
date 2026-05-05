#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

STANDARD_FIELDS = {
    "title",
    "first_name",
    "last_name",
    "company",
    "address1",
    "address2",
    "address3",
    "city",
    "state",
    "postal_code",
    "country",
}

FIELD_ALIASES = {
    "firstname": "first_name",
    "first": "first_name",
    "givenname": "first_name",
    "lastname": "last_name",
    "last": "last_name",
    "surname": "last_name",
    "addressline1": "address1",
    "line1": "address1",
    "street": "address1",
    "addressline2": "address2",
    "line2": "address2",
    "addressline3": "address3",
    "line3": "address3",
    "postcode": "postal_code",
    "postalcode": "postal_code",
    "zip": "postal_code",
    "zipcode": "postal_code",
    "countrycode": "country",
}


def norm_key(value):
    return "".join(ch.lower() for ch in value if ch.isalnum())


def canonical_key(key):
    clean = norm_key(key)
    if key in STANDARD_FIELDS:
        return key
    return FIELD_ALIASES.get(clean, key)


def load_rows(path):
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        return data["data"]
    if isinstance(data, list):
        return data
    raise ValueError("JSON input must be an array or an object with a data array")


def clean(value):
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def convert_row(row, create_index):
    if not isinstance(row, dict):
        raise ValueError("Each recipient row must be an object")

    address_input = row.get("address") if isinstance(row.get("address"), dict) else {}
    normalized = {}
    variables = {}

    for key, value in row.items():
        if key == "address":
            continue
        canonical = canonical_key(key)
        if canonical in STANDARD_FIELDS:
            normalized[canonical] = clean(value)
        elif clean(value) is not None:
            variables[key] = clean(value)

    for key, value in address_input.items():
        canonical = canonical_key(key)
        if canonical in STANDARD_FIELDS:
            normalized[canonical] = clean(value)

    address = {
        "address1": normalized.get("address1"),
        "address2": normalized.get("address2"),
        "address3": normalized.get("address3"),
        "city": normalized.get("city"),
        "state": normalized.get("state"),
        "postal_code": normalized.get("postal_code"),
        "country": normalized.get("country"),
    }

    recipient = {
        "title": normalized.get("title"),
        "first_name": normalized.get("first_name"),
        "last_name": normalized.get("last_name"),
        "company": normalized.get("company"),
        "address": {key: value for key, value in address.items() if value is not None},
        "variables": variables,
        "createIndex": create_index,
    }

    return {key: value for key, value in recipient.items() if value is not None}


def main():
    parser = argparse.ArgumentParser(description="Build a Scribeless recipient creation payload.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = load_rows(args.input)
    payload = {
        "campaignId": args.campaign_id,
        "data": [convert_row(row, index) for index, row in enumerate(rows)],
    }

    output = json.dumps(payload, indent=2)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    raise SystemExit(main())

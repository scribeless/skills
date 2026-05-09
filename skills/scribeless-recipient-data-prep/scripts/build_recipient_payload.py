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
    "title": "title",
    "salutation": "title",
    "firstname": "first_name",
    "first": "first_name",
    "givenname": "first_name",
    "forename": "first_name",
    "lastname": "last_name",
    "last": "last_name",
    "surname": "last_name",
    "familyname": "last_name",
    "company": "company",
    "organisation": "company",
    "organization": "company",
    "business": "company",
    "address1": "address1",
    "addressaddress1": "address1",
    "addressline1": "address1",
    "line1": "address1",
    "street": "address1",
    "streetaddress": "address1",
    "address2": "address2",
    "addressaddress2": "address2",
    "addressline2": "address2",
    "line2": "address2",
    "unit": "address2",
    "apartment": "address2",
    "suite": "address2",
    "address3": "address3",
    "addressaddress3": "address3",
    "addressline3": "address3",
    "line3": "address3",
    "city": "city",
    "addresscity": "city",
    "town": "city",
    "locality": "city",
    "state": "state",
    "addressstate": "state",
    "province": "state",
    "county": "state",
    "region": "state",
    "postcode": "postal_code",
    "postalcode": "postal_code",
    "addresspostcode": "postal_code",
    "addresspostalcode": "postal_code",
    "zip": "postal_code",
    "zipcode": "postal_code",
    "country": "country",
    "addresscountry": "country",
    "countrycode": "country",
}

HTML_FIELD_ALIASES = {
    "htmlfront": "front",
    "fronthtml": "front",
    "variableshtmlfront": "front",
    "htmlback": "back",
    "backhtml": "back",
    "variableshtmlback": "back",
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


def clean_html(value):
    if isinstance(value, str):
        text = value.strip()
        return text if text else None
    return None


def merge_html_variable(variables, value):
    if not isinstance(value, dict):
        return

    html = variables.setdefault("html", {})
    for side in ("front", "back"):
        cleaned = clean_html(value.get(side))
        if cleaned is not None:
            html[side] = cleaned
    if not html:
        variables.pop("html", None)


def convert_row(row):
    if not isinstance(row, dict):
        raise ValueError("Each recipient row must be an object")

    address_input = row.get("address") if isinstance(row.get("address"), dict) else {}
    variables_input = row.get("variables") if isinstance(row.get("variables"), dict) else {}
    normalized = {}
    variables = {}

    for key, value in variables_input.items():
        if key == "html":
            merge_html_variable(variables, value)
        elif (cleaned := clean(value)) is not None:
            variables[key] = cleaned

    for key, value in row.items():
        if key in {"address", "variables"}:
            continue
        normalized_key = norm_key(key)
        html_side = HTML_FIELD_ALIASES.get(normalized_key)
        if html_side:
            html_value = clean_html(value)
            if html_value is not None:
                variables.setdefault("html", {})[html_side] = html_value
            continue

        canonical = canonical_key(key)
        if canonical in STANDARD_FIELDS:
            normalized[canonical] = clean(value)
        elif (cleaned := clean(value)) is not None and key not in variables:
            variables[key] = cleaned

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
        "postalCode": normalized.get("postal_code"),
        "country": normalized.get("country"),
    }

    recipient = {
        "title": normalized.get("title"),
        "firstName": normalized.get("first_name"),
        "lastName": normalized.get("last_name"),
        "company": normalized.get("company"),
        "address": {key: value for key, value in address.items() if value is not None},
        "variables": variables or None,
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
        "data": [convert_row(row) for row in rows],
    }

    output = json.dumps(payload, indent=2)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

STATE_REQUIRED_COUNTRIES = {"US", "CA", "AU"}


def norm_key(value):
    return "".join(ch.lower() for ch in value if ch.isalnum())


FIELD_SYNONYMS = {
    "title": {"title", "salutation"},
    "first_name": {"firstname", "first", "givenname", "forename"},
    "last_name": {"lastname", "last", "surname", "familyname"},
    "company": {"company", "organisation", "organization", "business"},
    "address1": {"address1", "addressline1", "line1", "street", "streetaddress"},
    "address2": {"address2", "addressline2", "line2", "unit", "apartment", "suite"},
    "address3": {"address3", "addressline3", "line3"},
    "city": {"city", "town", "locality"},
    "state": {"state", "province", "county", "region"},
    "postal_code": {"postalcode", "postcode", "zip", "zipcode"},
    "country": {"country", "countrycode"},
}


def load_rows(path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))

    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        return data["data"]
    if isinstance(data, list):
        return data
    raise ValueError("JSON input must be an array or an object with a data array")


def flatten_row(row):
    if not isinstance(row, dict):
        return {}
    address = row.get("address") if isinstance(row.get("address"), dict) else {}
    flat = {k: v for k, v in row.items() if k != "address"}
    for key, value in address.items():
        flat[f"address.{key}"] = value
        flat[key] = value
    return flat


def infer_mapping(headers):
    mapping = {}
    for header in headers:
        key = norm_key(header)
        for output, synonyms in FIELD_SYNONYMS.items():
            if key in synonyms:
                mapping[header] = output
                break
    return mapping


def mapped_value(row, mapping, output):
    for source, target in mapping.items():
        if target == output:
            value = row.get(source)
            if value is not None and str(value).strip():
                return str(value).strip()
    direct = row.get(output) or row.get(f"address.{output}")
    return str(direct).strip() if direct is not None else ""


def validate_row(row, mapping, row_number):
    issues = []
    first_name = mapped_value(row, mapping, "first_name")
    address1 = mapped_value(row, mapping, "address1")
    state = mapped_value(row, mapping, "state")
    postal_code = mapped_value(row, mapping, "postal_code")
    country = mapped_value(row, mapping, "country").upper()

    if not first_name:
        issues.append({"level": "error", "field": "first_name", "message": "First name is missing"})
    if not address1:
        issues.append({"level": "error", "field": "address.address1", "message": "Address line 1 is missing"})
    if address1 and len(address1) > 30:
        issues.append({"level": "warning", "field": "address.address1", "message": "Address line 1 is over 30 characters"})
    if not country:
        issues.append({"level": "error", "field": "address.country", "message": "Country is missing"})
    if country in STATE_REQUIRED_COUNTRIES and not state:
        issues.append({"level": "error", "field": "address.state", "message": f"State/province is required for {country}"})
    if not postal_code:
        issues.append({"level": "warning", "field": "address.postal_code", "message": "Postal code is missing"})

    return {"row": row_number, "issues": issues}


def build_report(path):
    raw_rows = load_rows(path)
    rows = [flatten_row(row) for row in raw_rows]
    headers = sorted({key for row in rows for key in row.keys()})
    mapping = infer_mapping(headers)
    results = [validate_row(row, mapping, index + 1) for index, row in enumerate(rows)]
    rows_with_issues = [result for result in results if result["issues"]]
    errors = sum(1 for result in results for issue in result["issues"] if issue["level"] == "error")
    warnings = sum(1 for result in results for issue in result["issues"] if issue["level"] == "warning")
    return {
        "input": str(path),
        "rowCount": len(rows),
        "validRows": len(rows) - sum(1 for result in rows_with_issues if any(issue["level"] == "error" for issue in result["issues"])),
        "errorCount": errors,
        "warningCount": warnings,
        "mapping": mapping,
        "rowsWithIssues": rows_with_issues,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate recipient data for Scribeless.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    report = build_report(args.input)
    output = json.dumps(report, indent=2)
    if args.report:
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if report["errorCount"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

MAX_HTML_BYTES = 250 * 1024
SUPPORTED_HTML_PRODUCT_KEYS = {
    "a5_postcard",
    "a6_postcard",
    "4x6_postcard",
    "5x7_postcard",
    "a5_card",
    "a6_card",
    "a4_letter",
    "4x6_card",
    "5x7_card",
    "7x10_letter",
}
STATE_REQUIRED_COUNTRIES = {"US", "CA", "AU"}

DISPLAY_FIELDS = {
    "first_name": "firstName",
    "last_name": "lastName",
    "postal_code": "address.postalCode",
    "address1": "address.address1",
    "address2": "address.address2",
    "address3": "address.address3",
    "city": "address.city",
    "state": "address.state",
    "country": "address.country",
    "title": "title",
    "company": "company",
}

HTML_FIELD_ALIASES = {
    "htmlfront": "front",
    "fronthtml": "front",
    "htmlback": "back",
    "backhtml": "back",
}


def norm_key(value):
    return "".join(ch.lower() for ch in value if ch.isalnum())


FIELD_SYNONYMS = {
    "title": {"title", "salutation"},
    "first_name": {"firstname", "first", "givenname", "forename"},
    "last_name": {"lastname", "last", "surname", "familyname"},
    "company": {"company", "organisation", "organization", "business"},
    "address1": {"address1", "addressaddress1", "addressline1", "line1", "street", "streetaddress"},
    "address2": {"address2", "addressaddress2", "addressline2", "line2", "unit", "apartment", "suite"},
    "address3": {"address3", "addressaddress3", "addressline3", "line3"},
    "city": {"city", "addresscity", "town", "locality"},
    "state": {"state", "addressstate", "province", "county", "region"},
    "postal_code": {"postalcode", "addresspostalcode", "postcode", "addresspostcode", "zip", "zipcode"},
    "country": {"country", "addresscountry", "countrycode"},
}


def load_rows(path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))

    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("data"), list):
        return data["data"]
    if isinstance(data, dict) and isinstance(data.get("data"), dict):
        row = dict(data["data"])
        for key in ("product_key", "include_envelope", "orientation", "html"):
            if key in data:
                row[key] = data[key]
        return [row]
    if isinstance(data, list):
        return data
    raise ValueError("JSON input must be an array or an object with a data array/object")


def flatten_row(row):
    if not isinstance(row, dict):
        return {}
    address = row.get("address") if isinstance(row.get("address"), dict) else {}
    endpoint_html = row.get("html") if isinstance(row.get("html"), dict) else None
    flat = {k: v for k, v in row.items() if k != "address"}
    for key, value in address.items():
        flat[f"address.{key}"] = value
        flat[key] = value
    if endpoint_html:
        for side, value in endpoint_html.items():
            if isinstance(value, dict) and "html" in value:
                flat[f"html.{side}.html"] = value["html"]
            else:
                flat[f"html.{side}"] = value
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
    city = mapped_value(row, mapping, "city")
    state = mapped_value(row, mapping, "state")
    postal_code = mapped_value(row, mapping, "postal_code")
    country = mapped_value(row, mapping, "country").upper()

    if not first_name:
        issues.append({"level": "error", "field": "firstName", "message": "First name is missing"})
    if not address1:
        issues.append({"level": "error", "field": "address.address1", "message": "Address line 1 is missing"})
    if address1 and len(address1) > 30:
        issues.append({"level": "warning", "field": "address.address1", "message": "Address line 1 is over 30 characters"})
    if not city:
        issues.append({"level": "error", "field": "address.city", "message": "City is missing"})
    if not country:
        issues.append({"level": "error", "field": "address.country", "message": "Country is missing"})
    if not state and country in STATE_REQUIRED_COUNTRIES:
        issues.append({"level": "error", "field": "address.state", "message": f"State/region is missing for {country}"})
    if not postal_code:
        issues.append({"level": "error", "field": "address.postalCode", "message": "Postal code is missing"})

    validate_html(row, issues)

    return {"row": row_number, "issues": issues}


def html_side_values(row):
    values = {}
    for key, value in row.items():
        if key == "html" or key.startswith("html."):
            continue
        side = HTML_FIELD_ALIASES.get(norm_key(key))
        if side:
            values[side] = value

    return values


def validate_html(row, issues):
    endpoint_html = row.get("html")
    if endpoint_html is not None:
        if not isinstance(endpoint_html, dict):
            issues.append({"level": "error", "field": "html", "message": "HTML recipient content must be an object with front/back side objects"})
        else:
            validate_endpoint_html(endpoint_html, issues)

    validate_html_endpoint_options(row, endpoint_html, issues)
    validate_variables_html(row, issues)

    values = html_side_values(row)
    for side in ("front", "back"):
        value = values.get(side)
        if value is None or value == "":
            continue
        if not isinstance(value, str):
            issues.append({"level": "error", "field": f"html.{side}.html", "message": "HTML side must be a string"})
            continue
        if len(value.encode("utf-8")) > MAX_HTML_BYTES:
            issues.append({"level": "error", "field": f"html.{side}.html", "message": "HTML side is over 250 KB"})


def validate_html_endpoint_options(row, endpoint_html, issues):
    if endpoint_html is None:
        return

    product_key = row.get("product_key")
    if not product_key:
        issues.append({"level": "error", "field": "product_key", "message": "Product key is required for HTML recipient rendering"})
    elif product_key not in SUPPORTED_HTML_PRODUCT_KEYS:
        issues.append({"level": "error", "field": "product_key", "message": "Product key is not supported for HTML recipient rendering"})

    orientation = row.get("orientation")
    if orientation is not None and orientation not in {"landscape", "portrait"}:
        issues.append({"level": "error", "field": "orientation", "message": "Orientation must be landscape or portrait"})

    include_envelope = row.get("include_envelope")
    if include_envelope is not None and not isinstance(include_envelope, bool):
        issues.append({"level": "error", "field": "include_envelope", "message": "include_envelope must be a boolean"})


def validate_variables_html(row, issues):
    variables = row.get("variables")
    if isinstance(variables, dict) and "html" in variables:
        issues.append({"level": "error", "field": "data.variables.html", "message": "Custom HTML creative belongs in top-level html, not data.variables.html"})


def validate_endpoint_html(html, issues):
    if "front" not in html:
        issues.append({"level": "error", "field": "html.front", "message": "html.front is required for HTML recipient rendering"})

    for side in ("front", "back"):
        value = html.get(side)
        if value is None:
            continue
        if not isinstance(value, dict):
            issues.append({"level": "error", "field": f"html.{side}", "message": "HTML side must be an object with an html string"})
            continue
        html_string = value.get("html")
        if not isinstance(html_string, str) or not html_string.strip():
            issues.append({"level": "error", "field": f"html.{side}.html", "message": "HTML side must include a non-empty html string"})
            continue
        if len(html_string.encode("utf-8")) > MAX_HTML_BYTES:
            issues.append({"level": "error", "field": f"html.{side}.html", "message": "HTML side is over 250 KB"})


def format_mapping(mapping):
    return {source: DISPLAY_FIELDS.get(target, target) for source, target in mapping.items()}


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
        "mapping": format_mapping(mapping),
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

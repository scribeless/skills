---
name: scribeless-recipient-data-prep
description: Clean and validate recipient CSV or JSON data for Scribeless uploads and API calls. Use when a user needs to map spreadsheet columns to Scribeless recipient fields, detect missing names or postal addresses, normalize country/state/postcode fields, keep personalization variables, build POST /api/recipients payloads, or produce a validation report before uploading recipients.
---

# Scribeless Recipient Data Prep

## Workflow

1. Inspect the input format:
   - CSV spreadsheet
   - raw JSON array
   - existing Scribeless API payload with `campaignId` and `data`
2. Map standard fields:
   - `title`
   - `first_name`
   - `last_name`
   - `company`
   - `address.address1`
   - `address.address2`
   - `address.address3`
   - `address.city`
   - `address.state`
   - `address.postal_code`
   - `address.country`
3. Preserve unrecognized business fields as `variables`.
4. Validate:
   - first name present
   - address line 1 present
   - country present
   - state present for state-sensitive countries when known
   - postcode present
   - address line 1 preferably no longer than 30 characters
5. Return a concise report:
   - valid count
   - warning/error count
   - rows requiring user attention
   - suggested column mapping
6. Build payloads only when the user provides or confirms the campaign ID.

## Scripts

Validate a CSV or JSON file:

```bash
python3 scripts/validate_recipients.py recipients.csv --report report.json
```

Build a Scribeless API payload:

```bash
python3 scripts/build_recipient_payload.py recipients.csv --campaign-id CAMPAIGN_ID --output payload.json
```

## Payload Guidance

Prefer the public API shape:

```json
{
  "campaignId": "CAMPAIGN_ID",
  "data": [
    {
      "first_name": "Ada",
      "last_name": "Lovelace",
      "company": "Example Co",
      "address": {
        "address1": "123 Example St",
        "city": "Bristol",
        "postal_code": "BS1 1AA",
        "country": "GB"
      },
      "variables": {
        "plan": "VIP"
      }
    }
  ]
}
```

## Rules

- Do not discard unknown columns; put them under `variables` unless they are empty.
- Do not fabricate missing addresses.
- Do not send live API requests unless explicitly asked after payload review.
- If a country, state, or postcode is ambiguous, flag it rather than guessing.

## References

- Use `references/recipient-fields.md` for field mapping and warning rules.

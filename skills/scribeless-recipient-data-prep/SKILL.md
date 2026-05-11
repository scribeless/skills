---
name: scribeless-recipient-data-prep
description: Clean and validate recipient CSV or JSON data for Scribeless uploads and API calls. Use when a user needs to map spreadsheet columns to Scribeless recipient fields, detect missing names or postal addresses, normalize country/state/postcode fields, keep personalization variables, build POST /api/recipients payloads, validate POST /api/recipients/html data, or produce a validation report before uploading recipients.
---

# Scribeless Recipient Data Prep

## Workflow

1. Inspect the input format:
   - CSV spreadsheet
   - raw JSON array
   - existing Scribeless API payload with `campaignId` and `data`
   - custom HTML recipient payload with `product_key`, `html`, and `data`
2. Map input columns to public Scribeless API fields:
   - `title`
   - `firstName`
   - `lastName`
   - `company`
   - `address.address1`
   - `address.address2`
   - `address.address3`
   - `address.city`
   - `address.state`
   - `address.postalCode`
   - `address.country`
3. Preserve unrecognized business fields as `variables`.
   - For `POST /api/recipients/html`, keep generated creative in the top-level `html.front` and/or `html.back` objects.
   - Keep custom recipient values inside `data.variables`.
4. Validate:
   - first name present
   - address line 1 present
   - city present
   - state/region present when required for the destination country
   - country present
   - postcode present
   - address line 1 preferably no longer than 30 characters
   - HTML front/back `html` values, when present, are strings no larger than 250 KB each
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

Prefer the standard campaign recipient API shape:

```json
{
  "campaignId": "CAMPAIGN_ID",
  "data": [
    {
      "firstName": "Ada",
      "lastName": "Lovelace",
      "company": "Example Co",
      "address": {
        "address1": "123 Example St",
        "city": "Bristol",
        "state": "Bristol",
        "postalCode": "BS1 1AA",
        "country": "GB"
      },
      "variables": {
        "plan": "VIP"
      }
    }
  ]
}
```

For custom HTML recipient rendering, validate the `data` object, top-level `html` object, `product_key`, `include_envelope`, and `orientation` used by `POST /api/recipients/html`.

## Rules

- Do not discard unknown columns; put them under `variables` unless they are empty.
- Use the public API field names in generated payloads: `firstName`, `lastName`, and `address.postalCode`.
- For custom HTML recipient rendering, do not put HTML creative inside `data.variables`; use the endpoint's top-level `html.front` and/or `html.back` objects.
- Do not fabricate missing addresses.
- Do not send live API requests unless explicitly asked after payload review.
- If a country, state, or postcode is ambiguous, flag it rather than guessing.

## Support

- Help Center: `https://help.scribeless.co/en/`
- API documentation: `https://docs.scribeless.co/`
- For integration issues, ask the user to contact Scribeless through live chat or `team@scribeless.co`.

## References

- Use `references/recipient-fields.md` for field mapping and warning rules.

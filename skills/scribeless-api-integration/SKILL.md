---
name: scribeless-api-integration
description: Build public Scribeless API and automation workflows for creating recipients, connecting Zapier, Make, Pipedream, n8n, CRM, ecommerce, warehouse, product analytics, and custom app triggers to Scribeless campaigns. Use when a user needs API authentication guidance, X-API-Key examples, POST /api/recipients payloads, error handling, webhook-to-recipient mapping, or implementation review.
---

# Scribeless API Integration

## Workflow

1. Identify the source system:
   - CRM, ecommerce store, product analytics, warehouse, form, event tool, or custom app
2. Identify the trigger:
   - order created, deal stage changed, demo booked, form submitted, customer milestone, QR scan, or scheduled list sync
3. Confirm the Scribeless destination:
   - existing campaign ID
   - recipient data fields
   - template variables required by the campaign
4. Build mapping:
   - source contact/customer fields to recipient fields
   - source event fields to `variables`
   - suppression rules and deduplication strategy
5. Produce an example:
   - curl
   - JavaScript/TypeScript fetch
   - Zapier/Make step outline when relevant
6. Review safety:
   - do not expose API keys
   - do not send live requests unless the user confirms
   - include retry/backoff guidance for transient failures

## API Basics

- Base endpoint for recipient creation: `https://platform.scribeless.co/api/recipients`
- Authentication header: `X-API-Key`
- API keys are created in platform settings.
- Campaigns should already exist before sending recipients through the API.

## Example Payload

```json
{
  "campaignId": "CAMPAIGN_ID",
  "data": {
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
}
```

## Error Guidance

- `401`: missing, malformed, or invalid API key.
- `400`: payload validation issue; inspect required fields and variable shape.
- `503`: unexpected traffic spike or temporary service issue; retry after a short delay.

## References

- Use `references/api-workflows.md` for examples and connector outlines.

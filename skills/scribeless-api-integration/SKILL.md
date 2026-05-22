---
name: scribeless-api-integration
description: Build public Scribeless API and automation workflows for creating recipients, including custom HTML recipient rendering. Use when a user needs API authentication guidance, X-API-Key examples, POST /api/recipients payloads, POST /api/recipients/html payloads, product_key selection, HTML front/back rendering, Zapier/Make/Pipedream/n8n/CRM/ecommerce mappings, error handling, webhook-to-recipient mapping, or implementation review.
---

# Scribeless API Integration

## Workflow

1. Identify the source system:
   - CRM, ecommerce store, product analytics, warehouse, form, event tool, AI agent, data pipeline, server-side automation, or custom app
2. Identify the trigger:
   - order created, deal stage changed, demo booked, form submitted, customer milestone, QR scan, agent-approved send, or scheduled list sync
3. Confirm the Scribeless destination:
   - existing campaign ID for standard campaign recipients
   - `product_key` for custom HTML recipient rendering
   - recipient data fields
   - template variables required by the campaign
4. Build mapping:
   - source contact/customer fields to recipient fields
   - source event fields to `variables`
   - generated HTML to `/api/recipients/html` `html.front`, with optional `html.back`
   - source record IDs and run IDs for audit/dedupe
   - suppression rules and deduplication strategy
5. Produce an example:
   - curl
   - JavaScript/TypeScript fetch
   - Zapier/Make step outline when relevant
6. Review safety:
   - do not expose API keys
   - do not send live requests unless the user confirms
   - test standard campaign recipients against a Pending recurring campaign before activating it
   - review custom HTML rendered documents before using them in a live workflow
   - show returned preview `signed_url` images to the user when validating an HTML recipient render
   - include retry/backoff guidance for transient failures

## API Basics

- Base endpoint for campaign recipient creation: `https://platform.scribeless.co/api/recipients`
- Base endpoint for custom HTML recipient rendering: `https://platform.scribeless.co/api/recipients/html`
- Authentication header: `X-API-Key`
- API keys are created in platform settings.
- For `POST /api/recipients`, campaigns should already exist before sending recipients through the API.
- Send standard recipients to a recurring campaign while it is still Pending for test previews; after activation, new API recipients may be processed and charged.
- Custom HTML recipient rendering uses `product_key`, `include_envelope`, `orientation`, `html`, and `data`.
- Product keys identify supported postcard, flat card/note, and letter formats for HTML rendering.

## Example Payload

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
        "plan": "VIP",
        "source": "demo"
      }
    }
  ]
}
```

## HTML Recipient Rules

- Use the `POST /api/recipients/html` endpoint for custom HTML recipients.
- `product_key` must match a supported product key.
- `orientation` can be `landscape` or `portrait`.
- `html.front` is required for non-envelope products. `html.back` can be included for duplex/front-and-back output.
- Add Smart QR placeholders with an empty `div data-sqr` when the HTML should render a tracked QR code.
- Give each QR slot on the same side a unique `data-sqr-id`, a `data-sqr-destination`, and a stable CSS size.
- After a successful HTML recipient request, surface any returned `documents` with `format: "preview"` and `signed_url` so the user can inspect the rendered output.
- Use self-contained HTML in each side's `html` value; JavaScript is disabled during rendering.
- Do not rely on external stylesheets, scripts, fetch/XHR, iframes, or other network resources.
- Inline `data:image/*` images are allowed.
- External images must be HTTPS, publicly reachable, and must not redirect to another URL.
- Use standard web font hosting only when it is supported by the renderer; avoid depending on custom font requests unless they have been tested in rendered output.
- Keep HTML payloads deterministic and product-sized; content is rendered inside a clipped mail-piece container.

## Error Guidance

- `401`: missing, malformed, or invalid API key.
- `400`: payload validation issue; inspect required fields and variable shape.
- `503`: unexpected traffic spike or temporary service issue; retry after a short delay.

## Support

- Help Center: `https://help.scribeless.co/en/`
- API documentation: `https://docs.scribeless.co/`
- For API or automation issues, ask the user to contact Scribeless through live chat or `team@scribeless.co`.

## References

- Use `references/api-workflows.md` for examples and connector outlines.
- Use `references/html-recipient-api.md` for HTML recipient product keys and request/response examples.

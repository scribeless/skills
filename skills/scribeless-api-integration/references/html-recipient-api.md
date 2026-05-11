# HTML Recipient API

Use this endpoint when a workflow generates the recipient's mail-piece HTML and wants Scribeless to render the recipient documents.

## Product Keys

| Product | Product key | Region/standard | Notes |
| --- | --- | --- | --- |
| A5 postcard | `a5_postcard` | ISO / UK-friendly | Postcard |
| A6 postcard | `a6_postcard` | ISO / UK-friendly | Postcard |
| 4x6 postcard | `4x6_postcard` | US | Postcard |
| 5x7 postcard | `5x7_postcard` | US | Postcard |
| A5 card | `a5_card` | ISO / UK-friendly | Flat card/note, can include envelope |
| A6 card | `a6_card` | ISO / UK-friendly | Flat card/note, can include envelope |
| A4 letter | `a4_letter` | ISO / UK-friendly | Letter, can include envelope |
| 4x6 card | `4x6_card` | US | Flat card/note, can include envelope |
| 5x7 card | `5x7_card` | US | Flat card/note, can include envelope |
| 7x10 letter | `7x10_letter` | US | Letter, can include envelope |

## Request

```bash
curl -X POST "https://platform.scribeless.co/api/recipients/html" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: API_KEY_HERE" \
  -d '{
    "product_key": "a6_postcard",
    "include_envelope": false,
    "orientation": "landscape",
    "html": {
      "front": {
        "styles": {
          "backgroundColor": "#ffffff",
          "color": "#111827",
          "fontFamily": "Arial, sans-serif"
        },
        "html": "<main style=\"padding:24px;font-size:18px\"><h1>Hello {{ first_name }}</h1><p>Thanks for trying Scribeless.</p></main>"
      }
    },
    "data": {
      "first_name": "Jane",
      "last_name": "Doe",
      "address": {
        "address1": "221B Baker Street",
        "city": "London",
        "postal_code": "NW1 6XE",
        "country": "GB"
      },
      "variables": {
        "externalId": "customer-123",
        "customMessage": "Thanks again"
      }
    }
  }'
```

## Notes

- `product_key` must match one of the supported product keys.
- `include_envelope` controls whether to render and include an envelope document with the recipient.
- `orientation` can be `landscape` or `portrait`.
- `html.front` is required for non-envelope products.
- `html.back` can be included for duplex/front-and-back output.
- `data` is the recipient payload.
- Use `data.variables` for custom values available for merge/personalization.

## Example Response

```json
{
  "recipient": {
    "id": "11111111-1111-4111-8111-111111111111",
    "first_name": "Jane",
    "last_name": "Doe",
    "address1": "221B Baker Street",
    "city": "London",
    "postal_code": "NW1 6XE",
    "country": "GB",
    "status": "ready",
    "is_rendered": true,
    "variables": {
      "externalId": "customer-123",
      "customMessage": "Thanks again",
      "html": {
        "front": {
          "styles": {
            "backgroundColor": "#ffffff",
            "color": "#111827",
            "fontFamily": "Arial, sans-serif"
          },
          "html": "<main style=\"padding:24px;font-size:18px\"><h1>Hello {{ first_name }}</h1><p>Thanks for trying Scribeless.</p></main>"
        }
      }
    }
  },
  "documents": [
    {
      "id": "22222222-2222-4222-8222-222222222222",
      "format": "pdf",
      "type": "postcard",
      "src": "teams/team-id/campaigns/campaign-id/recipients/recipient-id/postcard.pdf",
      "signed_url": "SIGNED_DOCUMENT_URL"
    },
    {
      "id": "33333333-3333-4333-8333-333333333333",
      "format": "preview",
      "type": "postcard",
      "src": "teams/team-id/campaigns/campaign-id/recipients/recipient-id/postcard-1.png",
      "signed_url": "SIGNED_PREVIEW_URL"
    }
  ]
}
```

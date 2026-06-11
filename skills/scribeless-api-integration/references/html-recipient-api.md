# HTML Recipient API

Use this endpoint when a workflow generates the recipient's mail-piece HTML and wants Scribeless to render the recipient documents. It supports postcards, flat cards/notes, and letters.

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
        "html": "<main style=\"padding:24px;font-size:18px\"><h1>Hello {{ first_name }}</h1><p>Thanks for trying Scribeless.</p><div data-sqr data-sqr-id=\"booking-link\" data-sqr-destination=\"https://example.com/book\" data-sqr-size=\"24mm\" style=\"width:24mm;height:24mm\"></div></main>"
      }
    },
    "data": {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com",
      "domain": "example.com",
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
- Send `data.email` and `data.domain` as first-class fields when available. Scribeless uses them for analytics and attribution.
- Use `data.variables` for custom values available for merge/personalization.

## Billing and Checkout

HTML recipients follow the team's billing setup.

- If the team is on a subscription, successful HTML recipients move straight to `ready` and do not need checkout.
- If the team is using one-time billing, successful HTML recipients can remain `pending` until they are paid for.
- For one-time billing, fetch the active cart and checkout the cart before treating the recipients as ready for fulfilment.

```bash
curl "https://platform.scribeless.co/api/carts/active" \
  -H "X-API-Key: API_KEY_HERE"
```

```bash
curl -X POST "https://platform.scribeless.co/api/recipients/checkout" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: API_KEY_HERE" \
  -d '{
    "cartId": "CART_ID"
  }'
```

Checkout may return a checkout or invoice URL when payment cannot be collected automatically. Recipients are not processed until payment is complete.

## Smart QR Placeholders

Add an empty `div` with the `data-sqr` marker when the rendered HTML should include a tracked Smart QR code.

```html
<div
  data-sqr
  data-sqr-id="booking-link"
  data-sqr-destination="https://example.com/book"
  data-sqr-size="24mm"
  style="width:24mm;height:24mm"
></div>
```

- `data-sqr-id` identifies the QR slot in the HTML. Use a unique value for each QR placeholder on the same side.
- `data-sqr-destination` is the URL the QR code should send recipients to.
- `data-sqr-size` controls the generated QR image size. CSS `width` and `height` are recommended so the layout reserves the right space before rendering.
- The placeholder must be an explicitly closed `div` and should not contain child elements.

## Example Response

The returned recipient `status` depends on the team's billing setup. Teams on a subscription return `ready`; one-time billing can return `pending` until checkout is complete.

```json
{
  "recipient": {
    "id": "11111111-1111-4111-8111-111111111111",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "domain": "example.com",
    "address1": "221B Baker Street",
    "city": "London",
    "postal_code": "NW1 6XE",
    "country": "GB",
    "status": "ready",
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
          "html": "<main style=\"padding:24px;font-size:18px\"><h1>Hello {{ first_name }}</h1><p>Thanks for trying Scribeless.</p><div data-sqr data-sqr-id=\"booking-link\" data-sqr-destination=\"https://example.com/book\" data-sqr-size=\"24mm\" style=\"width:24mm;height:24mm\"></div></main>"
        }
      }
    }
  },
  "documents": [
    {
      "id": "22222222-2222-4222-8222-222222222222",
      "format": "pdf",
      "type": "postcard",
      "src": "DOCUMENT_STORAGE_PATH",
      "signed_url": "SIGNED_DOCUMENT_URL"
    },
    {
      "id": "33333333-3333-4333-8333-333333333333",
      "format": "preview",
      "type": "postcard",
      "src": "PREVIEW_STORAGE_PATH",
      "signed_url": "SIGNED_PREVIEW_URL"
    }
  ]
}
```

When validating an HTML recipient render for a user, show the returned preview image URLs (`documents` where `format` is `preview`) so they can inspect the rendered output before sending live traffic.

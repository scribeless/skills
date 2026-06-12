# API Workflows

## curl

```bash
curl --location 'https://platform.scribeless.co/api/recipients' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --data '{
    "campaignId": "CAMPAIGN_ID",
    "data": [
      {
        "firstName": "Ada",
        "lastName": "Lovelace",
        "email": "ada@example.com",
        "domain": "example.com",
        "address": {
          "address1": "123 Example St",
          "city": "Bristol",
          "state": "Bristol",
          "postalCode": "BS1 1AA",
          "country": "GB"
        },
        "variables": {
          "source": "demo"
        }
      }
    ]
  }'
```

## JavaScript Fetch

```js
const response = await fetch('https://platform.scribeless.co/api/recipients', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.SCRIBELESS_API_KEY,
  },
  body: JSON.stringify({
    campaignId: 'CAMPAIGN_ID',
    data: [{
      firstName: 'Ada',
      lastName: 'Lovelace',
      email: 'ada@example.com',
      domain: 'example.com',
      address: {
        address1: '123 Example St',
        city: 'Bristol',
        state: 'Bristol',
        postalCode: 'BS1 1AA',
        country: 'GB',
      },
      variables: {
        source: 'demo',
      },
    }],
  }),
})

if (!response.ok) {
  throw new Error(`Scribeless request failed: ${response.status} ${await response.text()}`)
}
```

## Standard Campaign State

For standard `/api/recipients` requests, use a Pending recurring campaign for tests so recipients generate previews without being mailed or charged. Activate the campaign only after the mapping, variables, and previews are correct.

## Email and Domain Attribution

When the source system has a recipient email address, company domain, store domain, or account domain, map those values to top-level `email` and `domain` recipient fields. Do not put email addresses or domains in `variables` unless they are also needed as template merge fields. Scribeless stores `email` and `domain` separately for analytics and attribution.

## Billing and Checkout

Before considering an API workflow complete, confirm the billing path for the account and campaign.

- For teams on a subscription, recipients process automatically.
- One-time campaign or HTML recipient usage may require checkout before fulfilment starts.
- For one-time campaign recipients, checkout with `POST /api/recipients/checkout` using `campaignId` or `campaignIds`.
- For one-time HTML recipients, fetch the active cart with `GET /api/carts/active`, then checkout with `POST /api/recipients/checkout` using the returned `cartId`.
- If checkout returns a payment URL, surface it to the user and do not describe the recipients as ready for fulfilment until payment is complete.

## Custom HTML Recipient Endpoint

Use `POST https://platform.scribeless.co/api/recipients/html` when the source system generates the complete mail-piece artwork as HTML. This endpoint uses product keys for postcards, flat cards/notes, and letters.

```json
{
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
}
```

Rules for generated HTML:

- `product_key` must match a supported product key.
- `orientation` can be `landscape` or `portrait`.
- `html.front` is required for non-envelope products.
- `html.back` can be included for duplex/front-and-back output.
- Use an empty `div data-sqr` placeholder for tracked Smart QR codes.
- JavaScript is disabled.
- Do not use external CSS, scripts, fetch/XHR, iframes, or form actions.
- Inline `data:image/*` URLs are allowed.
- External images must be HTTPS public URLs and must not redirect.
- Avoid depending on custom web fonts unless they have been tested in rendered output.

## Zapier or Make Outline

1. Trigger from the source app.
2. Add optional filter to suppress incomplete postal addresses.
3. Add optional delay if the mail should arrive after a milestone.
4. Add a webhook/custom request step.
5. Send `POST https://platform.scribeless.co/api/recipients`.
6. Include `X-API-Key`.
7. Map contact fields to recipient fields.
8. Map email/domain values to top-level `email` and `domain`.
9. Map extra personalization fields to `variables`.
10. For full custom layouts, use `POST /api/recipients/html` and map generated HTML to `html.front` and optional `html.back`.
11. If the resulting recipients need one-time payment, checkout the active cart before fulfilment.
12. Test with one non-sensitive recipient before turning on.

## Review Checklist

- Campaign ID is correct for standard `/api/recipients` workflows.
- Product key, envelope setting, and orientation are correct for `/api/recipients/html` workflows.
- API key is stored in the automation platform's secure credential field.
- Required recipient fields are present.
- Variables match the Scribeless template.
- Email and domain values use top-level `email` and `domain` fields for analytics and attribution.
- HTML content, when present, uses the custom HTML recipient endpoint and respects render limits.
- Returned HTML recipient preview `signed_url` images have been shown to the user for visual review.
- Billing path is understood: recipients on a subscription process automatically; one-time recipients may need checkout first.
- Duplicate prevention is handled in the source system or automation flow.
- First standard campaign test sends go to a Pending recurring campaign.
- Custom HTML render outputs are reviewed before live use.

## Support

- Help Center: `https://help.scribeless.co/en/`
- API documentation: `https://docs.scribeless.co/`
- For API integration issues, use live chat in the Scribeless platform or contact `team@scribeless.co`.

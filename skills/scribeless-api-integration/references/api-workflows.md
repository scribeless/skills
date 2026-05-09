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

## Custom HTML Recipient Endpoint

Use `POST https://platform.scribeless.co/api/recipients/html` when the source system generates the complete front and/or back artwork as HTML. This endpoint uses product keys rather than an existing campaign ID.

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
8. Map extra personalization fields to `variables`.
9. For full custom layouts, use `POST /api/recipients/html` and map generated HTML to `html.front` and/or `html.back`.
10. Test with one non-sensitive recipient before turning on.

## Review Checklist

- Campaign ID is correct for standard `/api/recipients` workflows.
- Product key, envelope setting, and orientation are correct for `/api/recipients/html` workflows.
- API key is stored in the automation platform's secure credential field.
- Required recipient fields are present.
- Variables match the Scribeless template.
- HTML content, when present, uses the custom HTML recipient endpoint and respects render limits.
- Duplicate prevention is handled in the source system or automation flow.
- First standard campaign test sends go to a Pending recurring campaign.
- Custom HTML render outputs are reviewed before live use.

## Support

- Help Center: `https://help.scribeless.co/en/`
- API documentation: `https://docs.scribeless.co/`
- For API integration issues, use live chat in the Scribeless platform or contact `team@scribeless.co`.

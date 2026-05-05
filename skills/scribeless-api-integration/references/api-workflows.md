# API Workflows

## curl

```bash
curl --location 'https://platform.scribeless.co/api/recipients' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: YOUR_API_KEY' \
  --data '{
    "campaignId": "CAMPAIGN_ID",
    "data": {
      "first_name": "Ada",
      "last_name": "Lovelace",
      "address": {
        "address1": "123 Example St",
        "city": "Bristol",
        "postal_code": "BS1 1AA",
        "country": "GB"
      },
      "variables": {
        "source": "demo"
      }
    }
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
      first_name: 'Ada',
      last_name: 'Lovelace',
      address: {
        address1: '123 Example St',
        city: 'Bristol',
        postal_code: 'BS1 1AA',
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

## Zapier or Make Outline

1. Trigger from the source app.
2. Add optional filter to suppress incomplete postal addresses.
3. Add optional delay if the mail should arrive after a milestone.
4. Add a webhook/custom request step.
5. Send `POST https://platform.scribeless.co/api/recipients`.
6. Include `X-API-Key`.
7. Map contact fields to recipient fields.
8. Map extra personalization fields to `variables`.
9. Test with one non-sensitive recipient before turning on.

## Review Checklist

- Campaign ID is correct.
- API key is stored in the automation platform's secure credential field.
- Required recipient fields are present.
- Variables match the Scribeless template.
- Duplicate prevention is handled in the source system or automation flow.

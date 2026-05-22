# Recipient Fields

## Standard Fields

Use these output fields for Scribeless payloads:

| Output field | Notes |
| --- | --- |
| `title` | Optional salutation or title |
| `firstName` | Required for most handwritten messages |
| `lastName` | Optional |
| `company` | Optional |
| `address.address1` | Required postal line |
| `address.address2` | Optional |
| `address.address3` | Optional |
| `address.city` | Required for reliable delivery |
| `address.state` | Required when state/province is part of the destination country's postal routing, such as US, CA, or AU |
| `address.postalCode` | Required for reliable delivery |
| `address.country` | Country value accepted by Scribeless, such as `US`, `GB`, `CA`, `AU`, or full country names shown in platform examples |
| `variables` | Personalization fields not part of the address |
| `html.front.html` | Required top-level custom HTML for `POST /api/recipients/html` front side |
| `html.back.html` | Optional top-level custom HTML for `POST /api/recipients/html` back side |

## Common Column Synonyms

- first name: `first_name`, `firstName`, `first`, `given_name`, `forename`
- last name: `last_name`, `lastName`, `last`, `surname`, `family_name`
- address1: `address1`, `address_1`, `address line 1`, `line1`, `street`
- address2: `address2`, `address_2`, `address line 2`, `line2`, `unit`, `apartment`
- city: `city`, `town`, `locality`
- state: `state`, `province`, `county`, `region`
- postal code: `postal_code`, `postalCode`, `postcode`, `zip`, `zip_code`
- country: `country`, `country_code`, `countryCode`
- HTML front: `html_front`, `htmlFront`, `front_html`, `html.front.html`
- HTML back: `html_back`, `htmlBack`, `back_html`, `html.back.html`

## Warning Rules

- Missing `firstName`: action required unless the template does not use names.
- Missing `address.address1`: action required.
- Missing `address.city`: action required.
- Missing `address.country`: action required.
- Missing `address.postalCode`: action required for most campaigns.
- Missing `address.state`: action required for countries that need state/province routing, such as US, CA, or AU.
- `address.address1` longer than 30 characters: split into address2/address3 where possible.
- `html.front` or `html.back` as a plain string: action required; each side must be an object with an `html` string.
- `html.front.html` or `html.back.html` over 250 KB: action required.

## Variables

Variables should use stable keys with no spaces when possible:

- good: `last_purchase`, `account_owner`, `renewal_date`
- avoid: `Last Purchase Date`, `owner email?`

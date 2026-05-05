# Recipient Fields

## Standard Fields

Use these output fields for Scribeless payloads:

| Output field | Notes |
| --- | --- |
| `title` | Optional salutation or title |
| `first_name` | Required for most handwritten messages |
| `last_name` | Optional |
| `company` | Optional |
| `address.address1` | Required postal line |
| `address.address2` | Optional |
| `address.address3` | Optional |
| `address.city` | Recommended |
| `address.state` | Required for some countries and useful for routing |
| `address.postal_code` | Required for reliable delivery |
| `address.country` | Prefer ISO 3166-1 alpha-2 code, such as `US`, `GB`, `CA`, `AU` |
| `variables` | Personalization fields not part of the address |

## Common Column Synonyms

- first name: `first_name`, `firstName`, `first`, `given_name`, `forename`
- last name: `last_name`, `lastName`, `last`, `surname`, `family_name`
- address1: `address1`, `address_1`, `address line 1`, `line1`, `street`
- address2: `address2`, `address_2`, `address line 2`, `line2`, `unit`, `apartment`
- city: `city`, `town`, `locality`
- state: `state`, `province`, `county`, `region`
- postal code: `postal_code`, `postalCode`, `postcode`, `zip`, `zip_code`
- country: `country`, `country_code`, `countryCode`

## Warning Rules

- Missing `first_name`: action required unless the template does not use names.
- Missing `address.address1`: action required.
- Missing `address.country`: action required.
- Missing `address.postal_code`: action required for most campaigns.
- Missing `address.state`: action required for countries where state/province is part of postal routing.
- `address.address1` longer than 30 characters: split into address2/address3 where possible.

## Variables

Variables should use stable keys with no spaces when possible:

- good: `last_purchase`, `account_owner`, `renewal_date`
- avoid: `Last Purchase Date`, `owner email?`

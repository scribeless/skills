---
name: scribeless-campaign-planner
description: Plan Scribeless handwritten direct mail campaigns for customer retention, acquisition, ABM, real estate, financial services, nonprofit, home services, ecommerce, and other business use cases. Use when a user wants help choosing a campaign audience, message, product, delivery method, personalization variables, Smart QR tracking, or campaign success criteria before building in Scribeless.
---

# Scribeless Campaign Planner

## Workflow

1. Clarify the campaign goal:
   - retention, winback, loyalty, VIP moment, lead generation, ABM, referral, onboarding, renewal, donation, event follow-up, or gift follow-up
   - primary conversion event and expected next action
2. Define audience and trigger:
   - customer segment, CRM/ecommerce event, list source, suppression rules, and timing
   - require enough data for recipient name and postal address
3. Choose Scribeless setup:
   - one-off campaign for a fixed list
   - recurring campaign or integration/API workflow for ongoing triggers
   - direct mail for sending with local stamp
   - bulk shipping when cards should go to one address for redistribution
4. Choose creative:
   - product type: flat card, folded card, letter, postcard, envelope-only, or gift campaign
   - personalization variables: first name, company, purchase, lifecycle stage, sender, QR destination
   - optional Smart QR code when measurement or digital follow-up matters
5. Produce a campaign brief:
   - goal, audience, trigger, offer/CTA, template direction, variables, data source, delivery method, timing, measurement, and risks
6. If the user wants implementation guidance, hand off to:
   - `$scribeless-template-writer` for copy
   - `$scribeless-recipient-data-prep` for list cleanup
   - `$scribeless-platform-guide` for UI steps
   - `$scribeless-api-integration` for automation/API setup

## Decision Rules

- Prefer practical direct-response copy over brand-heavy prose.
- Recommend Smart QR codes only when there is a clear digital action or attribution need.
- For account-based campaigns, prioritize low-volume high-personalization.
- For ecommerce retention, prioritize timely lifecycle events and concrete purchase context.
- For regulated or sensitive categories, flag that the user should review copy internally before sending.
- Do not claim exact uplift, open rate, delivery time, price, or availability unless the user provides current source material.

## Output Shape

Use this structure:

```markdown
## Campaign Brief
- Goal:
- Audience:
- Trigger/source:
- Product:
- Delivery method:
- Message angle:
- Variables:
- QR/CTA:
- Timing:
- Measurement:
- Setup path:
- Risks/checks:
```

## References

- Use `references/campaign-playbooks.md` for common industry and lifecycle playbooks.

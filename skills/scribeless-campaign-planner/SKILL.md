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
   - API-led agent workflow when an AI system will generate recipients, variables, or HTML artifacts
   - direct mail for sending with local stamp
   - bulk shipping when cards should go to one address for redistribution
4. Choose creative:
   - product type: flat card, folded card, letter, postcard, envelope-only, or gift campaign
   - personalization variables: first name, company, purchase, lifecycle stage, sender, QR destination
   - optional API-provided HTML when the campaign needs fully custom, code-generated front/back artwork
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
- For regulated or sensitive categories, flag that the user's team should review copy before sending.
- For standard campaign integrations, plan tests against a Pending recurring campaign before activation; after activation, new recipients may be produced and charged.
- For custom HTML recipient rendering, confirm the supported product key, envelope setting, and orientation before implementation.
- Use API-provided HTML only when the source system can generate complete, product-sized artwork; use normal templates when the user mainly needs copy, variables, and standard layout control.
- Do not recommend folded card products for API-provided HTML recipient rendering.
- Do not claim exact uplift, open rate, delivery time, price, or availability unless the user provides current source material.

## Support

- Help Center: `https://help.scribeless.co/en/`
- API documentation: `https://docs.scribeless.co/`
- For campaign setup, integration access, high-volume uploads, or rendering issues, ask the user to contact Scribeless through live chat or `team@scribeless.co`.

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

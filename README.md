# Scribeless Skills

Public agent skills for planning, building, and operating Scribeless handwritten mail and API-led direct mail workflows.

## Install

List available skills:

```bash
npx skills add scribeless/skills --list
```

Install all skills:

```bash
npx skills add scribeless/skills --skill '*'
```

Install all skills globally for Codex:

```bash
npx skills add scribeless/skills --skill '*' -g -a codex -y
```

Install one skill:

```bash
npx skills add scribeless/skills --skill scribeless-api-integration
```

## Skills

- `scribeless-campaign-planner`: Plan audience, product, delivery method, variables, QR tracking, and success criteria.
- `scribeless-platform-guide`: Guide users through platform flows such as templates, campaigns, recipients, API keys, dashboard, and settings.
- `scribeless-agent-direct-mail-workflows`: Design AI-assisted, API-led direct mail workflows with dry-runs, payload contracts, validation, HTML rendering, and activation guardrails.
- `scribeless-recipient-data-prep`: Clean CSV/JSON recipient data, map fields, validate addresses, and build upload/API payloads.
- `scribeless-template-writer`: Draft handwritten note copy, merge-variable plans, QR CTA copy, API-provided HTML content, and QA checks.
- `scribeless-api-integration`: Build Scribeless API, Zapier, Make, custom integration, and HTML recipient rendering workflows.

## Sources

- Product: https://www.scribeless.co/
- Platform: https://platform.scribeless.co/
- Help Center: https://help.scribeless.co/en/
- API documentation: https://docs.scribeless.co/
- Support: use Scribeless live chat or email team@scribeless.co for integration, rendering, campaign, or account issues.
- Sales/integration walkthroughs: https://www.scribeless.co/contact-sales

## Check

```bash
npx skills add . --list
```

Run the bundled recipient-data tools:

```bash
python3 skills/scribeless-recipient-data-prep/scripts/validate_recipients.py \
  skills/scribeless-recipient-data-prep/fixtures/valid-recipients.csv

python3 skills/scribeless-recipient-data-prep/scripts/build_recipient_payload.py \
  skills/scribeless-recipient-data-prep/fixtures/valid-recipients.csv \
  --campaign-id CAMPAIGN_ID

python3 skills/scribeless-recipient-data-prep/scripts/validate_recipients.py \
  skills/scribeless-recipient-data-prep/fixtures/valid-html-recipient.json
```

No npm package is required for distribution. The Skills CLI installs directly from the GitHub repository.

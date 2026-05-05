# Scribeless Skills

Public agent skills for planning, building, and operating Scribeless handwritten mail workflows.

These skills are designed for public Scribeless users. They do not require internal Scribeless systems, private local paths, or company credentials.

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
- `scribeless-recipient-data-prep`: Clean CSV/JSON recipient data, map fields, validate addresses, and build upload/API payloads.
- `scribeless-template-writer`: Draft handwritten note copy, merge-variable plans, QR CTA copy, and QA checks.
- `scribeless-api-integration`: Build Scribeless API, Zapier, Make, and custom integration workflows.

## Sources

- Product: https://www.scribeless.co/
- Platform: https://platform.scribeless.co/
- Help Center: https://help.scribeless.co/en/
- API documentation: https://docs.scribeless.co/

## Check

```bash
npx skills add . --list
```

No npm package is required for distribution. The Skills CLI installs directly from the GitHub repository.

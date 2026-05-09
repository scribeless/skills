---
name: scribeless-agent-direct-mail-workflows
description: Design and review AI-assisted, API-led Scribeless direct mail workflows. Use when a user wants an AI agent, LLM workflow, custom app, server-side automation, CRM automation, data pipeline, or generated creative system to create recipients, generate personalized variables or HTML front/back content, validate payloads, trigger previews, and safely operate direct mail campaigns through the Scribeless API.
---

# Scribeless Agent Direct Mail Workflows

## Workflow

1. Define the agent job:
   - trigger or user intent
   - source system and available data
   - campaign ID and campaign state for standard recipient workflows
   - product key, envelope setting, and orientation for custom HTML recipient rendering
   - approval boundary before live sending
   - max recipient volume per run
2. Choose the rendering path:
   - standard Scribeless template plus variables
   - custom HTML recipient rendering via `POST /api/recipients/html`
   - Smart QR code destination and tracking variables
3. Build the payload contract:
   - required recipient identity and postal address fields
   - business variables used by the template or HTML
   - source identifiers for dedupe and audit, such as `external_id`
   - suppression rules and retry behavior
4. Require a dry-run phase:
   - validate data shape before API calls
   - produce a sample `POST /api/recipients` or `POST /api/recipients/html` payload
   - send standard campaign tests only to a Pending recurring campaign
   - review rendered custom HTML documents before live use
   - review generated previews or rendered documents before activation/live use
5. Produce an operating plan:
   - happy path
   - failure handling
   - logs/observability
   - rollback or pause action
   - human approval points
6. Hand off to focused skills when needed:
   - `$scribeless-api-integration` for endpoint examples and automation setup
   - `$scribeless-recipient-data-prep` for CSV/JSON mapping and payload generation
   - `$scribeless-template-writer` for copy and HTML content QA
   - `$scribeless-campaign-planner` for campaign strategy

## Agent Safety Rules

- Do not send live API requests unless the user explicitly asks after reviewing the payload.
- Test standard campaign recipient workflows against a Pending recurring campaign. After activation, new recipients may be produced, mailed, and charged.
- For custom HTML rendering, confirm the selected `product_key`, `include_envelope`, and `orientation` before making live requests.
- Never expose API keys in chat, logs, client-side code, or generated artifacts.
- Put secrets in the workflow platform's secure credential store.
- Require dedupe/suppression before recurring or autonomous sends.
- Keep a visible limit on recipients per run until the workflow has been proven.
- Make generated HTML deterministic and self-contained; JavaScript and most external resource loads are blocked by the renderer.

## Support

- Help Center: `https://help.scribeless.co/en/`
- API documentation: `https://docs.scribeless.co/`
- For integration, rendering, campaign, or account issues, route the user to Scribeless live chat or `team@scribeless.co`.

## Output Shape

```markdown
## Agent Workflow
- Trigger:
- Data source:
- Campaign state:
- Rendering path:
- Payload contract:
- Suppression/dedupe:
- Dry-run/test path:
- Activation guard:
- Failure handling:

## Example Payload
[JSON]

## Handoff
- API setup:
- Data validation:
- Copy/HTML QA:
```

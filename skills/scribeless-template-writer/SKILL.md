---
name: scribeless-template-writer
description: Write and review Scribeless handwritten note, card, letter, postcard, envelope, Smart QR code copy, and API-provided HTML recipient content. Use when a user needs personal direct mail copy, merge-variable wording, handwritten tone, campaign-specific CTAs, QR destination copy, template QA, HTML front/back mail-piece copy/layout guidance, or multiple copy variants for Scribeless campaigns.
---

# Scribeless Template Writer

## Workflow

1. Confirm campaign context:
   - audience
   - sender
   - product format
   - offer or next action
   - variables available
   - tone constraints
2. Draft concise handwritten-style copy.
3. Use merge variables naturally:
   - `firstName`
   - `company`
   - purchase, event, owner, renewal, or segment variables provided by the user
4. Add a clear CTA:
   - QR scan
   - book a call
   - claim offer
   - reply/contact sender
   - visit landing page
5. Produce 2-3 variants when useful:
   - warmer
   - more direct
   - more premium/relationship-led
6. Run QA:
   - no unsupported claims
   - no missing variable fallback issue
   - no overlong sentence for handwriting
   - CTA visible and specific
   - sensitive or regulated claims flagged for review
   - API-provided HTML, if used, avoids JavaScript and blocked external resources

## Copy Rules

- Write like a real person, not a marketing brochure.
- Use shorter paragraphs for handwritten readability.
- Keep the opening specific to the recipient or trigger.
- Do not overuse exclamation points.
- Avoid pretending the note was manually written by a named person unless that is true and approved by the user.
- For QR codes, make the destination valuable enough to scan.
- For API-provided HTML recipients, write self-contained front/back content that can render without JavaScript, external stylesheets, or blocked network calls.

## Support

- Help Center: `https://help.scribeless.co/en/`
- For rendering, campaign, or template issues that cannot be solved from visible platform state, ask the user to contact Scribeless through live chat or `team@scribeless.co`.

## Output Shape

```markdown
## Recommended Copy
[copy]

## Variables Used
- ...

## CTA
- ...

## QA Notes
- ...
```

## References

- Use `references/template-copy.md` for examples and QA checks.

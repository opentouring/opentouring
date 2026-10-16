<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Domain docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase. This repo is single-context.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: the glossary.
- **`docs/adr/`**: read ADRs that touch the area you're about to work in.

## File structure

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-auspice-by-an-existing-not-for-profit.md
│   └── 0002-cc-by-4-0-data-with-revenue-from-the-api-service.md
├── schema/
├── api/
├── services/
├── pipelines/
├── web/
├── infra/
└── sdks/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Use the defined term in place of the synonyms the glossary lists under _Avoid_.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0009 (event-sourced submissions), but worth reopening because..._

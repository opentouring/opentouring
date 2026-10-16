---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Schema and API stay a draft until v1.0.0 is released

The OTWD schema and API are a draft until a `v1.0.0` tag is made on this repository, which happens before any partner app outside the project integrates. Until then any field, code or endpoint can change or be removed without a new major version, and every document carries `schema_version` `1.0`. From the tag on, version 1 only grows by additions and a breaking change ships as version 2 under `/v2`, as set out in `schema/README.md` and `api/README.md`.

No partner app outside the project integrates yet, so a breaking change costs nothing beyond updating the project's own examples and the founding partner app. Freezing the contract now would force a version 2 for changes that research and review still turn up, before anyone outside the project has used version 1.

## Consequences

The OpenAPI document's version reads `1.0.0-draft` until the tag. The founding partner app's staging integration builds against the draft and expects changes. Tagging `v1.0.0` is a roadmap step that comes before outside partners are invited.

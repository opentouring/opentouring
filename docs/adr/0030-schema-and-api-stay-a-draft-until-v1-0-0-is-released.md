---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Schema and API stay a draft until v1.0.0 is released

The OTWD schema and API are a draft until a `v1.0.0` tag is made on this repository, which happens before any partner app outside the project integrates. Until then any field, code or endpoint can change or be removed without a new major version, and every document carries `schema_version` `1.0`. From the tag on, version 1 only grows by additions and a breaking change ships as version 2 under `/v2`, as set out in `schema/README.md` and `api/README.md`.

The contract was written in a day and is still being shaped by research and review. Freezing it on its first commit would force a version 2 before anyone has used version 1, while no consumer exists that a change could break.

## Consequences

The OpenAPI document's version reads `1.0.0-draft` until the tag. FuelOracle's staging integration builds against the draft and expects changes. Tagging `v1.0.0` is a roadmap step that comes before outside partners are invited.

---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# AGPL-3.0 server code, Apache-2.0 SDKs and schema

Server-side code (services, pipelines, website, infrastructure) is licensed under AGPL-3.0. The SDKs, the JSON Schema, the OpenAPI spec and sample clients are licensed under Apache-2.0. The AGPL means anyone who runs a modified copy of the platform as a network service must publish their changes, so improvements to the platform come back. Partner apps link SDKs and copy schema definitions into their own code, often closed source, so those pieces need a permissive licence with a patent grant or nobody will adopt them.

## Considered options

- **Apache-2.0 for everything.** Rejected: a well-funded operator could run a closed fork of the platform and compete with the host.
- **AGPL-3.0 for everything.** Rejected: it would deter partner apps from using the SDKs, which is how data comes back.

## Consequences

The licence of each directory is listed in LICENSING.md and declared with SPDX identifiers in every source file. Code must not move from an AGPL directory to an Apache directory unless every author of that code agrees.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Roadmap

Open Touring is built as a working concept before a host is approached, so that the host can see real assets. The concept build runs on the production stack at minimum size, with public code, a public Preview site, seeded government data and only the maintainer's submissions.

## Concept build

### 1. Design documents

- [ ] CONTEXT.md glossary
- [ ] Architecture decision records in docs/adr/
- [ ] Architecture overview (docs/architecture.md)
- [ ] Licensing, governance, contributing, security and code of conduct documents
- [ ] Draft data contributor terms for legal review
- [ ] JSON Schema v1 (schema/)
- [ ] OpenAPI spec (api/)

### 2. Walking skeleton

One site end to end, on infrastructure as code.

- [ ] Accounts created fresh under an Open Touring email: GitHub organisation, domain, cloud, CDN, AI provider
- [ ] Cluster, database, event bus, cache and gateway defined in OpenTofu and deployed by Argo CD
- [ ] Seed one site from a government dataset as a submission with seed-source provenance
- [ ] Query API returns the site
- [ ] Submit API appends a submission to the submission log
- [ ] Moderation queue shows the submission and records a moderation decision
- [ ] Approved change is applied, gets a sequence number and is published
- [ ] Website renders the site page from the public API

### 3. Breadth

- [ ] Full schema: all site types and facilities in the governed list, rig limits, prices, hours
- [ ] Fixed checks and AI pre-checks with structured verdicts
- [ ] Developer portal with reference generated from the OpenAPI spec
- [ ] SDKs generated from the OpenAPI spec
- [ ] Bulk downloads (full and delta) behind the CDN
- [ ] First state, Victoria, seeded and moderated
- [ ] FuelOracle contribute-back running against staging
- [ ] Public Preview site live

## To verify

- [x] PostGIS is available on Linode managed Postgres: `CREATE EXTENSION postgis` passed on 16 October 2026 (PostgreSQL 18.6, PostGIS 3.6.4). See [ADR 0017](adr/0017-postgres-with-postgis.md).
- [ ] Bunny Shield pricing: Shield Basic, the free level, is enabled. Whether the paid level is worth it, and its request caps, is still open.
- [x] Which state's government open data is richest and best licensed: Victoria, then New South Wales and Western Australia. See [ADR 0024](adr/0024-one-state-first.md) and [the research](research/seed-data-australia.md).
- [x] Whether OSGeo Oceania hosts projects, and on what terms: researched. OSGeo Oceania is approached first, and a Linux Australia proposal is prepared in parallel as the realistic default. See [GOVERNANCE.md](../GOVERNANCE.md) and [the research](research/host-organisations.md).
- [x] OSM and schema.org mappings checked against primary sources. See [the mapping verification](research/mapping-verification.md).
- [ ] Professional trade mark clearance for "Open Touring" and "OTWD" before filing
- [ ] Running costs once the design exists. First estimates are in [the platform cost research](research/platform-costs.md).

## After a host agrees

- [ ] Host agreement (MOU) signed and assets transferred
- [ ] Contributor terms reviewed by a lawyer and put in force
- [ ] Steering group formed
- [ ] Release the schema and API as `v1.0.0` (tag) before any outside partner app integrates ([ADR 0030](adr/0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md))
- [ ] Outside contributions switched on in production

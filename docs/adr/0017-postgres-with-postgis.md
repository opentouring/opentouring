---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Postgres with PostGIS

Live data, the submission log and the outbox live in Postgres with PostGIS, with heavy read queries sent to read replicas. The database is Linode's managed Postgres (an Aiven-based service) in Sydney. A live test on 16 October 2026 created a PostgreSQL 18.6 cluster in `ap-southeast`, ran `CREATE EXTENSION postgis` successfully (PostGIS 3.6.4, GEOS 3.14.1, PROJ 9.8.1), computed a geography distance correctly, and also installed `pg_trgm` and `unaccent`. `h3` and `pgrouting` are available too. The test cluster was deleted afterwards. Details are in `docs/research/platform-costs.md`.

## Considered options

- **CloudNativePG in the cluster.** Kept as the fallback. It would make backups, failover and upgrades the project's job, which a maintainer working with agents should avoid while a managed service passes the test.

## Consequences

Spatial queries (sites near a point, sites in a box, duplicate candidates by distance and name similarity) run in the database. The managed service exposes a built-in connection pool on its own port, which is tried before adding PgBouncer. Point-in-time restore was available within minutes of creation. Access is limited by an IP allow list, and a new cluster's hostname took a few minutes to appear in public DNS after it reported active.

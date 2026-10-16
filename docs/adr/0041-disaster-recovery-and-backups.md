---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Disaster recovery and backups

OTWD keeps two independent kinds of database backup. The managed Postgres service's own backups and point-in-time restore cover everyday mistakes and failures ([ADR 0017](0017-postgres-with-postgis.md)). Encrypted logical backups, taken on a schedule and stored with a different provider, Bunny Storage in its Sydney region ([ADR 0021](0021-bunny-cdn-and-crowdsec-instead-of-cloudflare.md)), cover the loss of the database provider or the account. Restores are tested every quarter, and the runbook is [docs/operations/disaster-recovery.md](../operations/disaster-recovery.md).

| Environment | Recovery point objective | Recovery time objective |
| ----------- | ------------------------ | ----------------------- |
| Preview     | 24 hours                 | 3 business days         |
| Production  | 1 hour                   | 8 hours                 |

The submission log is the source of everything else ([ADR 0009](0009-event-sourced-submissions-never-direct-writes.md)): live data, the change feed and bulk downloads can be rebuilt from it, and they cannot be rebuilt without it. Backups held only by the provider that runs the database would be lost with that provider's account. Akamai's documentation describes automatic backups and restores that create a new cluster, and gives retention as up to seven backups on one page and 14 days on another ([Managed Databases](https://techdocs.akamai.com/cloud-computing/docs/managed-databases), [Linode API: create a PostgreSQL database](https://techdocs.akamai.com/linode-api/reference/post-databases-postgre-sql-instances)), so the plan assumes the shorter figure. Bunny is already in the stack and is a separate company and account. Bunny's storage documentation does not state encryption at rest ([storage replication](https://bunny.net/docs/storage/replication)), so backups are encrypted before upload with keys Bunny never holds.

## Considered options

- **Rely on the managed service's backups alone.** Rejected: they share the fate of the provider account, and retention of a week or two is too short to notice slow corruption.
- **Linode Object Storage for backups.** Rejected: same provider, and no Sydney endpoint ([ADR 0029](0029-object-storage-deferred-singapore-bucket-for-infrastructure-state-only.md)).
- **Replicate to a standby database at another provider.** Deferred: it costs a second database all the time, and the objectives above are met without it.

## Consequences

The off-site backups also make a host handover practical: the same export carries the submission log, moderation decisions and live data, with contributor identity links in a separately encrypted file, and [GOVERNANCE.md](../../GOVERNANCE.md#transfer-intent) names it as part of the transfer. Backups hold personal information, so their retention (at most 90 days) appears in [the privacy policy draft](../policies/privacy-draft.md), and erasures and takedowns are applied again after any restore. The cluster holds no data and is rebuilt from this repository by Argo CD, and OpenTofu state is in its own bucket, so neither needs a backup of its own beyond the repository and that bucket.

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Disaster recovery runbook

This runbook says what is backed up, where, how often, and how to restore it, for the preview and production environments. The decision behind it is [ADR 0041](../adr/0041-disaster-recovery-and-backups.md). Infrastructure names follow [docs/architecture.md](../architecture.md).

## Objectives

| Environment | Recovery point objective (data that may be lost) | Recovery time objective (time to serve again) |
| ----------- | ------------------------------------------------ | --------------------------------------------- |
| Preview     | 24 hours                                         | 3 business days                               |
| Production  | 1 hour                                           | 8 hours                                       |

Staging has no objectives. It is rebuilt from the preview's latest backup when needed.

## What is protected, and how

| What                                                                     | Primary copy                        | Protection                                                                                                                                      |
| ------------------------------------------------------------------------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Live data and its history                                                | Data repository per country, GitHub | Every clone, and the read-only mirror on a second forge                                                                                         |
| Submission log, moderation decisions, read model, trust scores           | Managed Postgres, Sydney            | Managed backups and point-in-time restore, plus encrypted off-site logical backups. The read model can also be rebuilt from the data repository |
| Contributor identity links and the sign-in service's database            | Managed Postgres, Sydney            | As above, with identity links also exported to a separately encrypted file                                                                      |
| Photo files                                                              | Bunny Storage, Sydney               | Hash and metadata in the submission log. See known gaps                                                                                         |
| Bulk downloads                                                           | Bunny Storage, Sydney               | None needed: rebuilt from live data                                                                                                             |
| Cache and rate limit counters                                            | Managed Valkey                      | None needed: rebuilt as traffic arrives                                                                                                         |
| Kubernetes cluster and its workloads                                     | LKE, Sydney                         | None needed: rebuilt from this repository by OpenTofu and Argo CD                                                                               |
| OpenTofu state                                                           | Linode Object Storage, Singapore    | OpenTofu state encryption                                                                                                                       |
| Secrets needed to restore (backup decryption keys, provider credentials) | The operator's password manager     | A sealed copy held for the host, see [GOVERNANCE.md](../../GOVERNANCE.md#transfer-intent)                                                       |

## Managed backups

The managed Postgres service takes automatic backups and can restore to a point in time. A restore, called a fork, creates a second cluster rather than overwriting the first ([Managed Databases](https://techdocs.akamai.com/cloud-computing/docs/managed-databases), [managing a database cluster](https://techdocs.akamai.com/cloud-computing/docs/aiven-manage-database)). Akamai's pages give retention as up to seven backups on one page and 14 days on another, so this runbook assumes seven days.

## Off-site logical backups

A scheduled job in the cluster takes a logical backup of every database in the managed Postgres cluster:

1. `pg_dump --format=custom` of each database, from the read replica so the primary is not loaded.
2. The contributor identity link tables are also dumped to their own file, encrypted to a second key, so the main backup can be shared with a restore tester without exposing identity links.
3. Each file is encrypted with `age` to the backup public keys before it leaves the cluster. Bunny never holds a private key.
4. The encrypted files and a `SHA256SUMS` file are uploaded to a dedicated Bunny Storage zone in the Sydney region, through Bunny's storage HTTP API, with credentials that can write to that zone only.

| Environment | Schedule      | Kept                                                              |
| ----------- | ------------- | ----------------------------------------------------------------- |
| Preview     | Daily         | 30 daily backups                                                  |
| Production  | Every 6 hours | 7 days of 6-hourly, then daily to 30 days, then weekly to 90 days |

Nothing is kept longer than 90 days, the limit in [the privacy policy draft](../policies/privacy-draft.md). The job reports success or failure to the observability stack, and a missed backup alerts the maintainer.

## Restoring

### A bad change or a failed database: point-in-time restore

Use this first. It is the fastest path and loses the least data.

1. Decide the restore time: just before the bad change, or the latest time for a failed primary.
2. Fork the cluster to that time from Cloud Manager or the Linode API (the `fork` object with `source` and `restore_time`). The fork is a new cluster with its own hostname.
3. Install the PostGIS, `pg_trgm` and `unaccent` extensions if the fork lacks them, and add the cluster's IP allow list.
4. Point the environment's OpenTofu configuration at the new cluster and apply it, so Argo CD rolls the API, workers and pipelines onto the new connection details.
5. Run the checks under "After any restore".
6. Delete the old cluster once the new one is serving and the checks pass, because both are billed.

### The database provider or account is lost: restore from off-site

1. Create a Postgres cluster with PostGIS, on Linode in a fresh account or with another provider, using the OpenTofu modules in `infra/` with new provider settings.
2. Download the latest backup set from Bunny Storage, check it against `SHA256SUMS`, and decrypt it with the backup private key.
3. `pg_restore` each database. Restore the identity link file only if moderation is to resume, using its own key.
4. Rebuild the cluster from this repository, pointed at the new database, and repoint DNS if the API host changed.
5. Run the checks under "After any restore".

### The cluster is lost

Apply the environment's OpenTofu configuration to create a new cluster and let Argo CD deploy every workload from this repository. The cluster holds no data.

## After any restore

1. Re-apply the erasure list and every takedown recorded after the backup was taken ([the takedown process](../policies/takedown.md)), so nothing erased comes back.
2. Check the highest `change_seq` against the change feed partner apps last received. Changes approved after the restore point are lost, so tell partner apps on paid tiers the sequence number to resume from, and re-queue submissions whose decisions were lost from the submission log of the old database where it can still be read.
3. Run `tools/check-schema.sh`, rebuild one bulk download per record type and validate a sample of records against the schema.
4. Purge the CDN and rebuild bulk downloads.
5. Record what happened, the data lost and the time taken in a GitHub issue, and update this runbook with anything that did not match it.

## Restore tests

Every quarter, the maintainer restores the latest off-site backup of production (of preview until production exists) to a temporary cluster, without the identity link file, and runs the checks above against it. The test records the backup's age, the time each step took and any failure in a GitHub issue titled "Restore test `<year>` Q`<n>`", then deletes the temporary cluster. A test that misses an objective opens a fix before the next quarter.

## Host handover export

When Open Touring moves to the host or a successor ([GOVERNANCE.md](../../GOVERNANCE.md#transfer-intent)), the outgoing operator produces a final off-site backup set and hands over:

- the submission log and moderation decisions, in the logical backup
- the GitHub organisation, which holds the data repositories and the GitHub App, transferred with ownership
- contributor identity links and the sign-in service's database, in their separately encrypted file
- the backup private keys and every secret in the table above, handed over in person or through an encrypted channel, never in this repository
- the photo files, copied from Bunny Storage, unless the Bunny account itself is transferred
- control of the Bunny Storage zone, the Linode accounts, the OpenTofu state bucket and the domains

The receiving operator restores the set to its own accounts with the off-site restore steps above and confirms the checks pass before the old accounts are closed.

## Known gaps

Photo files live only in Bunny Storage. Losing the Bunny account would lose them, though every photo's hash, author and licence survive in the submission log. A copy outside Bunny needs a provider decision, because [ADR 0029](../adr/0029-object-storage-deferred-singapore-bucket-for-infrastructure-state-only.md) keeps Linode Object Storage to infrastructure state. Until that decision, a photo copy is made with every host handover and before any change to the Bunny account.

The restore steps above still treat Postgres as the home of live data. Since [ADR 0046](../adr/0046-live-data-in-a-public-git-repository-per-country.md), recovering live data is a rebuild of the read model from the data repository, and the restore steps are rewritten for that when the read side is designed.

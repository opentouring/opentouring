---
status: superseded by ADR 0046
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# NATS JetStream with a transactional outbox

Events between components (new submission, moderation decision, change applied) go through NATS JetStream. A service writes the event to an outbox table in the same Postgres transaction as the data it changes, and a relay publishes outbox rows to JetStream. An event is never published for a change that rolled back, and never lost for one that committed.

## Considered options

- **Kafka.** Rejected: too heavy to run at preview size.
- **Postgres LISTEN/NOTIFY only.** Rejected: no durable replay for consumers that were down.

## Consequences

Consumers (moderation workers, bulk download builder, cache purger, webhook sender) must be idempotent, because the relay can publish an event more than once.

Superseded by [ADR 0046](0046-live-data-in-a-public-git-repository-per-country.md), which replaces the outbox and the event bus with a loader that applies commits from the data repository in order and drives the bulk download builder, cache purger and webhook sender.

---
status: superseded by ADR 0046
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Event-sourced submissions, never direct writes

Every submission is appended to an append-only submission log and never writes to live data. Live data changes only when a moderation decision approves a submission, which produces a change with a sequence number. The log keeps the full history of who proposed what, what the fixed checks and AI found, and who decided, which moderation, appeals, trust scores and the evaluation set all depend on. It also lets live data be rebuilt or corrected after a bad decision.

## Considered options

- **Direct edits with an undo history.** Rejected: bad data would be visible to partner apps before anyone saw it, and safety facts cannot work that way.
- **A staging table merged on a schedule.** Rejected: it loses the per-submission decision record and delays every approved change until the next run.

## Consequences

The API has no endpoint that updates a site in place. Partner apps submit and later read the outcome. Approved changes flow out through the change feed, which also drives bulk download rebuilds, cache purges and webhooks.

Superseded by [ADR 0046](0046-live-data-in-a-public-git-repository-per-country.md), which keeps the submission log private on opentouring.org and makes a pull request on the country's data repository the public stage. Live data still changes only when a moderation decision approves a submission.

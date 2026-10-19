---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Live data in a public git repository per country

Supersedes [ADR 0008](0008-free-api-key-required-even-for-bulk-downloads.md), [ADR 0009](0009-event-sourced-submissions-never-direct-writes.md) and [ADR 0018](0018-nats-jetstream-with-a-transactional-outbox.md). Amends [ADR 0011](0011-no-anonymous-edits-pseudonymous-partner-ids.md) and [ADR 0013](0013-stable-public-ids-and-per-fact-provenance.md).

The source of truth for live data is a public git repository on GitHub, one per supported country, starting with `opentouring/otwd-au`. Every record is a JSON file, every change is a commit on `main`, and anyone can clone the whole dataset without an API key. opentouring.org becomes the layer that takes submissions from the public and from partner apps, turns them into pull requests, and serves the paid API from a read model built from the repository. Moderation on GitHub is set out in [ADR 0047](0047-moderation-on-github-through-pull-requests.md).

The data stays CC BY 4.0 and revenue still comes from the API as a service ([ADR 0002](0002-cc-by-4-0-data-with-revenue-from-the-api-service.md)). The contributor grant in [ADR 0006](0006-transferable-contributor-grant-for-data.md) is unchanged.

## Why

A public repository makes the dataset forkable from the first commit: if the operator or the host stops, every clone holds the full data and its history. Commit history gives every change an open, reviewable record, and pull requests give moderation a public trail without building one. It also removes the event bus and the moderation workers as writers of live data, which shrinks what the operator has to run.

## Decision

**Data repositories.** One public data repository per supported country, created from an `otwd-template` repository that carries the CI, rulesets, CODEOWNERS skeleton and `otwd.json`. Records live at `<state>/<record-type>/<ulid>.json`, for example `vic/sites/01JA2V7Q3M8X4K6T9B5N0R2C7D.json`. A record that crosses a state or territory border, such as a ferry service across Bass Strait or a road segment over the Murray, lives under `interstate/`. A correction that moves a record into another state moves its file in the same commit, and everything downstream follows the public ID, never the path. The GitHub organisation, the data repositories and the GitHub App belong to Open Touring and transfer to the host with the organisation ([ADR 0025](0025-the-preview-runs-the-production-stack.md)).

**The repository form.** A record file is the full form without the values OTWD computes when it loads the record: `change_seq` on the record and on each fact, derived values, `confidence` and `updated_at`. Closed records keep their files. Merged, replaced and retracted records shrink to stubs ([ADR 0036](0036-record-lifecycle-and-change-origins.md)) and are never deleted, so a public ID never disappears from the repository. The schema gains this form as its own document kind before `v1.0.0` ([ADR 0030](0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)).

**Schema pinning.** `otwd.json` at the repository root names the schema tag the data conforms to, and CI validates every pull request against that tag. A schema change that needs data changed lands as its own migration pull request in the data repository.

**One submission, one change.** Pull requests are squash-merged through a merge queue, history on `main` is linear, and one pull request carries one submission. The squash commit is the change. The merge queue re-runs the fixed checks against the latest `main` before each merge, so two pull requests that each pass alone cannot both add the same site.

**Sequence numbers come from the read model.** The loader assigns `change_seq` in commit order as it applies commits from `main`. The change feed, delta files and conflict checks on `base_change_seq` work as before, from the read model.

**The submission log stays private.** opentouring.org keeps the submission log and the identity link ([ADR 0038](0038-contributor-identity-in-published-data.md)). A submission becomes a pull request only after it passes the fixed checks and a screen for spam and personal information. A submission that fails is rejected inside opentouring.org with a moderation decision and never reaches GitHub, because a closed pull request stays public and only GitHub Support can delete it. This replaces ADR 0009: the log is private, the pull request is the public, reviewable stage, and live data still changes only when a moderation decision approves a submission.

**Nothing in git identifies a contributor.** Pull requests the GitHub App opens are authored by the App and carry the decision ID once there is one, never a submission ID, pseudonymous ID, contributor ID or display name. The App opens pull requests in scheduled batches, not as each submission arrives, so a pull request's timestamp does not reveal when a contributor submitted. Contributors who open a pull request from their own GitHub account (ADR 0047) choose to be public, as a direct contributor who shows their display name does. This amends ADR 0011: contributors are still never anonymous to OTWD, but the identity stays in the identity link.

**Public IDs.** Public IDs are ULIDs, so the App and contributors can mint them without coordinating and two pull requests cannot collide. This amends ADR 0013 only in where values live: provenance stays per fact in the repository form, and `change_seq` and `confidence` are added by the read model.

**The read model.** A loader keeps the commit SHA it last applied. On each push webhook, and on a 5-minute timer as a backstop, it applies the commits between that SHA and `main` in order to Postgres with PostGIS. After a history rewrite (ADR 0047) it rebuilds from an empty database. Derived values and recompute changes are produced by the loader and never committed. The query API, the change feed, webhooks and bulk downloads are served from the read model.

**Access.** Cloning a data repository needs no key. An API key is still needed for the query API, the change feed, webhooks and bulk downloads from the CDN. This replaces ADR 0008 for git: contribute-back obligations live in the API terms of service, and readers who clone are asked to contribute back without it being a condition.

**Photos stay out of git.** A photo is uploaded to opentouring.org, its embedded location data is stripped, and it waits in a private quarantine area. The pull request names the photo ID and links to a signed preview that expires. When the pull request merges, the loader publishes the photo to Bunny Storage behind the CDN. A rejected photo is deleted from quarantine.

**No event bus.** The loader's ordered walk of `main` replaces the outbox and NATS JetStream. The loader drives the bulk download builder, the cache purger and the webhook sender directly, and each is idempotent because the loader can replay a commit after a restart. This replaces ADR 0018. The rest of the stack stays as decided (ADRs 0015, 0016, 0017, 0019, 0020, 0021 and 0025), and running costs are estimated again once the read side is designed.

**A read-only mirror.** Each data repository is mirrored read-only to a second forge such as Codeberg, so the data survives a change in GitHub's terms or a problem with the organisation's account. The moderation workflow depends on GitHub, and that is accepted.

**Staging.** Partner integrations, the founding partner's contribute-back among them, are tested against a private `otwd-au-staging` repository with its own App installation and its own read model.

**When to split.** A country repository splits into one repository per state or territory when it passes 1 GB or CI on a pull request takes longer than 10 minutes, whichever comes first. The split needs no new ADR.

## Considered options

- **Keep live data in Postgres and publish a git mirror.** Rejected: the mirror would be a copy, not the record, so it would not make the dataset forkable in the sense that matters, and it would keep the event bus and moderation workers.
- **One repository per state from the start.** Rejected for now: records that cross a border would need a pull request in two repositories, and CODEOWNERS already gives each state its own moderators in one repository.
- **A non-commercial data licence on the repository with commercial use sold.** Rejected: it would sell a licence, which ADR 0002 rules out, the seed sources' CC BY 4.0 licences forbid adding downstream restrictions to their facts, and "non-commercial" is too vague for councils and partner apps to rely on.
- **Every submission as a pull request.** Rejected: spam, defamation and personal information in rejected submissions would stay public for good.
- **Photos in the repository, or in Git LFS.** Rejected: clones would grow with every photo, takedowns would need history rewrites far more often, and LFS bandwidth is billed.
- **`change_seq` in the record files.** Rejected: every merge would write the next number, so every pair of pull requests would conflict and merges could only happen one at a time.

## Open questions

- Confirmations ([ADR 0036](0036-record-lifecycle-and-change-origins.md)) are low-risk and frequent. Whether each becomes a commit, or confirmations are batched or held only in the read model with the count committed, needs deciding before confirmations open.
- GitHub limits how fast an app can create content. The App's batch size and schedule need measuring against those limits once real submission volumes exist.

## Consequences

The submit API writes to the private submission log, and the GitHub App turns screened submissions into pull requests. Postgres becomes a read model that can be rebuilt from git at any time, which makes recovery of live data a rebuild ([ADR 0041](0041-disaster-recovery-and-backups.md)). The schema gains the repository form, and the validator checks files in that form. `docs/architecture.md`, `CONTEXT.md`, `LICENSING.md`, the takedown process, the privacy policy draft and the contributor terms draft describe the new flow. The disaster recovery runbook still lists the outbox and is updated when the read side is designed.

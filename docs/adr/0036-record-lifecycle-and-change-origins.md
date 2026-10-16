---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Record lifecycle beyond merges, and changes without a submission

A change required a submission and a moderation decision, and a record could only be active, closed or merged into another record of its own type. That left no honest way to record four things the platform has to do: undo a bad change, take content down, recompute derived values when a boundary dataset changes, and fix a record that turned out to be the wrong type, two things at once, or wrongly merged. Each would otherwise be faked as a submission from nobody, or done as a direct write that skips the submission log ([ADR 0009](0009-event-sourced-submissions-never-direct-writes.md)).

## Change origins

Every change now has an `origin`, an open enumeration ([ADR 0035](0035-open-enumerations-and-a-record-type-registry.md)), beside its `kind`. The kind says what happened to the record and the origin says why, so a revert of a merge is a `record_unmerged` with origin `revert`, and a takedown of a photo is a `photo_removed` with origin `takedown`.

- **submission**: a moderation decision approved a submission. It names `submission_id` and `decision_id`, as before.
- **revert**: a moderator undid the change named in `reverts_seq`, after an upheld appeal, vandalism, a moderator's mistake, or to remove everything an abused API key sent ([ADR 0039](0039-partner-api-keys-tokens-and-abuse.md)). The touched facts return to their values and provenance before that change, with the revert's sequence number as their `change_seq`, so a submission based on the bad value meets a conflict. One decision can revert many changes, each as its own revert change.
- **takedown**: a moderator removed content for the reason in `takedown_reason` (personal information, copyright, a legal requirement, offensive content or a private place). A takedown names its decision and never a submission, so the change feed cannot lead back to whoever asked. Requests are handled as restricted cases under the moderation policy (to be published at `docs/policies/moderation.md`), outside the submission log.
- **recompute**: OTWD recomputed derived values (country, subdivision, locality, time zones, length) for a reason in `recompute_reason`, such as a boundary dataset update or a new IANA time zone database. The kind is always `derived_updated` and `changed_fields` is only `/derived`. It has no submission and no decision, because no fact changes. The fire district is a fact with seed source provenance, so a change of fire district boundaries arrives as seed source submissions and is moderated, never recomputed silently.

Reverts and takedowns are moderation decisions without a submission: a decision's new `subject` is `submission`, `revert` or `takedown`. Only a moderator can make one, it is always approved, and it has no routing.

## Lifecycle beyond merge

Two statuses join `merged`, and together they are the stubs: records with a public ID and status but no facts, never listed.

- **replaced**: the record was the wrong record type, such as a low rail bridge entered as a site. A moderator approves a `request_replacement`, the new record of the right type is created, and the old record's `redirect_to` names it. A merge stays within one record type and a replacement always leaves it, and the validator checks both. The API answers both with 301, and a consumer that does not know the target's record type skips it.
- **retracted**: the record should never have been published, because the thing does not exist, it was spam, or a takedown removed it whole. Only the stub remains, the API answers 410, and the validator rejects any fact, photo or name left on it.

Two lifecycle operations join merge, each requested with a submission kind of its own that is on the always-human list:

- **Unmerge** (`request_unmerge`, change `record_unmerged`): a wrong merge is undone. The stub becomes a record again under the same public ID with the facts it had before the merge, and the decision records which record it came out of. Facts the merge moved onto the survivor come off it in `facts_updated` changes from the same decision.
- **Split** (`request_split`, change `record_split`): a record that described two things keeps its public ID and the facts of one of them, and the others become new records of the same type, each created with `split_from` naming the original. Keeping the original ID live, rather than turning it into a stub, means a partner app that stored it still reaches a real record.

Public IDs never change and are never reused ([ADR 0013](0013-stable-public-ids-and-per-fact-provenance.md)): an unmerge revives an ID that was always the same record's, and a split or replacement mints new IDs for the new records.

## Confirmations

`confirm_facts` lets a contributor report that facts they saw are still true, as the record showed them at `base_change_seq`. The `Confirmation` term and `Fact.confirmations` existed, but nothing produced them. A confirmation changes no value. It becomes a `facts_confirmed` change, which moves the record's `change_seq` and ETag because its full form changed, but leaves each fact's own `change_seq` alone, so it never causes a conflict for anyone else. `confirmations.count` is the number of different contributors who confirmed the current value, excluding whoever supplied it, and it resets when the value changes. Confirmations raise a fact's confidence, which feeds re-verification and trust scores.

Routing treats a confirmation like any submission that touches the fields it names. A confirmation of a safety fact goes to a moderator, because a run of false confirmations could make a wrong clearance look recent and trusted, and a person checks it against the record's history and the contributor's trust score. Confirmations of other facts are low risk and are the first candidates for automatic approval once it is switched on ([ADR 0010](0010-ai-recommends-fixed-code-routes-humans-decide.md)).

## Considered options

- **Model reverts and takedowns as submissions from a system contributor.** Rejected: the submission log would claim a contributor said something nobody said, and a takedown would carry the same identifiers as the request that caused it.
- **Let a merge cross record types.** Rejected: a merge combines facts of duplicates, which only works within one record type. A replacement creates a new record from a different fact table, and consumers need to know a redirect might lead to another type.
- **Turn a split record into a stub that redirects to its parts.** Rejected: a redirect can name only one record, and partner apps holding the original ID would lose a record that still exists.
- **Count confirmations without a submission, for example from read traffic.** Rejected: only a contributor who was there can confirm a fact, and the confirmation needs the same identity, consent and abuse controls as any submission.
- **Leave retracted records as closed.** Rejected: closed means a real place stopped operating and keeps its facts. A record that never existed, or one taken down for personal information, must not keep its facts in public.

## Consequences

`change.schema.json` requires `origin`, makes `submission_id` and `decision_id` depend on it, and gains `reverts_seq`, `takedown_reason`, `recompute_reason`, `unmerged_from`, `split_into`, `split_from` and `replaced_by`. Record schemas no longer narrow `redirect_to` to their own ID kind. The validator checks that merges, unmerges and splits stay within one record type, that a replacement leaves it, and that a retracted stub keeps nothing. Valid examples cover each origin, each new change kind, both new stubs, the four new submission kinds and revert and takedown decisions. Invalid examples prove a recompute cannot touch a fact, a takedown cannot name a submission, a revert must name its target, a replacement must change type, a retracted stub keeps nothing, a routing rule cannot revert or approve a split, and a confirmation needs `base_change_seq`.

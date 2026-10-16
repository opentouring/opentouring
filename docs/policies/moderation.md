<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Moderation policy

**Version:** `routing-1.0`. **In effect for:** the Preview, where the maintainer moderates the maintainer's own submissions and seed source imports.

This policy says how OTWD moderates submissions: what goes to a person, when automatic approval may switch on, how contributors ask for more time, answer questions and appeal, and how vandalism, seed source re-imports and stale facts are handled. It applies one standard to every submission, whichever partner app or tier sent it ([ADR 0002](../adr/0002-cc-by-4-0-data-with-revenue-from-the-api-service.md)). The pipeline that carries it out is described in [docs/architecture.md](../architecture.md#moderation-pipeline). Terms are defined in [CONTEXT.md](../../CONTEXT.md).

## Versions

The policy is a public document changed by pull request ([ADR 0040](../adr/0040-moderation-policy-is-a-versioned-public-document.md)). Its version is written `routing-<major>.<minor>`, and every moderation decision records the version it was made under in `routing.policy_version`, so a decision can always be read against the rules that applied.

- A **major** version changes where a submission goes or what outcome it can get: the list of what goes to a person, automatic approval criteria, time limits on needs-info replies and appeals, or the seed source rules.
- A **minor** version clarifies wording, adds examples or changes a suggested age for confirming stale facts, without changing any outcome.

Routing code reads the version it implements from its configuration, and a release that changes routing ships with the matching policy version. Changes need steering group approval (the maintainer during the interim arrangement in [GOVERNANCE.md](../../GOVERNANCE.md)) and are proposed with the "Moderation policy change" issue form. The history is at the end of this document.

## What goes to a person

At launch every submission goes to a person. The AI verdict is a pre-check that helps the moderator, never a decision ([ADR 0010](../adr/0010-ai-recommends-fixed-code-routes-humans-decide.md)).

Some submissions go to a person for good, even after automatic approval switches on for others. The always-human list holds new records of every record type, closures, merges and any change to a safety fact. Membership is derived by the fixed checks from the submission's kind and from the safety fact markers in the record type's schema, never from a flag routing sets ([schema/README.md](../../schema/README.md#unknown-absent-and-safety-facts)).

This policy also sends these to a person, as a routing rule that cannot be switched off without a major version:

- A change to an accessibility value that makes it more permissive, such as limited or no becoming yes. A wrong yes can strand a traveller who drove hours on the strength of it, while a wrong no costs far less (ADR 0033).
- Every photo, until photo checks for faces and number plates are measured like any other verdict.
- Every description and other free text, because free text carries defamation and copying risk ([ADR 0014](../adr/0014-reviews-and-ratings-deferred.md)).
- Every appeal, every takedown request ([the takedown process](takedown.md)) and every revert of vandalism.
- Any submission from a contributor or API key whose trust score is below the automatic approval threshold.
- A seed source re-import that conflicts with a newer community fact (see seed sources below).

Moderators record a moderation decision for each submission: approved, edited and approved (with amendments), rejected, or needs info. Rejected and needs info decisions carry a public note the contributor can read.

## Automatic approval

Automatic approval stays off until the evidence supports it, one group of submissions at a time. A group is a submission kind plus the facts it touches, such as `update_facts` on a site's `prices` or `opening_hours`. A group may switch on only when all of these hold:

1. No submission in the group can be on the always-human list or on this policy's list above.
2. The evaluation set holds at least 500 human moderation decisions for the group, made over at least 90 days.
3. Measured on the most recent 200 of those decisions, which the AI review was not tuned on, at least 98% of the submissions the verdict recommended approving were approved by the moderator unchanged.
4. The contributor and the API key both have a trust score above the threshold published with the switch-on.
5. The switch-on is a major version of this policy, with the measurements attached to the pull request.

Once a group is on, a moderator checks a random 5% of its automatic approvals each week. If the weekly sample falls below the 98% figure, the group switches off at once and stays off until a new policy version switches it on again. Every automatic approval is recorded as a moderation decision by a routing rule, with the model version, the verdict and the reasons, and it can be appealed like any other.

The figures in this section are starting values for the steering group to confirm before outside contributions open.

## Needs info

A moderator who needs more detail records a needs info decision with a public note that says exactly what is missing. Open Touring cannot contact a contributor who came through a partner app ([ADR 0011](../adr/0011-no-anonymous-edits-pseudonymous-partner-ids.md)), so the partner app relays the note, and the contributor's reply comes back through the API (ADR 0039) or the website. A reply reopens the submission in the queue with its history. A submission with no reply after 30 days is rejected with the reason code `no_reply`, and the contributor can submit again at any time.

## Appeals

A contributor can appeal any moderation decision on their own submission, including an automatic approval or a rejection, within 90 days of the decision. Appeals come in through the website or through the partner app by the API (ADR 0039), and say why the decision should change.

A different moderator from the one who made the decision reviews the appeal, and records a new moderation decision that names the earlier one in `appeal_of`. The target is a decision within 14 days. Each decision can be appealed once. A contributor who thinks the policy itself is wrong, rather than its application, can propose a change with the "Moderation policy change" issue form, and the steering group hears appeals that turn on what the policy means.

## Vandalism and reverts

Vandalism is a submission made to damage the data: removing true facts, moving records, inserting false safety facts, or spam. Signals include many changes in a short time, changes that remove or weaken safety facts, and text unrelated to the record. Fixed checks and rate limits catch most of it before it reaches a queue.

When vandalism is approved by mistake, a moderator reverts it. A revert is a change without a submission (ADR 0036): it restores the earlier values as a new change with its own sequence number, so the history keeps both the vandalism and the repair and partner apps following the change feed receive the correction. A revert that touches a safety fact is made by a person. Reverting never deletes history from the submission log.

A contributor or API key found vandalising is rate-limited or suspended, and its other recent changes are checked. For a partner app, the suspension applies to the pseudonymous ID, and the partner app is told so it can act on its side. Repeated vandalism through one API key is a matter for the API terms of service.

## Seed sources

Seed sources are imported as submissions with seed source provenance and pass through the same pipeline as everyone else. The registry of seed sources and their re-sync schedules is [docs/seed-sources.md](../seed-sources.md).

**Re-import over a newer community edit.** Provenance is kept per fact ([ADR 0013](../adr/0013-stable-public-ids-and-per-fact-provenance.md)), so a re-import only proposes the facts the seed source holds. When a re-imported value differs from a fact a contributor supplied, and the contributor observed it after the seed source's own update date, the re-import does not replace it automatically: it goes to a person with both values and both dates. When the seed source's update is newer than the contributor's observation, the re-import is an ordinary submission. A re-import never touches a fact the seed source did not supply.

**A seed source drops a record.** A record missing from a later import is never closed automatically, because a dataset can drop rows for reasons unrelated to the place itself. The pipeline submits a problem report for that record, a moderator checks it, and a closure, if warranted, goes through the always-human list like any other. Facts the seed source supplied keep their provenance until someone replaces or confirms them.

**A seed source changes or withdraws its licence.** The import stops at once and the maintainer reviews the new terms. Facts already received under CC BY 4.0 stay licensed, because that licence is irrevocable (section 2(a)(1) of [the licence text](../../LICENSES/CC-BY-4.0.txt)). Whether to keep them is decided case by case, with the publisher's wishes weighed.

## Prompts to confirm stale facts

Facts age. OTWD never removes or hides a fact for being old, because an old fact is often still true and an unknown is worse for a traveller than a dated one. Instead, apps see `observed_on` on every fact and `safety_facts_observed_on` on every compact record, and OTWD prompts contributors to confirm facts older than the suggested age for their kind. A confirmation records new provenance without changing the value, through a submission or the `confirm_facts` change ADR 0036 defines.

| Fact                                                                                           | Suggested age before a prompt     |
| ---------------------------------------------------------------------------------------------- | --------------------------------- |
| Prices, fares, opening hours and reception hours                                               | 12 months                         |
| Drinking water and non-potable water                                                           | 12 months                         |
| Seasonal closure                                                                               | Each year, before the season      |
| Fire policy (`fires_allowed`)                                                                  | 24 months                         |
| Accessibility                                                                                  | 24 months                         |
| Contact details, bookings, stay limits and capacity                                            | 24 months                         |
| Towing permitted, surface and vehicle access class                                             | 24 months                         |
| Ferry vehicle limits and accepted vehicle classes                                              | 24 months                         |
| Rig limits and other facilities                                                                | 36 months                         |
| Vertical clearance, width limit, weight limit and length limit                                 | 60 months, or after any roadworks |
| Fire district (recomputed when the seed source's boundaries change, never prompted by its age) | Not prompted                      |

A suggested age is a minor version change. A prompt goes to partner apps and the website, which may show it to contributors near the record.

## Moderators

Moderators are approved by the steering group ([GOVERNANCE.md](../../GOVERNANCE.md#steering-group)). A moderator does not decide a submission about a record they operate, work for or are paid by, or a submission from someone they know personally, and passes it to another moderator. Moderators see the contributor's pseudonymous ID or display name and the partner app, never more ([the privacy policy draft](privacy-draft.md)).

## History

| Version       | Date            | Change                                                                    |
| ------------- | --------------- | ------------------------------------------------------------------------- |
| `routing-1.0` | 16 October 2026 | First published version, matching the `routing-1.0` used in the examples. |

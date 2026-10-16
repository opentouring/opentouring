---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Open enumerations and a record type registry

Before this decision the public ID pattern, the record type and the submission kinds named only the four record types, and every other list of values in the contract was a closed `enum`. A fifth record type, a new change kind or a new price unit would have broken every consumer that validates against version 1, so none of them could ship before version 2. Once `v1.0.0` is tagged ([ADR 0030](0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)) that would freeze the contract at whatever this review missed.

Every list of values in the contract is now one of three things, and the schema says which.

**Governed lists** stay as they are: site types, facilities, structures, surfaces, vehicle access classes and vehicle classes, proposed by the community with OSM and schema.org mappings, and checked against the list files rather than the schema.

**Open enumerations** are lists the contract itself defines that later minor versions may extend. In the schema each is a string that matches `EnumCode` (lower case letters, digits and underscores) with the values known at that version in `x-otwd-known-values`. Each description states the fallback a consumer applies to a value it does not know. OTWD never sends or accepts a value its own schema version does not list, and `tools/validate.py` applies the keyword to every example, so producers stay strict. A consumer's ordinary JSON Schema validator ignores the unknown keyword and accepts any value that matches the pattern, which is the point: a document from version 1.3 still validates for a consumer built against 1.0.

**Closed enumerations** keep a plain `enum`. A consumer acts on the value directly, so an unknown one cannot be ignored safely, and a new value needs version 2. Where a later need appears, a new optional field or fact carries it, which is an addition.

Record types are open, through a registry. `schema/record-types.json` lists each record type with its geometry, schemas, API path, creation kind, computed facts, the schema version that added it and its ADR, and `GET /v1/record-types` serves it. `RecordId` accepts any snake_case kind segment except the kinds reserved for OTWD's other identifiers (submission, decision, verdict, photo, upload, contributor, partner app, seed source, appeal, API key), and `RecordType` accepts any code. Both carry `x-otwd-registry`, so OTWD and the validator accept only registered record types. The consumer rule is: skip records, changes and bulk downloads of a record type you do not know. A new record type needs an ADR, its schemas, a registry entry, its creation kind and a path, all in one pull request, and the validator reads the record types from the registry instead of a list in its own code.

## The decision for each list

| List                                                                                               | Kind   | A consumer that meets an unknown value                                                                          |
| -------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------- |
| Record type and the kind segment of a public ID                                                    | Open   | Skips the record, change or file                                                                                |
| Change kind                                                                                        | Open   | Fetches the record again, using `changed_fields` to see what moved                                              |
| Change origin ([ADR 0036](0036-record-lifecycle-and-change-origins.md))                            | Open   | Treats the change like any other and fetches the record                                                         |
| Submission kind                                                                                    | Open   | Shows a submission it cannot describe in detail. The API answers 422 to a kind it does not accept               |
| Moderation outcome                                                                                 | Open   | Treats it as not applied, unless the decision lists `change_seqs`                                               |
| Submission status, decided-by kind                                                                 | Open   | Treats the submission as still in progress, and does not name who decided                                       |
| Problem report category                                                                            | Open   | Treats it as `other`                                                                                            |
| Takedown reason, recompute reason                                                                  | Open   | Shows the change without the reason                                                                             |
| Provenance source kind                                                                             | Open   | Treats the source as unnamed and still reads the fact's confidence                                              |
| Verdict category, evidence kind, model tier                                                        | Open   | Treats the category as `needs_human_judgement`, the evidence as text, the tier as `fast`                        |
| Price `applies_to`, `per`, `period`, payment methods                                               | Open   | Shows the price as `other` without a total, and ignores the payment method                                      |
| Limit basis (signed, surveyed, measured, unknown)                                                  | Open   | Treats the figure as `unknown` and still compares a rig with `lowest_m`                                         |
| Bulk download kind and format                                                                      | Open   | Skips the file                                                                                                  |
| Record status                                                                                      | Closed | Not applicable: what to show, and whether to follow `redirect_to`, depends on it                                |
| Name kind, weekday, passage, towing permitted, big rig suitable, charging, fare crossings          | Closed | Not applicable: each is a complete set or a scale an app acts on                                                |
| Pets, bookings, surface condition, signal and the other value enumerations in `values.schema.json` | Closed | Not applicable: a scale or a yes and no answer a filter reads                                                   |
| Facility attribute values                                                                          | Closed | Not applicable: they follow the facility's entry in its governed list                                           |
| Routing route                                                                                      | Closed | Not applicable: only `auto_approval` is constrained, and a new route needs review against the always-human list |

Record status is closed because it decides whether a consumer shows a record, hides it or follows a redirect. A status it did not know would be shown as open or dropped, and neither is safe. The statuses version 1 needs are settled before the tag, including the two that [ADR 0036](0036-record-lifecycle-and-change-origins.md) adds.

## Considered options

- **Keep closed enums and ship version 2 for each addition.** Rejected: each new change kind or record type would force every consumer to move, and `/v1` would have to run beside `/v2` for a year for a change that harms nobody who ignores it.
- **Turn every list into a governed list.** Rejected: governed lists carry labels, translations and OSM mappings and are approved by the steering group. Change kinds and price units are contract mechanics that a pull request with an ADR can extend.
- **Accept any string with no list of known values.** Rejected: OTWD's own output would no longer be checked, and a typo would ship as a new value.
- **Open the record ID with a lookahead in the pattern.** Rejected: JSON Schema patterns use ECMA-262, and regular expression engines without lookaround, such as the one in the Rust `regex` crate, could not run it. A separate `not` against `NonRecordId` works everywhere.

## Consequences

Additions to open enumerations and the record type registry are non-breaking within version 1, as `api/README.md` and `schema/README.md` now say. `schema/examples/consumer/` holds documents from a later minor version (a change to an unregistered record type, a change kind and price values this version does not know). The validator proves each passes the plain validator a consumer would use and fails the strict one on an unknown value, so the rule is tested rather than only written down. Invalid examples prove that OTWD may not send an unknown change kind and that a submission ID cannot stand in for a record ID. SDKs generate open enumerations as a string type with named constants for the known values, never as a closed enum type.

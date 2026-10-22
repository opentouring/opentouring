<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Extending Open Touring

Open Touring will miss things, and every gap is closed the same way: a pull request, reviewed in the open, with the decision recorded where the next person will find it. This guide gives one checklist per kind of change. Each names the files to touch, the review the change needs, who approves it and whether it needs an ADR. Use the terms in [CONTEXT.md](../CONTEXT.md), follow the writing rules and checks in [CONTRIBUTING.md](../CONTRIBUTING.md), and link the pull request to its issue.

## Who approves

**Maintainer.** During the interim arrangement in [GOVERNANCE.md](../GOVERNANCE.md), the maintainer approves every change.

**Steering group.** After the host agreement, the steering group takes over the decisions GOVERNANCE.md gives it: the governed list, moderation policy and appeals, new moderators, the contributor terms and relicensing. In the checklists below, "steering group" means the maintainer until the steering group exists.

**ADR.** A change needs an ADR in [docs/adr/](adr/) when it makes or reverses a decision someone would later ask "why" about: a new record type, a new safety fact, a change to who decides, or anything that contradicts an existing ADR. Number it after the highest number in use, including numbers taken by open pull requests, and give it `status: proposed` until it is accepted. An ADR that replaces another says so, and the old one's status becomes `superseded by ADR NNNN`.

Every pull request uses the [pull request template](../.github/pull_request_template.md), which links back here. Contract changes (anything under `schema/` or `api/`) are a draft until `v1.0.0` ([ADR 0030](adr/0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)). After that tag, a change to the contract is additive or it is a breaking change (see below), and every contract change gets a line in [CHANGELOG.md](../CHANGELOG.md).

## New governed list code

A new site type, facility, structure, surface, vehicle access class or vehicle class.

1. Open an issue with the "Governed list proposal" form. It gets the `governed-list` label and asks for the format in [CONTRIBUTING.md](../CONTRIBUTING.md#proposing-a-governed-list-value).
2. Add the entry to the list file in `schema/` (`site-types.json`, `facilities.json`, `structures.json`, `surfaces.json`, `vehicle-access-classes.json` or `vehicle-classes.json`) with its code, en-AU label, description, `status` `active`, `introduced_in`, `safety_fact`, attributes, and `osm` and `schema_org` mappings, in the format `schema/vocabulary.schema.json` describes.
3. A facility with attributes also gets its own schema in `schema/values.schema.json`. The validator checks the two agree.
4. Update the tables in `schema/mappings/osm.md` and, for site types and facilities, `schema/mappings/schema-org.md` to match the new entry. There is no generator script yet, so edit the tables by hand.
5. Add the term to `CONTEXT.md` when the code introduces a concept the glossary does not hold.
6. Add a valid example that uses the code and, when the code carries a rule (attributes, passages, a rank), an invalid example with its expected error in `schema/examples/invalid/expected.json`.
7. Run `npm run check:schema`.

**Review:** discussion on the issue, then code review of the pull request. **Approves:** the steering group. **ADR:** no, unless the code carries `safety_fact: true`.

A code that carries `safety_fact: true` changes routing: every submission that touches it goes to a person. It meets the higher bar of a new safety fact (below) as well: steering group approval recorded in an ADR, and the moderation policy updated in the same pull request. Codes are never renamed or reused. Retiring one marks it `deprecated`, and it keeps its meaning.

## New translation

A governed list translated into another language ([ADR 0031](adr/0031-governed-lists-and-the-api-are-translatable.md)). Translations live in `schema/i18n/<language>/<list file>`, follow `schema/translation.schema.json`, and are added by the steps in [schema/i18n/README.md](../schema/i18n/README.md), summarised here.

1. Open an issue with the "Translation" form, or go straight to a pull request titled "Governed list: `<language>` translation of `<list>`".
2. Write the labels and descriptions yourself, or check every line of a draft. Unreviewed machine translation is not accepted.
3. Save it as `schema/i18n/<language>/<list file>` with `reference_version` set to the version of the list you translated from.
4. Run `npm run check:schema`. The pull request gets the `governed-list` label.

**Review:** a speaker of the language reviews the text, and the maintainer reviews the file. **Approves:** the maintainer. **ADR:** no. A translation holds text only, so it can never change what a code means or whether it is a safety fact.

## New fact on an existing record type

A new fact, such as a new detail on sites or road segments.

1. Open an issue with the "New fact or record type proposal" form.
2. `schema/values.schema.json`: add the value shape.
3. The record type's full form schema (`schema/site.schema.json`, `schema/road-restriction.schema.json`, `schema/road-segment.schema.json` or `schema/ferry-service.schema.json`): add the fact to `Facts` (wrapped in `Fact`) and to `FactValues` with the same value shape. Add it to `RequiredFacts` only if every record must have it, which is a breaking change after `v1.0.0`.
4. The compact form schema (`schema/<record type>-compact.schema.json`) references `FactValues`, so it usually needs no change. Change it only when the fact feeds a facility read from other facts or a field such as `safety_facts_observed_on`.
5. `schema/submission.schema.json` references `FactValues` too. When the fact is required, add its pointer to the `update_facts` list of facts that cannot be removed.
6. `schema/tools/validate.py`: add any rule JSON Schema cannot express (a cross-field rule, a governed list lookup) to the fact checks table. The validator already checks that `Facts`, `FactValues`, the compact form and submissions agree.
7. `schema/mappings/osm.md` and `schema/mappings/schema-org.md`: map the fact, or say it has no equivalent.
8. `api/openapi.yaml`: add filters to the record type's list endpoint where apps need them. A filter on a fact keeps records where the fact is unknown, and a matching `_known` parameter leaves them out ([api/README.md](../api/README.md#rig-filters)).
9. `schema/README.md`: add the fact to the record type's list of facts. `api/README.md`: describe any new filter.
10. Examples: add the fact to a valid example in the full form and its compact form, and an invalid example for each rule.
11. If a seed source can supply the fact, record the field it comes from in [docs/seed-sources.md](seed-sources.md).
12. Run `npm run check:schema` and `npm run check:api`.

**Review:** maintainer code review. **Approves:** the maintainer, or the steering group when the fact changes moderation. **ADR:** when the fact records something new about the world that needs a reason (as ADR 0026 did for fire districts), when it is a safety fact, or when it changes how facts are shared between record types.

## New record type

A new kind of record beside sites, road restrictions, road segments and ferry services, as [ADR 0027](adr/0027-road-restrictions-road-segments-and-ferry-services-as-record-types.md) added three.

1. Open an issue with the "New fact or record type proposal" form, and write the ADR first. It explains why the thing is not a site type or a fact on an existing record type.
2. `schema/common.schema.json`: add the code to `RecordType`, an ID definition (`<CamelCase>Id`, pattern `otwd:<code>:<ULID>`) and the ID to `RecordId`.
3. New `schema/<record-type>.schema.json` (with `Facts`, `FactValues`, `RequiredFacts` and the safety fact markers) `schema/<record-type>-compact.schema.json`, built on `FullRecord` and `CompactRecord`, and `schema/<record-type>-repository.schema.json`, a copy of another record type's with the names changed. Add all three to the entry in `schema/record-types.json`.
4. `schema/submission.schema.json`: a `new_<code>` creation kind. `schema/moderation-decision.schema.json`: the kind in `submission_kind`. `schema/change.schema.json`: the record type in changes.
5. `schema/tools/validate.py`: add a `RecordType` to `RECORD_TYPES`. Schema file names, document suffixes and the creation kind follow from its code.
6. Any new governed lists, with their entries, mappings and the list name in `GOVERNED_LISTS` in the validator.
7. `api/openapi.yaml`: list and get endpoints, the bulk download `record_type`, change feed filters. `api/README.md` and `schema/README.md`: the new record type in every section that lists them.
8. `CONTEXT.md`: the record type and its terms. `docs/architecture.md`: anything it changes in the pipeline, such as a new fixed check.
9. Valid and invalid examples for every rule, including the always-human rules for the new creation kind.
10. Update the moderation policy when the record type brings new safety facts.

**Review:** maintainer code review of every file, and a design review of the ADR. **Approves:** the steering group. **ADR:** yes.

## New safety fact

Marking a fact, facility or site type as a safety fact. The designation changes routing: every submission that touches it goes to a person ([ADR 0010](adr/0010-ai-recommends-fixed-code-routes-humans-decide.md)), and the always-human list follows from the markers, never from a flag routing sets.

1. Write an ADR that names the fact and the harm a wrong value could cause a traveller, as ADR 0026 and ADR 0027 do.
2. Mark it: `"x-otwd-safety-fact": true` in the record type's full form schema, or `safety_fact: true` in the governed list entry.
3. Add it to the safety fact definition in `CONTEXT.md` and the list in `schema/README.md`.
4. Add an invalid moderation decision example where a routing rule decides a submission touching it, with its expected error.
5. Update [the moderation policy](policies/moderation.md) and bump its version.

**Review:** maintainer code review and an open comment period on the pull request of at least 14 days once a steering group exists. **Approves:** the steering group, recorded in the ADR. **ADR:** yes. Removing a safety fact designation follows the same steps and needs the same approval.

## New seed source

An open dataset imported as submissions with seed source provenance.

1. Open an issue with the "Seed source proposal" form.
2. Check licence compatibility, and record the answers in the issue:
   - The licence is CC BY 4.0, CC BY 3.0 AU, CC0 or written permission to republish under CC BY 4.0. A licence with non-commercial, no-derivatives, share-alike or no-sublicensing terms is not compatible.
   - The licence is stated on the publisher's own catalogue page, and no other terms on that page or the publisher's site conflict with it.
   - The data contains no OpenStreetMap-derived data ([ADR 0003](adr/0003-no-openstreetmap-data-import.md)) and no material the publisher says comes from third parties under other terms.
   - The attribution the publisher requires is known, word for word.
   - The data holds no personal information, or the fields that hold it are dropped before import.
3. Add the source to [docs/seed-sources.md](seed-sources.md) and to `schema/seed-sources.json`, the registry `GET /v1/seed-sources` serves, with its ID (`otwd:seed_source:<slug>`), publisher, URL, licence, attribution text, the facts it supplies and its re-sync schedule.
4. The pipeline in `pipelines/` submits through the submission log like any contributor and never writes live data. Re-syncs follow the seed source rules in [the moderation policy](policies/moderation.md#seed-sources).

**Review:** a licence review by a second person on the issue, then code review of the pipeline. **Approves:** the maintainer, or the steering group for a source whose licence needed interpretation. **ADR:** no, unless the source is the first for a new country or record type.

## New country

Bringing a country into supported service. Follow the onboarding checklist in [docs/supported-countries.md](supported-countries.md#onboarding-a-new-country).

**Review:** the checklist items, each signed off on the tracking issue. **Approves:** the steering group. **ADR:** yes, as [ADR 0024](adr/0024-one-state-first.md) records the first state.

## Changed moderation rule

A change to what goes to a person, the auto-approval criteria, appeals, re-verification ages or any other rule in [the moderation policy](policies/moderation.md).

1. Open an issue with the "Moderation policy change" form.
2. Edit `docs/policies/moderation.md` and bump its version as its versioning section says. A change to routing code ships in the same release as the policy version it implements.
3. Add the version and a one-line reason to the policy's change history.

**Review:** an open comment period on the pull request of at least 14 days once a steering group exists. **Approves:** the steering group ([ADR 0040](adr/0040-moderation-policy-is-a-versioned-public-document.md)). **ADR:** no for a rule change within the policy. Yes for a change that contradicts an ADR, such as letting a routing rule decide a safety fact.

## Breaking change after v1.0.0

Removing or renaming a field, code or endpoint, changing a field's meaning, or making an optional field required.

1. Write an ADR that explains why an additive change cannot do the job.
2. Publish the new contract as version 2: schemas under the `https://schema.opentouring.org/otwd/v2/` base and endpoints under `/v2`, as [schema/README.md](../schema/README.md#versioning) and [api/README.md](../api/README.md#versioning) set out. `/v1` keeps running beside it for at least 12 months after `/v2` is released.
3. Mark the `/v1` operations that go away as deprecated in `api/openapi.yaml` and announce the shutdown date with the `Deprecation` and `Sunset` headers, as the Versioning section of [api/README.md](../api/README.md#versioning) sets out ([ADR 0035](adr/0035-open-enumerations-and-a-record-type-registry.md)).
4. Add a CHANGELOG.md entry with the change, the reason, the migration steps and the `/v1` shutdown date.
5. Tell every partner app by the contact on its API key, at least 12 months before `/v1` stops.

**Review:** maintainer code review and an open comment period of at least 30 days, with partner apps invited to comment. **Approves:** the steering group. **ADR:** yes.

## New API endpoint

1. Open an issue that names the question the endpoint answers and why an existing endpoint and filter cannot answer it.
2. `api/openapi.yaml`: the path, `operationId`, parameters, responses and problem types, with bodies referencing `schema/`.
3. Review it against this list:
   - It follows the conventions in [api/README.md](../api/README.md): `OTWD-API-Key`, cursor pagination, ETags, RFC 9457 errors, rate limit headers.
   - It writes nothing to live data. Writes go through `POST /v1/submissions` and reach the data repository only as a pull request after screening ([ADR 0046](adr/0046-live-data-in-a-public-git-repository-per-country.md)).
   - The website would use it through the public API like any partner app ([ADR 0023](adr/0023-the-website-is-just-another-api-client.md)).
   - It exposes no contributor identity beyond what [the privacy policy draft](policies/privacy-draft.md) allows.
   - The tier it needs is stated, and anything on the contribute path is free ([ADR 0008](adr/0008-free-api-key-required-even-for-bulk-downloads.md)).
   - A moderator-only endpoint says so and how it is restricted.
4. `api/README.md`: describe it. CHANGELOG.md: add it under the next release after `v1.0.0`.
5. Run `npm run check:api`.

**Review:** maintainer code review. **Approves:** the maintainer. **ADR:** when the endpoint changes a decision, such as exposing data an ADR keeps private.

---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Contributor identity in published data

Published provenance carried a contributor ID on every fact a contributor supplied, and every fact and change named its submission. The same contributor ID on facts at many records, each with an observed date and a location, would let anyone with a bulk download rebuild where that person had been and when. That is a travel history, and it is personal information whether or not a name is attached. Submission IDs add to it, because a ULID records the moment it was minted.

## Guidance this follows

The OAIC's guidance on de-identification says information is de-identified when it is "no longer about an identifiable (or reasonably identifiable) individual", and that "the risk of re-identification in the data access environment must be very low" ([De-identification and the Privacy Act](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/handling-personal-information/de-identification-and-the-privacy-act)). Open data under CC BY 4.0 has the widest possible data access environment: anyone, combined with anything. The APP guidelines ask entities to "limit collection of personal information to the minimum amount necessary in the circumstances" ([APP 3](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-3-app-3-collection-of-solicited-personal-information)), to "take such steps as are reasonable in the circumstances to protect the personal information it holds from misuse, interference and loss, as well as unauthorised access, modification or disclosure", and to destroy or de-identify personal information that is no longer needed ([APP 11](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-11-app-11-security-of-personal-information)).

OTWD's schema is global, so it also follows the GDPR's definition. Pseudonymisation is processing so that data "can no longer be attributed to a specific data subject without the use of additional information, provided that such additional information is kept separately and is subject to technical and organisational measures" (GDPR Article 4(5), [text](https://gdpr-info.eu/art-4-gdpr/)). The EDPB's Guidelines 01/2025 on Pseudonymisation (adopted 16 January 2025, the version for public consultation, [PDF](https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf)) add that pseudonymised data "is to be considered information on an identifiable natural person, and is therefore personal", name keyed one-way functions "like HMACs" as suitable building blocks (paragraph 107), describe a "pseudonymisation domain" in which attribution is to be precluded, describe relationship pseudonyms, kept consistent only within one relationship (paragraphs 117 and 118), and describe transaction pseudonyms, which give the same person a different pseudonym for each interaction and so prevent "unlawful or unauthorised linkage" (paragraph 119).

## Decision

Privacy first: published data carries the least identifying provenance that still works, and no contributor identifier at all, because no published feature needs one.

- **What is published.** A fact's provenance names its `source_kind`, the partner app (`partner_app_id`) or the seed source, `observed_on` as a local date, `recorded_at`, `confidence` and the `change_seq` that set it. A direct contributor appears as `source_kind` contributor and, only if they opted in on their account (off by default), their `display_name`. The `observed_on` precision stays a date: it is what a traveller needs to judge freshness, and a time of day would add to the travel history.
- **What is never published.** Contributor IDs, pseudonymous IDs, submission IDs, upload IDs, API key IDs, moderator IDs, the moment a contributor made a submission (`contributor_submitted_at`), and any per-record stand-in for a contributor. Provenance drops `contributor_id`, `submission_id` and `decision_id`. Changes drop `submission_id` and keep `decision_id`, which identifies a moderation act and lets a consumer group the changes one decision produced, such as a merge. A partner app matches its own submissions to the change feed through `change_seqs` in their status, which only it can read.
- **Confirmations without identities.** The one feature that needs to tell contributors apart is counting confirmations ([ADR 0036](0036-record-lifecycle-and-change-origins.md)). OTWD counts different contributors privately and publishes the count, so a per-record ID is not needed for it.
- **The identity link stays private.** OTWD keeps who supplied each fact, as contributor ID and, for a partner app's contributor, partner app and pseudonymous ID, in the submission log. Moderation, trust scores, per-contributor rate limits ([ADR 0039](0039-partner-api-keys-tokens-and-abuse.md)), appeals and abuse handling use it, through the moderator endpoints and nothing public. How long it is kept, and how it is protected and deleted, belongs in the privacy policy, drafted at `docs/policies/privacy-draft.md`.
- **Photos.** A photographer's credit is optional and chosen per photo. Without one the photo is credited "Open Touring contributor" ([ADR 0037](0037-structured-attribution-and-photo-licences.md)). Apps are told that a name repeated across photos links them.

If a future feature needs to show which facts on one record came from the same contributor, it may publish only a per-record contributor reference, derived as a keyed HMAC of the contributor ID and the record's public ID with a secret held only by OTWD, so the same contributor has unrelated references on different records and the reference cannot be reversed or joined across records without the key. That is a relationship pseudonym in the EDPB's terms, with each record as its own pseudonymisation domain. It needs its own ADR, which must name the feature, the key's custody and rotation, and the re-identification test it passed.

## Making sure it works

The schema leaves no place for an identifier: `Provenance` and `change.schema.json` close their properties, and `display_name` is allowed only for `source_kind` contributor. The validator goes further for every published document kind (both record forms, which are also the rows of GeoParquet and GeoJSON bulk downloads, and changes, which are also webhook payloads and delta file entries). It walks every key and string, and fails any `contributor_id`, `pseudonymous_id`, `submission_id`, `moderator_id` or `api_key_id` key, and any string holding an `otwd:contributor:`, `otwd:submission:`, `otwd:upload:` or `otwd:api_key:` identifier. A future free-text or extension field cannot carry one either. Invalid examples prove a contributor ID in provenance, a submission ID in a change, a display name on a partner app's fact, and a contributor ID pasted into a description all fail. The valid examples show what is published: partner app provenance, seed source provenance, and a direct contributor with an opted-in display name on a photo.

## Considered options

- **Per-record opaque contributor IDs in all published provenance.** Rejected for now: it was the earlier proposal, and it does prevent rebuilding a travel history across records. But no published feature needs it, so publishing it would collect and disclose more than the minimum. The derivation above is ready if a feature does.
- **One stable public contributor ID.** Rejected: it is the travel history problem itself.
- **Coarsen observed_on to a month.** Rejected: travellers need to know a fact was seen last week rather than last season, and with no contributor identifier a date alone does not link records.
- **Hide the partner app too.** Rejected: consumers weigh facts by the app they came through, and attribution and trust work at the app level. The partner app is an organisation, not a person.

## Open questions

- A partner app with very few contributors makes its `partner_app_id` close to identifying, because its facts at different records with their dates may all be one person's. Whether to hold back `partner_app_id`, or delay publishing, until an app has enough active contributors, and what number is enough, is for the privacy policy and needs a re-identification test against real volumes.
- Whether the operator is an APP entity under the Privacy Act, given the small business exemption, is for the legal review the contributor terms already need. This decision follows APP 3 and APP 11 either way.
- The EDPB guidelines cited are the version adopted for public consultation. Check the final version when it is published.

## Consequences

`ContributorId` is private by definition, and every example's provenance lost its contributor, submission and decision IDs. The contributor terms draft now says what is published and what is kept privately. The docs on moderation and privacy refer to the identity link by that name.

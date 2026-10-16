---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Structured attribution, a seed source registry and photo licences

A record's attribution list was a list of strings, and every photo had to be CC BY 4.0. A string cannot say which licence a credit is under, link to the licence or the source, or carry the notice of changes that CC BY licences ask for, so a partner app could not show credits correctly without parsing prose. A photo from a seed source under another compatible licence could not be represented at all.

## What the licences ask for

The CC BY 4.0 legal code, section 3(a)(1), asks anyone who shares the material, "including in modified form", to retain the creator's identification, a copyright notice, a notice referring to the licence and to the disclaimer, and a URI or hyperlink to the material "to the extent reasonably practicable", to "indicate if You modified the Licensed Material and retain an indication of any previous modifications", and to indicate the material is licensed under CC BY 4.0 with the licence text or its URI. Section 3(a)(2) allows these conditions to be met "in any reasonable manner based on the medium, means, and context" ([CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)).

The CC BY 3.0 Australia legal code, section 4B, asks for the name or pseudonym of the original author and any attribution parties, the title of the work if supplied, and the URI the licensor specifies "to the extent reasonably practicable". For a derivative work, "You must take reasonable steps to clearly identify that changes were made to the Work" ([CC BY 3.0 AU legal code](https://creativecommons.org/licenses/by/3.0/au/legalcode)). Several Australian road datasets OTWD plans to seed are under CC BY 3.0 AU (`docs/research/road-and-ferry-data.md`).

OTWD always changes seed source data: it maps the source's fields to OTWD's codes and value shapes and combines them with contributor reports. So every credit for a seed source under a CC BY licence carries a changes notice.

## Decision

**Attribution entries are objects.** Each has `text` (the credit to show), `licence` (an SPDX identifier), and optionally `licence_url`, `source_url`, `seed_source` (the registry ID) and `changes`. The schema requires `changes` on an entry for a seed source whose licence is a CC BY licence, and `prefixItems` fixes the first entry as the Open Touring credit. The validator also checks that each seed source is credited once. `SeedSourceRef` in full-form provenance gains `licence_url` and `changes` under the same rule. The page-level `attribution` string in API list responses stays a plain credit line.

**A seed source registry.** `schema/seed-sources.json`, validated by `seed-sources.schema.json` and served at `GET /v1/seed-sources` with each source's last sync, lists every seed source with its dataset, publisher, licence, credit, changes notice, the publisher's own dataset record, the record types it seeds and a status (candidate, active, blocked, retired, as in `docs/seed-sources.md`). Each entry has a licence review, and the schema refuses an active source whose review is not confirmed with a date: a maintainer must check the licence and the exact attribution the publisher asks for on the publisher's own record before the first import. It holds the same sources, IDs and statuses as the table in `docs/seed-sources.md`, which carries the prose (re-sync schedules, what each source supplies), and the two change together. Every entry starts pending review, and the two sources with an unconfirmed licence are blocked with `LicenseRef-unconfirmed` as their licence.

**Photos carry their licence.** `Photo.licence` is an open enumeration ([ADR 0035](0035-open-enumerations-and-a-record-type-registry.md)) of SPDX identifiers compatible with publishing in OTWD, known today as `CC-BY-4.0`, `CC0-1.0` and `CC-BY-3.0-AU`. A contributor licenses their own photo under CC BY 4.0 by default, or CC0 1.0 if they choose, and `add_photo` accepts only those two. A photo from a seed source keeps the source's licence and credit, with `source_url` and `changes`, and the validator checks its licence matches its provenance's seed source. `licence_url` travels with every photo. A contributor's photo credit is now optional: without one it is credited "Open Touring contributor" ([ADR 0038](0038-contributor-identity-in-published-data.md)).

## Considered options

- **Keep strings and add a parallel list of licences.** Rejected: the two lists could drift apart, and the changes notice would still have nowhere to go.
- **One attribution entry per fact.** Rejected: the full form already carries the seed source on each fact. The compact form needs one credit per source, once.
- **Allow any SPDX licence on photos.** Rejected: OTWD republishes photos as part of a CC BY 4.0 dataset, so only licences checked as compatible belong in the known list. Share-alike and non-commercial licences are left out.
- **Store the attribution text only in the registry and refer to it by ID.** Rejected for records: a bulk download or a cached record must be able to show its credits without another request. The registry is the source the API copies from.

## Open questions

- Whether resizing a photo and removing its location data counts as a modification CC BY 4.0 asks a reuser to indicate. Section 2(a)(4) permits technical modifications, and this decision does not rely on reading it either way: every photo from a seed source states its changes, which costs nothing.
- The exact credit wording each publisher in the registry asks for. Each entry's licence review records it once a maintainer confirms it from the publisher's own record.

## Consequences

Every compact example's attribution is now structured, every seed source reference under CC BY states its changes, a seed source photo appears in the national park example, and invalid examples prove that a CC BY seed source credit must state its changes, that the list must lead with the Open Touring credit, that plain string credits fail, and that a seed source photo cannot be relicensed. Partner apps render credits from fields rather than parsing text.

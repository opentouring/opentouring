<!-- SPDX-License-Identifier: Apache-2.0 -->

# OTWD API, version 1

`openapi.yaml` is the OpenAPI 3.1 description of the OTWD API. Request and response bodies reference the JSON Schema in `../schema/` directly, so the spec and the data contract cannot drift apart. SDKs and the developer portal's reference pages are generated from this file.

Lint it with:

```sh
npx @redocly/cli lint api/openapi.yaml
```

Redocly resolves the relative references into `../schema/`. To produce a single self-contained file for tools that cannot follow them, run `npx @redocly/cli bundle api/openapi.yaml -o openapi.bundled.yaml`.

## Record types

The record type registry (`GET /v1/record-types`, from `schema/record-types.json`) lists every record type with its geometry, schemas and path, and a minor version can add one. The API serves four record types today, with the same conventions: sites (`/v1/sites`), road restrictions (`/v1/road-restrictions`), road segments (`/v1/road-segments`) and ferry services (`/v1/ferry-services`). Each has a list endpoint and a get endpoint by public ID, the compact and full views, ETags, 301 redirects for merged records, closures, photos, bulk downloads, change feed coverage and submissions, and the sections below describe them for every record type. Sites and road restrictions are points, and road segments and ferry services are lines. OTWD serves no map tiles.

## Finding records along a route

The road restriction, road segment and ferry service lists take `route`, the route's geometry encoded in Google's Encoded Polyline Algorithm Format (precision 5), and `corridor_m`, the corridor either side of it to search (30 m by default, 5,000 m at most). Results are ordered by how far along the route they are first met, and `route_positions_km` gives that distance for each record. Simplify a route to about 50 m tolerance before encoding it, and split a route that is too long for one query string into legs. OTWD never stores a route. `bbox` and `near` work as they do for sites.

## Rig filters

`rig_length_m`, `rig_height_m`, `rig_width_m`, `rig_weight_t` and `rig_axle_load_t` describe the rig the same way on every list endpoint, and each is compared with the record type's matching limit. A vertical clearance or width limit is compared using `lowest_m`, the lowest figure of any basis, so a measured figure below the sign counts.

| Endpoint                             | Question it answers               | A recorded limit below the rig | No recorded limit                                                |
| ------------------------------------ | --------------------------------- | ------------------------------ | ---------------------------------------------------------------- |
| Sites, road segments, ferry services | Which of these can my rig use?    | Left out                       | Kept, unless `rig_limits_known=true`                             |
| Road restrictions                    | Which of these would stop my rig? | Returned                       | Not returned, so an empty result is not proof the route is clear |

Road restrictions answer the opposite question because they are the obstacles themselves. Other filters follow one pattern: a filter on a fact keeps records where the fact is unknown, and the matching `_known` parameter (`rig_limits_known`, `vehicle_access_class_known`, `towing_permitted_known`) leaves them out. On road segments, `vehicle_access_class` keeps segments a vehicle of that class can use, `towing_permitted` keeps segments with one of the listed values and `has_seasonal_closure` keeps segments with or without a seasonal closure. On ferry services, `vehicle_class` keeps services that carry every listed class.

## Authentication

Every request carries an API key in the `OTWD-API-Key` header, including bulk downloads and the governed lists. Keys are free from the developer portal. The key identifies the partner app, so submissions do not repeat it, and it sets the tier: the change feed, the `changeApplied` webhook and delta files need a paid tier, and a free key gets 403 with problem type `tier-required`. Submitting is free on every tier, and so is the `submissionDecided` webhook that reports the outcome of your own submissions. During the Preview, keys outside the maintainers' own get 403 with problem type `contributions-closed` on the submission endpoints.

## Versioning

Until version 1.0.0 is released, the schema and the API are a draft. Release means a `v1.0.0` tag on this repository, made before any partner app outside the project integrates ([ADR 0030](../docs/adr/0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)). Before that tag, any field, code or endpoint can change or be removed without a new major version, and documents carry `schema_version` `1.0`. From the tag on, the rules below apply.

The major version is in the path (`/v1`). Within v1, changes are additive only: new endpoints, new optional query parameters, new optional response fields, new governed list codes, new values of open enumerations and new record types in the registry. Clients must ignore response fields and codes they do not recognise.

Open enumerations ([ADR 0035](../docs/adr/0035-open-enumerations-and-a-record-type-registry.md)) are the lists of values a minor version can extend: change kinds and origins, submission kinds and statuses, moderation outcomes, problem categories, price units, limit bases and bulk download kinds and formats, among others. In the schema each lists its known values in `x-otwd-known-values` and says what to do with an unknown one. Generate them as strings with named constants, never as closed enum types, or your client will fail on the first new value. Record status, towing permitted and the other closed enumerations change only in `/v2`. Record types are open too: `GET /v1/record-types` lists them, and a client skips records, changes and downloads of a type it does not know. A breaking change ships as `/v2` with schema version 2, and `/v1` keeps running alongside it for at least 12 months after `/v2` is released. Each response body that is a record carries its `schema_version`.

## Languages

The governed list endpoints (`/v1/site-types`, `/v1/facilities`, `/v1/structures`, `/v1/surfaces`, `/v1/vehicle-access-classes` and `/v1/vehicle-classes`) honour `Accept-Language` ([ADR 0031](../docs/adr/0031-governed-lists-and-the-api-are-translatable.md)). Labels and descriptions are written in en-AU, the reference language, and translated by contributors in `schema/i18n`. The API picks the best match for the header, and a label or description with no translation falls back from the requested tag to its base language (de-AT to de) and then to en-AU, so nothing is blank. The response's `language` field and `Content-Language` header name the language served, an entry that fell back names its own language in `label_lang` or `description_lang`, and `Vary: Accept-Language` keeps caches apart. Without the header the lists are served in en-AU.

Record responses, the change feed and webhooks are the same in every language. They carry codes, which you label from the governed lists in the traveller's language, and free text (names, descriptions, notes) as `LocalisedText` in the language the contributor wrote, with its `lang` tag. If your app shows a machine translation of free text, mark it as machine translated, and never send it back in a submission: a description must be the contributor's own words.

## Time

Every instant the API sends or accepts, in records, the change feed, webhook payloads and query parameters such as `updated_since`, is RFC 3339 in UTC with the `Z` suffix (`Timestamp`), and any other offset is rejected ([ADR 0032](../docs/adr/0032-utc-for-instants-local-time-for-schedules.md)). Show instants in the reader's own time zone. Opening hours, ferry operating hours, check-in times and seasonal closures are local clock times and dates, read in the record's `time_zone`, or in the schedule's own `time_zone` when a line record crosses into another zone. Never convert them to UTC for storage: convert them for a given date when you need to compare them with an instant.

## Compact and full forms

Record endpoints return the compact form (`view=compact`, the default): plain values plus an `attribution` list, `min_confidence` and `safety_facts_observed_on`. Add `view=full` to get every fact with its provenance. `../schema/README.md` explains the two forms.

Every list endpoint also answers `Accept: application/geo+json` with a GeoJSON FeatureCollection of compact records, ready for a map layer: Point features for sites and road restrictions, LineString or MultiLineString features for road segments and ferry services.

## Pagination

List endpoints use cursor pagination. A page has `data` and `next_cursor`. Pass `next_cursor` back as `cursor` with the same filters to get the next page, and stop when it is null. Cursors are opaque and expire after 24 hours. The `Link` header carries the same next page as an RFC 8288 link with `rel="next"`. `limit` sets the page size, 100 by default and 500 at most.

The change feed pages by sequence number instead of a cursor, because the sequence number is also your sync position: store `next_after_seq` and send it as `after_seq` next time.

## Caching and ETags

Record, governed list and download list responses carry `Cache-Control` and an `ETag`. A record's ETag changes exactly when its `change_seq` changes. Send the ETag back in `If-None-Match` and the API answers 304 with no body when nothing changed. Responses may be served by the CDN, stale for a short while during revalidation (`stale-while-revalidate`), and change events purge them.

## Merged, replaced and retracted records

A record's public ID never changes and is never reused, but the record can become a stub ([ADR 0036](../docs/adr/0036-record-lifecycle-and-change-origins.md)). The get endpoint of every record type answers 301 for a merged record (a duplicate of another record of the same type) and for a replaced record (one that turned out to be another record type, such as a low bridge recorded as a site), with `Location` set to the record that took its place and the same query string, plus a small JSON body naming `redirect_to`. Update the ID you store when you follow it, and skip it if it names a record type you do not know. A retracted record, one that should never have been published, answers 410: remove it from your copy. Stubs are never listed.

The change feed announces each of these: `record_merged` with `merged_into`, `record_replaced` with `replaced_by` and `record_retracted`. A wrong merge is undone as `record_unmerged`, which brings the stub back as a record with its own facts. A record that described two things is split with `record_split`: it keeps its ID and part of its facts, and each new part arrives as a `record_created` naming it in `split_from`.

Every change also has an `origin`. Most apply a submission. A `revert` undoes the change named in `reverts_seq`, a `takedown` removes content for the reason in `takedown_reason`, never naming who asked, and a `recompute` updates derived values with `derived_updated`, for example after a boundary dataset changes. Treat all of them like any other change: fetch or patch the record.

## Submissions

`POST /v1/submissions` takes a document that validates against `submission.schema.json` and answers 202 with a `submission_id`, a `status_url` and a `Location` header. A submission never changes live data directly: it passes fixed checks, AI review and routing, and only an approving moderation decision turns it into a change. Follow the outcome with `GET /v1/submissions/{submission_id}` or the `submissionDecided` webhook. The status response gives the outcome, the public note for the contributor, reason codes and the resulting change sequence numbers, without exposing moderators or verdicts.

Before submitting for a contributor, a partner app must have their acceptance of the contributor terms and send it in `consent`. Identify the contributor with a stable pseudonymous ID that means nothing outside your app (`contributor.kind` pseudonymous), or with their OTWD contributor ID if they signed in to Open Touring (`contributor.kind` direct). Never send names or email addresses: the schema rejects an `@` in a pseudonymous ID.

Each record type has its own creation kind: `new_site`, `new_road_restriction`, `new_road_segment` and `new_ferry_service`. The kinds about an existing record (`update_facts`, `confirm_facts`, `add_photo`, `report_closure`, `request_merge`, `request_unmerge`, `request_split`, `request_replacement`, `report_problem`) name it in `record_id`, and the facts allowed depend on its record type, which the ID's kind segment gives. New records of every type, closures, merges, unmerges, splits, replacements and any submission that touches a safety fact, including a confirmation of one, always go to a moderator.

`confirm_facts` reports that facts the contributor saw on the ground are still true, as the record showed them at `base_change_seq`. It changes no value: it adds to each fact's confirmations, which count distinct contributors, and raises its confidence. Use it when a contributor checks a site and everything still matches, because a fact confirmed recently is worth more to the next traveller than one nobody has looked at for years.

Photos are uploaded first, and a photo can be of any record, such as a site or the clearance sign at a road restriction. `POST /v1/photo-uploads` returns a short-lived upload URL on the API host and an `upload_id`. PUT the file to that URL: the API checks its size, type and SHA-256 and strips EXIF location data before it writes the file to storage, and the URL is never a presigned storage URL. Then send an `add_photo` submission naming the `upload_id`.

### Idempotency keys

`POST /v1/submissions` and `POST /v1/photo-uploads` require an `Idempotency-Key` header, following the IETF Idempotency-Key header draft. Use a new random value, such as a UUID, for each logical submission, and reuse it on every retry of that submission, for example after a timeout or when an app sends a queue of submissions made offline. A repeat with the same key and the same body returns the original response with `Idempotent-Replayed: true` and creates nothing new. The same key with a different body returns 422. A repeat that arrives while the first request is still being processed returns 409. Keys are kept for 24 hours.

### Conflicts and base_change_seq

Every record has a `change_seq`: the sequence number of the latest change applied to it, and every fact records the `change_seq` that last set it. Submissions that edit or confirm a record (`update_facts`, `confirm_facts`, `report_closure`, `request_merge`, `request_unmerge`, `request_split`, `request_replacement`) must send `base_change_seq`, the record's `change_seq` as the contributor saw it.

The check is per fact. When every fact the submission touches is unchanged since `base_change_seq`, it is accepted even if other facts on the record changed in the meantime. When a touched fact did change, the API answers 409 with `current_change_seq` and `conflicting_fields` (JSON Pointers such as `/facts/prices`). Fetch the record again, show the contributor the newer values, and submit again with the new `base_change_seq` if they still want the change. This keeps two contributors from overwriting each other without either of them seeing the other's report.

## Change feed and webhooks

`GET /v1/changes` lists changes to every record type in sequence order after `after_seq`. Each change names its record in `record_id`. Filter with `record_id` or `record_type`. Sequence numbers are global and only increase, but they may have gaps, so never count on seq + 1. Each change gives the record's `previous_seq`: when it differs from the `change_seq` you hold for that record, you missed a change and should fetch the record again. When `after_seq` is older than the retained feed the response is 410, and you should restart from the latest full bulk download, whose `to_seq` tells you where to resume.

Any key can register a webhook endpoint in the developer portal for `submissionDecided`, which is free on every tier because it belongs to the contribute path. `changeApplied` needs a paid tier, like the change feed it mirrors. Deliveries follow the Standard Webhooks scheme: headers `webhook-id`, `webhook-timestamp` and `webhook-signature`, an HMAC-SHA256 signature over the ID, timestamp and raw body, at-least-once delivery with retries for 3 days, and the same `webhook-id` on every retry so you can deduplicate. Verify the signature and reject timestamps more than 5 minutes old. The change feed stays the source of truth for anything a webhook missed.

## Bulk downloads

`GET /v1/downloads` lists the files available to the key, one record type per file (filter with `record_type`): full downloads (GeoParquet in the compact form, GeoJSON and GeoJSON Text Sequences in the full form) and, on paid tiers, delta files covering the changes between `from_seq` and `to_seq`. URLs are signed for the key and expire, and every file has a `sha256` to verify. Load the latest full download, then follow the change feed or apply delta files from its `to_seq`.

## Rate limits

Responses carry the `RateLimit` and `RateLimit-Policy` header fields from the IETF RateLimit header fields draft, for example `RateLimit-Policy: "default";q=1000;w=60` and `RateLimit: "default";r=812;t=34`. When a limit is used up the API answers 429 with `Retry-After` in seconds. Limits depend on the tier and are set per API key.

## Errors

Errors use RFC 9457 problem details with content type `application/problem+json`. `type` is a URI under `https://opentouring.org/problems/` that identifies the problem and documents it, `title` and `status` are always present, and `request_id` identifies the request in OTWD's logs. Validation errors (422) add an `errors` list of JSON Pointers into the request body with a message for each, and conflicts (409) add `current_change_seq` and `conflicting_fields`.

## Attribution and licences

OTWD data is CC BY 4.0. Show "Data: Open Touring contributors, opentouring.org, CC BY 4.0" wherever OTWD data appears, plus every credit in a record's `attribution` list and each photo's own credit. The spec itself and the JSON Schema are Apache-2.0.

Each `attribution` entry is structured ([ADR 0037](../docs/adr/0037-structured-attribution-and-photo-licences.md)): `text` to show, `licence` as an SPDX identifier, `licence_url`, `source_url` where the licence asks for a link, `seed_source` naming the registry entry, and `changes`, the notice of changes OTWD made, which every seed source under a CC BY licence has. The first entry is always the Open Touring credit. Render them in your own layout, for example as "Contains Vicmap Transport data, Department of Transport and Planning (Victoria), CC BY 4.0, modified: mapped to OTWD codes and combined with contributor reports", with the licence name linked to `licence_url`. `GET /v1/seed-sources` lists every seed source with its licence, credit, licence review and last sync.

Photos carry their own `licence`, `licence_url` and `attribution`. A contributor's photo is CC BY 4.0, or CC0 1.0 if they chose it, credited as they asked or as "Open Touring contributor". A photo from a seed source keeps that source's licence and credit, links to where it was published in `source_url`, and states the changes OTWD made in `changes`.

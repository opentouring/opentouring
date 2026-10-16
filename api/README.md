<!-- SPDX-License-Identifier: Apache-2.0 -->

# OTWD API, version 1

`openapi.yaml` is the OpenAPI 3.1 description of the OTWD API. Request and response bodies reference the JSON Schema in `../schema/` directly, so the spec and the data contract cannot drift apart. SDKs and the developer portal's reference pages are generated from this file.

Lint it with:

```sh
npx @redocly/cli lint api/openapi.yaml
```

Redocly resolves the relative references into `../schema/`. To produce a single self-contained file for tools that cannot follow them, run `npx @redocly/cli bundle api/openapi.yaml -o openapi.bundled.yaml`.

## Authentication

Every request carries an API key in the `OTWD-API-Key` header, including bulk downloads and the governed lists. Keys are free from the developer portal. The key identifies the partner app, so submissions do not repeat it, and it sets the tier: the change feed, the `changeApplied` webhook and delta files need a paid tier, and a free key gets 403 with problem type `tier-required`. Submitting is free on every tier, and so is the `submissionDecided` webhook that reports the outcome of your own submissions. During the Preview, keys outside the maintainers' own get 403 with problem type `contributions-closed` on the submission endpoints.

## Versioning

The major version is in the path (`/v1`). Within v1, changes are additive only: new endpoints, new optional query parameters, new optional response fields, and new site type and facility codes. Clients must ignore response fields and codes they do not recognise. A breaking change ships as `/v2` with schema version 2, and `/v1` keeps running alongside it for at least 12 months after `/v2` is released. Each response body that is a site carries its `schema_version`.

## Compact and full sites

Site endpoints return the compact form (`view=compact`, the default): plain values plus an `attribution` list, `min_confidence` and `safety_facts_observed_on`. Add `view=full` to get every fact with its provenance. `../schema/README.md` explains the two forms.

`GET /v1/sites` also answers `Accept: application/geo+json` with a GeoJSON FeatureCollection of compact sites, ready for a map layer.

## Pagination

List endpoints use cursor pagination. A page has `data` and `next_cursor`. Pass `next_cursor` back as `cursor` with the same filters to get the next page, and stop when it is null. Cursors are opaque and expire after 24 hours. The `Link` header carries the same next page as an RFC 8288 link with `rel="next"`. `limit` sets the page size, 100 by default and 500 at most.

The change feed pages by sequence number instead of a cursor, because the sequence number is also your sync position: store `next_after_seq` and send it as `after_seq` next time.

## Caching and ETags

Site, governed list and download list responses carry `Cache-Control` and an `ETag`. A site's ETag changes exactly when its `change_seq` changes. Send the ETag back in `If-None-Match` and the API answers 304 with no body when nothing changed. Responses may be served by the CDN, stale for a short while during revalidation (`stale-while-revalidate`), and change events purge them.

## Merged sites

`GET /v1/sites/{site_id}` for a merged site answers 301 with `Location` set to the surviving site and the same query string, plus a small JSON body naming `redirect_to`. Update the ID you store when you follow it. The change feed also announces every merge as a `site_merged` change with `merged_into`.

## Submissions

`POST /v1/submissions` takes a document that validates against `submission.schema.json` and answers 202 with a `submission_id`, a `status_url` and a `Location` header. A submission never changes live data directly: it passes fixed checks, AI review and routing, and only an approving moderation decision turns it into a change. Follow the outcome with `GET /v1/submissions/{submission_id}` or the `submissionDecided` webhook. The status response gives the outcome, the public note for the contributor, reason codes and the resulting change sequence numbers, without exposing moderators or verdicts.

Before submitting for a contributor, a partner app must have their acceptance of the contributor terms and send it in `consent`. Identify the contributor with a stable pseudonymous ID that means nothing outside your app (`contributor.kind` pseudonymous), or with their OTWD contributor ID if they signed in to Open Touring (`contributor.kind` direct). Never send names or email addresses: the schema rejects an `@` in a pseudonymous ID.

Photos are uploaded first. `POST /v1/photo-uploads` returns a short-lived upload URL and an `upload_id`. Upload the file, then send an `add_photo` submission naming the `upload_id`.

### Idempotency keys

`POST /v1/submissions` and `POST /v1/photo-uploads` require an `Idempotency-Key` header, following the IETF Idempotency-Key header draft. Use a new random value, such as a UUID, for each logical submission, and reuse it on every retry of that submission, for example after a timeout or when an app sends a queue of submissions made offline. A repeat with the same key and the same body returns the original response with `Idempotent-Replayed: true` and creates nothing new. The same key with a different body returns 422. A repeat that arrives while the first request is still being processed returns 409. Keys are kept for 24 hours.

### Conflicts and base_change_seq

Every site has a `change_seq`: the sequence number of the latest change applied to it, and every fact records the `change_seq` that last set it. Submissions that edit a site (`update_facts`, `report_closure`, `request_merge`) must send `base_change_seq`, the site's `change_seq` as the contributor saw it.

The check is per fact. When every fact the submission touches is unchanged since `base_change_seq`, it is accepted even if other facts on the site changed in the meantime. When a touched fact did change, the API answers 409 with `current_change_seq` and `conflicting_fields` (JSON Pointers such as `/facts/prices`). Fetch the site again, show the contributor the newer values, and submit again with the new `base_change_seq` if they still want the change. This keeps two contributors from overwriting each other without either of them seeing the other's report.

## Change feed and webhooks

`GET /v1/changes` lists changes in sequence order after `after_seq`. Sequence numbers are global and only increase, but they may have gaps, so never count on seq + 1. Each change gives the site's `previous_seq`: when it differs from the `change_seq` you hold for that site, you missed a change and should fetch the site again. When `after_seq` is older than the retained feed the response is 410, and you should restart from the latest full bulk download, whose `to_seq` tells you where to resume.

Any key can register a webhook endpoint in the developer portal for `submissionDecided`, which is free on every tier because it belongs to the contribute path. `changeApplied` needs a paid tier, like the change feed it mirrors. Deliveries follow the Standard Webhooks scheme: headers `webhook-id`, `webhook-timestamp` and `webhook-signature`, an HMAC-SHA256 signature over the ID, timestamp and raw body, at-least-once delivery with retries for 3 days, and the same `webhook-id` on every retry so you can deduplicate. Verify the signature and reject timestamps more than 5 minutes old. The change feed stays the source of truth for anything a webhook missed.

## Bulk downloads

`GET /v1/downloads` lists the files available to the key: full downloads (GeoParquet in the compact form, GeoJSON and GeoJSON Text Sequences in the full form) and, on paid tiers, delta files covering the changes between `from_seq` and `to_seq`. URLs are signed for the key and expire, and every file has a `sha256` to verify. Load the latest full download, then follow the change feed or apply delta files from its `to_seq`.

## Rate limits

Responses carry the `RateLimit` and `RateLimit-Policy` header fields from the IETF RateLimit header fields draft, for example `RateLimit-Policy: "default";q=1000;w=60` and `RateLimit: "default";r=812;t=34`. When a limit is used up the API answers 429 with `Retry-After` in seconds. Limits depend on the tier and are set per API key.

## Errors

Errors use RFC 9457 problem details with content type `application/problem+json`. `type` is a URI under `https://opentouring.org/problems/` that identifies the problem and documents it, `title` and `status` are always present, and `request_id` identifies the request in OTWD's logs. Validation errors (422) add an `errors` list of JSON Pointers into the request body with a message for each, and conflicts (409) add `current_change_seq` and `conflicting_fields`.

## Attribution and licences

OTWD data is CC BY 4.0. Show "Data: Open Touring contributors, opentouring.org, CC BY 4.0" wherever OTWD data appears, plus every credit in a site's `attribution` list and each photo's own `attribution`. The spec itself and the JSON Schema are Apache-2.0.

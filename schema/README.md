<!-- SPDX-License-Identifier: Apache-2.0 -->

# OTWD JSON Schema, version 1

This directory holds the data contract for OTWD: JSON Schema (draft 2020-12) documents for sites, submissions, moderation decisions, verdicts and changes, the two governed lists, their mappings to OpenStreetMap and schema.org, examples, and a validator. The OpenAPI spec in `../api/` references these files directly, and the Rust API, the Python pipelines, the website and the SDKs are all built against them.

Every schema has an `$id` under `https://schema.opentouring.org/otwd/v1/`. References between files are relative, so the files resolve both from disk and from that base URL.

## Files

| File                                   | What it describes                                                                                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `site.schema.json`                     | A site in the full form: every fact with its provenance. Served with `view=full` and in GeoJSON bulk downloads.                           |
| `site-compact.schema.json`             | A site in the compact form: plain values, no per-fact provenance. The API default and the GeoParquet column layout.                       |
| `submission.schema.json`               | A submission as a partner app or the website sends it (new_site, update_facts, add_photo, report_closure, request_merge, report_problem). |
| `verdict.schema.json`                  | The AI's structured recommendation on a submission. Advice only.                                                                          |
| `moderation-decision.schema.json`      | The recorded outcome for a submission, with who or what decided and why.                                                                  |
| `change.schema.json`                   | An applied change, as it appears in the change feed, webhooks and delta files.                                                            |
| `values.schema.json`                   | The value shape of every fact, shared by sites and submissions.                                                                           |
| `common.schema.json`                   | IDs, codes, localised text and the provenance record.                                                                                     |
| `vocabulary.schema.json`               | The format of the governed lists.                                                                                                         |
| `site-types.json`, `facilities.json`   | The governed lists themselves, with labels in en-AU, descriptions, attributes, safety fact flags and mappings.                            |
| `mappings/`                            | The OSM and schema.org mappings explained, with tables generated from the governed lists.                                                 |
| `examples/valid/`, `examples/invalid/` | Documents that must pass and documents that must fail.                                                                                    |
| `tools/validate.py`                    | Checks all of the above.                                                                                                                  |

## Public IDs

A site's public ID looks like `otwd:site:01KR6JW0QBNHM90XV3GS9Y2G26`: the namespace `otwd`, the kind of thing, and a ULID. Every other OTWD identifier follows the same form (`otwd:submission:...`, `otwd:decision:...`, `otwd:verdict:...`, `otwd:photo:...`, `otwd:contributor:...`, `otwd:partner_app:...`, `otwd:upload:...`). Seed sources are the one exception: they are curated by maintainers, so they use a readable slug such as `otwd:seed_source:au-example-parks-campgrounds`.

The prefix makes an ID self-describing wherever it ends up. Partner apps store OTWD IDs next to IDs from other sources in their own databases, logs and support tickets, and `otwd:site:` says where the ID came from and what it names. The kind segment also stops a submission ID being used where a site ID belongs, because the patterns in `common.schema.json` reject it.

The ULID part is 128 bits, so it fits a Postgres `uuid` column. It can be generated without coordination by any service, including the Rust API, the moderation workers and the Python pipelines. It sorts by creation time, which keeps database indexes compact, and it uses Crockford base32 in upper case, which avoids characters that are easy to misread (I, L, O, U). It reveals when the ID was created, which is harmless because `created_at` is public anyway. Sequential numbers were ruled out because they need a central counter and invite scraping by counting.

Colons are allowed in a URL path segment (RFC 3986), so the API uses the full ID in paths, for example `/v1/sites/otwd:site:01KR6JW0QBNHM90XV3GS9Y2G26`, without percent-encoding. Website addresses use only the ULID part, as in `/sites/nt/pandanus-flats-caravan-park-01KR6JW0QBNHM90XV3GS9Y2G26`, which converts back to the full ID without loss.

A public ID never changes and is never reused. A closure keeps its ID. A merge leaves the losing site as a stub with `status` merged and `redirect_to` naming the survivor, and the API answers it with a 301.

## Facts and provenance

Every fact carries its provenance: who supplied it, through which partner app or seed source, when it was observed, when OTWD recorded it, and with what confidence. In the full form each fact is an object holding the value and its provenance side by side:

```json
"rig_limits": {
  "value": { "max_length_m": 7, "big_rig_suitable": "no" },
  "provenance": {
    "source_kind": "contributor",
    "contributor_id": "otwd:contributor:01KJZDDQFKC9VHYPXC2VGW3JA4",
    "observed_on": "2026-09-06",
    "recorded_at": "2026-09-08T23:10:00Z",
    "confidence": 0.8,
    "submission_id": "otwd:submission:01KSEY055P9K7NVDVYTYQ12B0M",
    "decision_id": "otwd:decision:01KSVP53ET0XV8C1K5Y3HC83EP",
    "change_seq": 20211
  }
}
```

Facts live under `facts` (names, location, site types, description, opening and reception hours, prices, rig limits, access, pets, bookings, contact, capacity, stay limits). Facilities live under `facilities`, one fact per facility code, so each facility has its own provenance. Photos carry provenance too. The values derived from the location (country, subdivision, locality, time zone) sit under `derived` without provenance, because OTWD computes them and nobody submits them.

The grain is one provenance per fact, not per value inside it. A price list or a set of opening hours is reported, checked and replaced as a whole by one contributor or one seed source, so splitting provenance further would add size without telling a reader anything new. Facilities are separate facts because different people report them at different times.

The compact form (`site-compact.schema.json`) is the same site with each fact replaced by its value. It keeps three things from the provenance so readers of the compact form are not left blind: an `attribution` list with every credit the facts require, `min_confidence` (the lowest confidence on the site) and `safety_facts_observed_on` (the oldest observation among its safety facts). It also fills in the facilities that are read from other facts, so filters work the same way on every facility code.

### Trade-off

Keeping value and provenance together in the full form means a fact can never be separated from its source, a seed source update can replace one fact without touching a contributor's newer fact beside it, and a moderator or partner app can weigh each fact on its own. The cost is size and verbosity: a full site is several times larger than the compact one, and reading a value takes one extra step (`facts.prices.value`). Two alternatives were weighed. A parallel provenance map keyed by field path keeps values small but lets the two drift apart, and every consumer has to join them. Provenance only on the site, or only in the change history, is compact but cannot express a site whose facts come from different sources, which is the normal case once seed data and contributions mix.

The compact form removes the verbosity for the common case. Map apps, lists and bulk analysis read compact sites. Apps that show sources, weigh freshness or contribute corrections read the full form for the sites they need.

## Unknown, absent and safety facts

A fact or facility missing from a site is unknown. A facility recorded with `available: false` is known to be absent. The difference matters most for drinking water and rig limits, so apps must never present an unknown as a no, or as unlimited.

Safety facts are the facts a traveller relies on for safety: drinking water and non-potable water, road access, rig limits, the site's fire policy (`fires_allowed`) and its fire district, and the drinking water point and emergency hospital site types. They are marked with `"x-otwd-safety-fact": true` in `site.schema.json` and `safety_fact: true` in the governed lists. Routing always sends a change to a safety fact to a moderator.

Fire bans declared by fire authorities change daily and are never recorded in OTWD. `fires_allowed` is only the site's standing policy, and `fire_district` names the fire authority and district the site falls in, with `ban_info_url` pointing to the authority's official live fire ban information. OTWD computes `fire_district` from the location against a seed source's district boundaries, so contributors never submit it. Apps that show `fires_allowed` should link to `ban_info_url` beside it.

## Governed lists

`site-types.json` and `facilities.json` hold every site type and facility code with an en-AU label, a description, the attributes it carries, whether it is a safety fact, and its OSM and schema.org mappings. Codes are stable: a code is never renamed or reused, and one that is no longer wanted is marked `deprecated` and keeps its meaning.

The schemas accept any code that matches the code pattern, not only the codes in the lists. That way a site that uses a facility added in a later minor version still validates against an older copy of the schema. Membership of the governed lists is checked by the API and by `tools/validate.py`, and consumers ignore codes they do not recognise. Facilities with attributes are checked strictly: each has its own schema in `values.schema.json`, and the validator confirms the attributes in `facilities.json` match it.

Three facility codes are read from other facts rather than stored: `pets_allowed` and `dog_off_leash` from `pets`, and `big_rig_access` from `rig_limits.big_rig_suitable`. Storing them twice would let the two copies disagree, so the full form and submissions reject them in the facilities map, and the compact form and the API filters fill them in. Each has a `stored_as` entry in `facilities.json` with the rule.

The fuel site type records that a fuel station is there and its non-fuel facts. Fuel prices, grades and brands are outside OTWD.

## Versioning

Documents carry `schema_version` (for example `1.0`). Minor versions only add optional fields and governed list entries, so a document valid under 1.0 stays valid under every 1.x, and a consumer written for 1.0 can read any 1.x document by ignoring what it does not know. Removing or changing the meaning of a field or code needs version 2, published under a new `$id` base (`.../otwd/v2/`) and served under `/v2` of the API alongside `/v1`.

## Validating

```sh
python3 -m pip install -r schema/tools/requirements.txt
python3 schema/tools/validate.py
```

With no arguments the script checks every schema against the 2020-12 metaschema, checks the governed lists against `vocabulary.schema.json` and against the per-facility schemas, validates every example with format checking on, and applies the rules the API enforces beyond JSON Schema: governed list codes, ISO 3166-2 subdivisions inside the site's country, IANA time zones, and a few cross-field rules. Every file in `examples/valid` must pass. Every file in `examples/invalid` must fail with the error fragment named for it in `examples/invalid/expected.json`, so an invalid example cannot pass the test by failing for an unrelated reason. The exit status is 0 only when all of that holds.

To check documents of your own, name them. The schema is chosen from the file name suffix (`.site.json`, `.site-compact.json`, `.submission.json`, `.verdict.json`, `.moderation-decision.json`, `.change.json`):

```sh
python3 schema/tools/validate.py my-export/*.site.json
```

## Examples

The valid examples are invented Australian sites with plausible names and coordinates: a free camp in Queensland, a caravan park in the Northern Territory, a national park campsite in New South Wales imported from a seed source, a council dump point in Victoria, a rest area in Western Australia, a showground in South Australia that is temporarily closed, a lookout in Tasmania with a photo, and a merged site. Two of them also appear in the compact form. The rest cover every submission kind, a verdict, four moderation decisions and three changes. Phone numbers use the ranges ACMA reserves for fiction, and web addresses use the `example.com` and `example.org` domains.

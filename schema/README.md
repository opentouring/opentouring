<!-- SPDX-License-Identifier: Apache-2.0 -->

# OTWD JSON Schema, version 1

This directory holds the data contract for OTWD: JSON Schema (draft 2020-12) documents for the four record types (sites, road restrictions, road segments and ferry services), submissions, moderation decisions, verdicts and changes, the governed lists and their translations, their mappings to OpenStreetMap and schema.org, examples, and a validator. The OpenAPI spec in `../api/` references these files directly, and the Rust API, the Python pipelines, the website and the SDKs are all built against them.

Every schema has an `$id` under `https://schema.opentouring.org/otwd/v1/`. References between files are relative, so the files resolve both from disk and from that base URL.

## Files

| File                                                                                                                            | What it describes                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `site.schema.json`                                                                                                              | A site in the full form: every fact with its provenance. Served with `view=full` and in GeoJSON bulk downloads.                               |
| `site-compact.schema.json`                                                                                                      | A site in the compact form: plain values, no per-fact provenance. The API default and the GeoParquet column layout.                           |
| `road-restriction.schema.json`, `road-restriction-compact.schema.json`                                                          | A road restriction (a point where a limit applies to vehicles) in the full and compact forms.                                                 |
| `road-segment.schema.json`, `road-segment-compact.schema.json`                                                                  | A road segment (a stretch of road or track with line geometry) in the full and compact forms.                                                 |
| `ferry-service.schema.json`, `ferry-service-compact.schema.json`                                                                | A ferry service (a crossing between two ferry terminal sites) in the full and compact forms.                                                  |
| `submission.schema.json`                                                                                                        | A submission as a partner app or the website sends it: a new record of any type, or an edit, photo, closure, merge request or problem report. |
| `verdict.schema.json`                                                                                                           | The AI's structured recommendation on a submission. Advice only.                                                                              |
| `moderation-decision.schema.json`                                                                                               | The recorded outcome for a submission, with who or what decided and why.                                                                      |
| `change.schema.json`                                                                                                            | An applied change, as it appears in the change feed, webhooks and delta files.                                                                |
| `values.schema.json`                                                                                                            | The value shape of every fact, shared by all record types and submissions.                                                                    |
| `common.schema.json`                                                                                                            | IDs, codes, localised text, the provenance record and the record-level building blocks every record type shares.                              |
| `record-types.json`, `record-types.schema.json`                                                                                 | The record type registry and its format: every record type with its geometry, schemas, API path and creation kind.                            |
| `seed-sources.json`, `seed-sources.schema.json`                                                                                 | The seed source registry and its format: every seed source with its licence, credit, changes notice and licence review.                       |
| `vocabulary.schema.json`                                                                                                        | The format of the governed lists.                                                                                                             |
| `site-types.json`, `facilities.json`, `structures.json`, `surfaces.json`, `vehicle-access-classes.json`, `vehicle-classes.json` | The governed lists themselves, with labels and descriptions in en-AU, the reference language, and mappings.                                   |
| `translation.schema.json`                                                                                                       | The format of a governed list translation: labels and descriptions in another language, keyed by code.                                        |
| `i18n/`                                                                                                                         | Translations of the governed lists, one folder per language.                                                                                  |
| `mappings/`                                                                                                                     | The OSM and schema.org mappings explained, with tables generated from the governed lists.                                                     |
| `examples/consumer/`                                                                                                            | Documents from a later minor version that a consumer must accept and a producer may not send.                                                 |
| `examples/valid/`, `examples/invalid/`                                                                                          | Documents that must pass and documents that must fail.                                                                                        |
| `tools/validate.py`                                                                                                             | Checks all of the above.                                                                                                                      |

## Public IDs

A site's public ID looks like `otwd:site:01KR6JW0QBNHM90XV3GS9Y2G26`: the namespace `otwd`, the kind of thing, and a ULID. Road restrictions, road segments and ferry services use the same form with their own kind: `otwd:road_restriction:...`, `otwd:road_segment:...` and `otwd:ferry_service:...`. The kind is the record type's name in snake_case, like `partner_app` and `seed_source`, so an ID says what it names without a lookup. Every other OTWD identifier follows the same form (`otwd:submission:...`, `otwd:decision:...`, `otwd:verdict:...`, `otwd:photo:...`, `otwd:contributor:...`, `otwd:partner_app:...`, `otwd:upload:...`). Seed sources are the one exception: they are curated by maintainers, so they use a readable slug such as `otwd:seed_source:au-example-parks-campgrounds`.

The prefix makes an ID self-describing wherever it ends up. Partner apps store OTWD IDs next to IDs from other sources in their own databases, logs and support tickets, and `otwd:site:` says where the ID came from and what it names. The kind segment also stops a submission ID being used where a site ID belongs, because the patterns in `common.schema.json` reject it.

The ULID part is 128 bits, so it fits a Postgres `uuid` column. It can be generated without coordination by any service, including the Rust API, the moderation workers and the Python pipelines. It sorts by creation time, which keeps database indexes compact, and it uses Crockford base32 in upper case, which avoids characters that are easy to misread (I, L, O, U). It reveals when the ID was created, which is harmless because `created_at` is public anyway. Sequential numbers were ruled out because they need a central counter and invite scraping by counting.

Colons are allowed in a URL path segment (RFC 3986), so the API uses the full ID in paths, for example `/v1/sites/otwd:site:01KR6JW0QBNHM90XV3GS9Y2G26`, without percent-encoding. Website addresses use only the ULID part, as in `/sites/nt/pandanus-flats-caravan-park-01KR6JW0QBNHM90XV3GS9Y2G26`, which converts back to the full ID without loss.

A public ID never changes and is never reused. A closure keeps its ID. A merge leaves the losing record as a stub with `status` merged and `redirect_to` naming the survivor, and the API answers it with a 301. A record recorded as the wrong record type becomes a `replaced` stub whose `redirect_to` names its replacement, of another type, also answered with a 301. A record that should never have been published becomes a `retracted` stub with nothing but its ID and status, answered with a 410. An unmerge brings a merged stub back as a record under the same ID, and a split keeps the record's ID for one part and gives the others new IDs ([ADR 0036](../docs/adr/0036-record-lifecycle-and-change-origins.md)). These rules are the same for every record type: merges, unmerges and splits stay within one record type, and a replacement always leaves it.

Each change in `change.schema.json` has a `kind`, what happened to the record, and an `origin`, why: a `submission` names its submission and decision, a `revert` names the change it undoes in `reverts_seq`, a `takedown` names its reason and never its requester, and a `recompute` updates only `/derived` and has no decision. `confirm_facts` submissions become `facts_confirmed` changes, which add to `confirmations` without changing a value.

## Facts and provenance

Every fact carries its provenance: what kind of source supplied it, through which partner app or seed source, when it was observed, when OTWD recorded it, with what confidence, and the change that set it. In the full form each fact is an object holding the value and its provenance side by side:

```json
"rig_limits": {
  "value": { "max_length_m": 7, "big_rig_suitable": "no" },
  "provenance": {
    "source_kind": "partner_app",
    "partner_app_id": "otwd:partner_app:01KJK8W2CAWJC5J54FT58K4JGM",
    "observed_on": "2026-09-06",
    "recorded_at": "2026-09-08T23:10:00Z",
    "confidence": 0.8,
    "change_seq": 20211
  }
}
```

Published provenance never identifies a contributor ([ADR 0038](../docs/adr/0038-contributor-identity-in-published-data.md)). It names the partner app, or the seed source, and the date. A direct contributor appears as `source_kind` contributor, with their `display_name` only if they chose to be named. Contributor IDs, pseudonymous IDs and submission IDs stay in the submission log, where moderation, trust scores and abuse handling use them, and `tools/validate.py` fails any record or change that carries one, in any field. Confirmations publish a count of different contributors, never who they were.

Every record type uses the same fact wrapper, `Fact` in `common.schema.json`, and constrains its `value` with the value shape from `values.schema.json`. The parts every record shares live in `common.schema.json` once: the full form envelope (`FullRecord`: identity, `StatusFact`, timestamps, `change_seq`, photos and the merge rule), the compact form envelope (`CompactRecord`: the same with the closure fields flattened, the primary `name`, `attribution`, `min_confidence` and `safety_facts_observed_on`), and derived values (`PointDerivedValues` and `LineDerivedValues`, wrapped as `PointDerived` and `LineDerived` in the full form). A change to how provenance, status or photos work is made once for all four record types.

Each record type's full form schema defines its fact table once, in three definitions the other schemas reuse:

- `Facts`: every fact wrapped with its provenance, for the full form.
- `FactValues`: every fact as a plain value. The compact form and the submission schema reference it directly.
- `RequiredFacts`: the facts a record of that type always has, used by the full form, the compact form and the submission that creates one.

### What JSON Schema cannot share

JSON Schema has no templates, so two things are written twice and checked by `tools/validate.py` instead. `Facts` and `FactValues` both list every fact name, because one wraps each value in `Fact` and the other does not: the validator checks that they name the same facts with the same value shapes. The `update_facts` rule that the required facts cannot be removed lists them as JSON Pointers (`/facts/location`), which JSON Schema cannot build from names: the validator checks those lists against `RequiredFacts`. Schemas that combine definitions close the object with `unevaluatedProperties: false`, because `additionalProperties` cannot see properties defined in a referenced schema.

For a site, facts live under `facts` (names, location, site types, description, opening and reception hours, prices, rig limits, access, pets, bookings, contact, capacity, stay limits). Facilities live under `facilities`, one fact per facility code, so each facility has its own provenance. Photos, which any record type can have, carry provenance too. The values derived from the location (country, subdivision, locality, time zone) sit under `derived` without provenance, because OTWD computes them and nobody submits them.

The grain is one provenance per fact, not per value inside it. A price list or a set of opening hours is reported, checked and replaced as a whole by one contributor or one seed source, so splitting provenance further would add size without telling a reader anything new. Facilities are separate facts because different people report them at different times.

The compact form (`site-compact.schema.json`) is the same site with each fact replaced by its value. It keeps three things from the provenance so readers of the compact form are not left blind: an `attribution` list of structured entries with every credit the facts require (text, licence, links and the changes notice CC BY asks for, [ADR 0037](../docs/adr/0037-structured-attribution-and-photo-licences.md)), `min_confidence` (the lowest confidence on the site) and `safety_facts_observed_on` (the oldest observation among its safety facts). It also fills in the facilities that are read from other facts, so filters work the same way on every facility code.

### Trade-off

Keeping value and provenance together in the full form means a fact can never be separated from its source, a seed source update can replace one fact without touching a contributor's newer fact beside it, and a moderator or partner app can weigh each fact on its own. The cost is size and verbosity: a full site is several times larger than the compact one, and reading a value takes one extra step (`facts.prices.value`). Two alternatives were weighed. A parallel provenance map keyed by field path keeps values small but lets the two drift apart, and every consumer has to join them. Provenance only on the site, or only in the change history, is compact but cannot express a site whose facts come from different sources, which is the normal case once seed data and contributions mix.

The compact form removes the verbosity for the common case. Map apps, lists and bulk analysis read compact sites. Apps that show sources, weigh freshness or contribute corrections read the full form for the sites they need.

## Record types and geometry

Sites and road restrictions are points: their `location` fact is a latitude and longitude. Road segments and ferry services are lines: their `geometry` fact is a GeoJSON LineString or MultiLineString (RFC 7946) in WGS84, longitude first. GeoJSON responses and bulk downloads turn locations into Point geometry. There are no map tiles.

A **road restriction** has a `structure` (from `structures.json`) with a `passage`: over (the road crosses it, so weight and width matter), under (the road passes beneath it, so vertical clearance matters), through (a tunnel, gate or ford) or along (a limit signed on the open road). Each structure code lists the passages it allows. Its limits are `vertical_clearance`, `width_limit`, `weight_limit` and `length_limit`, and it always has at least one. Vertical clearance and width hold every known figure in `measurements`, each with a basis (signed, surveyed, measured or unknown), optional heading of travel or lane, date and survey certificate, plus `lowest_m`, the lowest figure of any basis, and `lowest_basis`, the basis of that figure. Rig filters and apps compare a vehicle with `lowest_m`, because a measured or surveyed figure below the sign is the one that strikes the vehicle. Every height and width, including each figure, is at most 10 m, so a figure in feet such as 13.5 fails instead of passing as metres.

A **road segment** has a `surface` (from `surfaces.json`, with a condition), a `vehicle_access_class` (from `vehicle-access-classes.json`, ranked from 2WD to closed to vehicles), `towing_permitted`, a `seasonal_closure`, and optional weight and length limits that apply along its whole length. `towing_permitted` comes from contributors, so its provenance is never a seed source and a seeding pipeline submission cannot propose it.

A **ferry service** joins exactly two `terminals`, which are sites whose site types include `ferry_terminal`, a fixed check. A service that calls at more places is recorded as one ferry service per crossing. It lists its `accepted_vehicle_classes` (from `vehicle-classes.json`), its `vehicle_limits` (overall and per vehicle class, plus the total load per crossing), `fares` per vehicle class and vehicle band, `bookings`, `operating_hours`, `crossing` details and any `seasonal_closure`. Vehicle bands and length limits are combined lengths, including the drawbar and anything towed, as operators price them. A fare's `crossings` is 1 for a one-way fare and 2 for a return. Fares and vehicle limits may only name vehicle classes the service carries.

A **seasonal closure** is a recurring window (month and day, with `dates_year` saying which year's published dates they came from) plus the authority and a link to its current information. A one-off closure of any record, such as a bridge shut by flood damage, is the record's status `temporarily_closed`, with `closed_on`, `reopens_on`, `closure_authority` and `closure_info_url`, named the same in the full form, the compact form and a `report_closure` submission. Short incident closures stay with the authority.

## Time

Every instant, such as `recorded_at`, `retrieved_at`, `decided_at`, `created_at` or `applied_at`, is a `Timestamp`: RFC 3339 in UTC with the `Z` suffix. Any other offset fails. Local schedules (opening and reception hours, check-in times, generator hours, ferry operating hours, seasonal closures and the periods of access and fire policy) are local clock times (`LocalTime`), local dates (`LocalDate`) and days of the year (`MonthDay`), read in the record's IANA time zone and never converted to UTC, so a 6:00 am departure stays at 6:00 am through daylight saving changes ([ADR 0032](../docs/adr/0032-utc-for-instants-local-time-for-schedules.md)).

A point record has one derived `time_zone`. A line record has `time_zone`, its default (the zone at its start), and `time_zones`, every zone it passes through in order. A schedule on a line that belongs to another of those zones names it in its own `time_zone`, which `OpeningHours`, `SeasonalClosure` and a ferry service's `Fares` accept, and `tools/validate.py` rejects a schedule zone that is not one of the record's zones. A line that returns to a zone lists it again, so a track from South Australia into Victoria and back has `time_zones` Adelaide, Melbourne, Adelaide, but no zone appears twice in a row.

## Unknown, absent and safety facts

A fact or facility missing from a site is unknown. A facility recorded with `available: false` is known to be absent. The difference matters most for drinking water and rig limits, so apps must never present an unknown as a no, or as unlimited.

Safety facts are the facts a traveller relies on for safety: drinking water and non-potable water, road access, rig limits, the site's fire policy (`fires_allowed`) and its fire district, the drinking water point and emergency hospital site types, a road restriction's location and every limit on it, a road segment's geometry, vehicle access class, towing permitted, seasonal closure and limits, and a ferry service's geometry, terminals, accepted vehicle classes, vehicle limits and seasonal closure. A site's location is not a safety fact. An absent limit on a road restriction, road segment or ferry service is unknown, never unlimited. They are marked with `"x-otwd-safety-fact": true` in the full form schemas and `safety_fact: true` in the site type and facility lists.

Routing always sends a change to a safety fact to a moderator, and the always-human list is derived, never declared. A moderation decision's `routing` records the submission's kind, record type and the fields it touched. The fixed checks, and `tools/validate.py` for the examples, put a submission on the list when its kind creates a record, closes one or merges records, or when any field it touches carries the safety fact marker for its record type. A decision by a routing rule on such a submission fails, whatever `always_human` says, and a change that touches a marked field must not say `safety_fact_changed: false`.

Fire bans declared by fire authorities change daily and are never recorded in OTWD. `fires_allowed` is only the site's standing policy, and `fire_district` names the fire authority and district the site falls in, with `ban_info_url` pointing to the authority's official live fire ban information. OTWD computes `fire_district` from the location against a seed source's district boundaries, so contributors never submit it. Apps that show `fires_allowed` should link to `ban_info_url` beside it.

## Governed lists

`site-types.json` and `facilities.json` hold every site type and facility code with a label and a description in en-AU, the attributes it carries, whether it is a safety fact, and its OSM and schema.org mappings. `structures.json` (with the passages each allows), `surfaces.json`, `vehicle-access-classes.json` (with a rank) and `vehicle-classes.json` follow the same format, described in `vocabulary.schema.json`. Codes are stable: a code is never renamed or reused, and one that is no longer wanted is marked `deprecated` and keeps its meaning.

The schemas accept any code that matches the code pattern, not only the codes in the lists. That way a site that uses a facility added in a later minor version still validates against an older copy of the schema. Membership of the governed lists is checked by the API and by `tools/validate.py`, and consumers ignore codes they do not recognise. Facilities with attributes are checked strictly: each has its own schema in `values.schema.json`, and the validator confirms the attributes in `facilities.json` match it.

### Translations

en-AU is the reference language. Every other language is a translation in `i18n/<language>/`, one file per governed list (for example `i18n/de/facilities.json`), following `translation.schema.json`. A translation holds only labels, descriptions and attribute descriptions, keyed by code. Codes, safety facts, attributes and mappings stay in the reference list, so a translation cannot change what a code means, and `tools/validate.py` rejects a translation that names a code or attribute the reference list does not have, carries any other field, or sits in a folder that does not match its `language`. The API serves the governed lists in the language asked for in `Accept-Language`, and missing text falls back to en-AU as [ADR 0031](../docs/adr/0031-governed-lists-and-the-api-are-translatable.md) sets out. `i18n/README.md` explains how to add a translation.

Free text in records, such as names, descriptions and notes, is never translated by OTWD. It is `LocalisedText` or `Notes`, which keep the language the contributor wrote in beside the text.

Three facility codes are read from other facts rather than stored: `pets_allowed` and `dog_off_leash` from `pets`, and `big_rig_access` from `rig_limits.big_rig_suitable`. Storing them twice would let the two copies disagree, so the full form and submissions reject them in the facilities map, and the compact form and the API filters fill them in. Each has a `stored_as` entry in `facilities.json` with the rule.

The fuel site type records that a fuel station is there and its non-fuel facts. Fuel prices, grades and brands are outside OTWD.

## Versioning

Until version 1.0.0 is released, the schema and the API are a draft. Release means a `v1.0.0` tag on this repository, made before any partner app outside the project integrates ([ADR 0030](../docs/adr/0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)). Before that tag, any field, code or endpoint can change or be removed without a new major version, and documents carry `schema_version` `1.0`. From the tag on, the rules below apply.

Documents carry `schema_version` (for example `1.0`). Minor versions only add optional fields, governed list entries, values of open enumerations and record types in the registry, so a document valid under 1.0 stays valid under every 1.x, and a consumer written for 1.0 can read any 1.x document by ignoring what it does not know.

### Open enumerations and record types

Every list of values in the schema is a governed list, an open enumeration or a closed enumeration ([ADR 0035](../docs/adr/0035-open-enumerations-and-a-record-type-registry.md)). An open enumeration, such as change kinds, submission kinds, moderation outcomes or price units, is a string matching `EnumCode`, with the values known at this version in `x-otwd-known-values` and, in its description, what a consumer does with a value it does not know. OTWD sends only known values, and `tools/validate.py` holds every example to them. A consumer's validator ignores the `x-otwd-` keywords, so it accepts values added in later minor versions. A closed enumeration, such as record status or towing permitted, is a plain `enum` that changes only in a new major version.

Record types are listed in `record-types.json` and served at `/v1/record-types`. `RecordId` and `RecordType` accept any snake_case record type code, apart from the kinds reserved for other OTWD identifiers, and `x-otwd-registry` holds producers to the registered ones. A consumer skips records, changes and bulk downloads of a record type it does not know. Removing or changing the meaning of a field or code needs version 2, published under a new `$id` base (`.../otwd/v2/`) and served under `/v2` of the API alongside `/v1`.

## Validating

```sh
python3 -m pip install -r schema/tools/requirements.txt
python3 schema/tools/validate.py
```

`tools/check-schema.sh` does the same in `.tools/venv` and also checks the script's formatting with `ruff format --check`. With no arguments the script checks every schema against the 2020-12 metaschema, checks the governed lists against `vocabulary.schema.json` and against the per-facility schemas, checks that each record type's `Facts`, `FactValues`, compact form and submissions name the same facts with the same value shapes and use one `RequiredFacts`, validates every example with format checking on, and applies the rules the API enforces beyond JSON Schema: governed list codes, ISO 3166-2 subdivisions inside the record's countries, IANA time zones, a structure's allowed passages, the `lowest_m` rule, fares and limits only for carried vehicle classes, the always-human list derived from the safety fact markers, ferry terminals that are `ferry_terminal` sites (in the examples, every terminal must be a site among the valid examples), and a few other cross-field rules. One table of fact checks serves every record type and submissions, and the record types come from `record-types.json`, from which the schema file names and document suffixes follow. Open enumerations and record types are checked as for a producer, and every file in `examples/consumer` must pass the plain validator a consumer uses while failing the strict one on a value this version does not know. It also checks every translation in `i18n/` against `translation.schema.json`, its reference list and its folder. Every file in `examples/valid` must pass, including the translations under `examples/valid/i18n`. Every file in `examples/invalid` must fail with the error fragment named for it (by its path below `examples/invalid`) in `examples/invalid/expected.json`, so an invalid example cannot pass the test by failing for an unrelated reason. The exit status is 0 only when all of that holds.

To check documents of your own, name them. The schema is chosen from the file name suffix (`.site.json`, `.site-compact.json`, `.road-restriction.json`, `.road-restriction-compact.json`, `.road-segment.json`, `.road-segment-compact.json`, `.ferry-service.json`, `.ferry-service-compact.json`, `.submission.json`, `.verdict.json`, `.moderation-decision.json`, `.change.json`):

```sh
python3 schema/tools/validate.py my-export/*.site.json
```

A file at `i18n/<language>/<list file>`, anywhere, is checked as a translation, including the check that its folder matches its `language`.

## Examples

The valid examples are invented Australian sites with plausible names and coordinates: a free camp in Queensland, a caravan park in the Northern Territory, a national park campsite in New South Wales imported from a seed source, a council dump point in Victoria, a rest area in Western Australia, a showground in South Australia that is temporarily closed, a lookout in Tasmania with a photo, and a merged site. Two of them also appear in the compact form. Victorian examples cover the other record types: a low rail bridge with signed and measured clearances per direction and lane, a timber bridge with a weight limit, a 4WD-only track with a seasonal closure, a sealed road divided at a town entry, a merged duplicate track, ferry terminal sites, and a vehicle ferry that carries cars towing caravans with length bands and fares, with compact forms of three of them. A 4WD track that loops from South Australia into Victoria and back shows a line with several time zones and a closure read on the Victorian clock. The rest cover every submission kind (including a photo of a road restriction), a verdict, four moderation decisions and five changes. Phone numbers use the ranges ACMA reserves for fiction, and web addresses use the `example.com` and `example.org` domains.

## Seed sources for road and ferry service records

These open datasets can seed road restrictions, road segments and ferry services. Each is imported as submissions with seed source provenance, like any other seed source. Those with a usable licence are listed in `seed-sources.json`, the seed source registry, as planned until a maintainer confirms the licence and the credit wording from the publisher's own record. The research behind this list, with field counts and URLs, is in `docs/research/road-and-ferry-data.md`.

| Seed source                                            | Licence      | Seeds                                                                                                                                                                                                                                                  |
| ------------------------------------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Vicmap Transport, Road Infrastructure Point (Victoria) | CC BY 4.0    | Road restrictions at bridges, tunnels, fords and gates: `structure`, and `vertical_clearance` and `weight_limit` from height_limit and load_limit with basis unknown.                                                                                  |
| Vicmap Transport, Road Line (Victoria)                 | CC BY 4.0    | Road segment `geometry`, `surface` from road_seal, `vehicle_access_class` from vehicular_access, `seasonal_closure` periods from seasonal_close_date and seasonal_open_date (month and day only), and ferry service `geometry` from ferry_route lines. |
| Road Bridges (Victoria)                                | CC BY 4.0    | Bridge structures and `width_limit` from traffic width (basis unknown). No clearance.                                                                                                                                                                  |
| Recreation Tracks (Victoria)                           | CC BY 4.0    | 4WD touring road segments, with the grade recorded in notes until it is mapped to a vehicle access class.                                                                                                                                              |
| NSW State Roads Vertical Clearances                    | CC BY 3.0 AU | Road restrictions under bridges over state roads, `vertical_clearance` with basis unknown. Its coordinates are the bridge's start point, so `accuracy_m` is set wide.                                                                                  |
| Main Roads WA Drive Under Structures                   | CC BY 3.0 AU | Road restrictions with `vertical_clearance` basis surveyed and a `certificate_url`.                                                                                                                                                                    |
| Tasmanian Low Bridge Clearances                        | CC BY 4.0    | `vertical_clearance` per lane.                                                                                                                                                                                                                         |

The Vicmap code tables (road_seal, vehicular_access, restrictions) must be read before mapping their numeric codes, and road_seal maps to `unsealed` until a contributor reports the material. The VicRoads Structure Height Clearance dataset, the best Victorian clearance source, has been delisted and its licence is unconfirmed, so it is not a seed source until the Department of Transport and Planning confirms the licence. Towing permitted and Victorian ferry vehicle limits come from contributors.

---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Own versioned JSON Schema with OSM and schema.org mappings

OTWD defines its own versioned JSON Schema and publishes mappings from it to OpenStreetMap tags (for example `tourism=camp_site`, `amenity=sanitary_dump_station`) and to schema.org types (for example `Campground`). Site types and facilities come from a governed list that the community can propose additions to. The schema is global from the start: ISO 3166-1 and 3166-2 codes, metric units, IANA time zones and no Australia-only values.

## Considered options

- **Use OSM tags directly.** Rejected: free-form tags cannot be validated or governed, and touring needs facts (rig limits, per-night prices, dump point access) that OSM tagging handles unevenly.
- **Use schema.org directly.** Rejected: it is too coarse for facility-level facts and is not versioned in a way a data contract can rely on.

## Consequences

The schema is the contract for the API, the SDKs and bulk downloads, so changes follow versioning rules and partner apps can rely on them. Adding a site type or facility is a governed proposal, described in CONTRIBUTING.md.

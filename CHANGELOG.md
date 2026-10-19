<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Changelog

This file records changes to the OTWD contract: the JSON Schema in `schema/` and the API in `api/`. The contract is a draft until `v1.0.0` is tagged ([ADR 0030](docs/adr/0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)), and entries start with that release. From then on, every pull request that changes the contract adds a line under "Unreleased", and a release moves those lines under its version and date.

Each entry says what changed, whether it is an addition or a breaking change, and what partner apps need to do. A breaking change also gives the date `/v1` stops, as [docs/extending.md](docs/extending.md#breaking-change-after-v100) sets out.

## Unreleased

- **Breaking change (draft):** the older codes that used "site" for a camping spot now say "pitch", matching the glossary term in CONTEXT.md. The contract is still a draft ([ADR 0030](docs/adr/0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)), so this ships without a version bump. Partner apps that read or write these codes need to switch to the new ones. Counts and units are unchanged.
  - Facilities: `tent_sites` is now `tent_pitches`, `ensuite_sites` is now `ensuite_pitches` and `drive_through_sites` is now `drive_through_pitches`. Their labels and the schema.org `amenityFeature` names follow ("Tent pitches", "Ensuite pitches", "Drive-through pitches", and "Powered pitches" for `power`). The OSM tags are unchanged.
  - Prices: `applies_to` values `site_unpowered`, `site_powered`, `site_ensuite` and `tent_site` are now `pitch_unpowered`, `pitch_powered`, `pitch_ensuite` and `tent_pitch`.
  - Capacity: `sites` is now `pitches` and `powered_sites` is now `powered_pitches`.

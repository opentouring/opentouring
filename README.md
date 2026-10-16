<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Open Touring

Open Touring is an open, crowd-contributed database of the places travellers stop at on the road: campsites, caravan parks, free camps, rest areas, dump points, drinking water, toilets, showers, laundries, information centres, ferry terminals, attractions and more. It also records what stands between a traveller and those places: low bridges and other road restrictions, roads and tracks by surface and vehicle access, and vehicle ferries. The data is free to use under CC BY 4.0. Partner apps read it through an API and send their contributors' new sites and corrections back through moderation, so every app that uses the data can help keep it current.

OTWD, the Open Touring and Waypoint Database, is the technical name for the dataset, the API and the SDKs. Australia comes first, and the schema works for any country.

## Status

Preview: concept build, not yet accepting outside contributions.

The Preview runs the production stack at minimum size with seeded government data and the maintainer's own submissions. Outside contributions open once a not-for-profit host has agreed to take on the project. See [GOVERNANCE.md](GOVERNANCE.md).

## What OTWD offers

Each site is a point (latitude and longitude) with its site types, facilities, prices, opening hours, rig limits, photos and a short description. Road restrictions are points too, with their structure and their vertical clearance, width, weight and length limits. Road segments are lines with their surface, vehicle access class (2WD to 4WD only), whether towing is permitted and seasonal closures. Ferry services are lines between two ferry terminals with the vehicle classes they carry, vehicle limits, fares and hours. Every fact records where it came from and when. Public IDs never change.

Partner apps can query records through the API, by area or along a route, download the whole dataset as GeoParquet or GeoJSON, and submit new records and corrections on behalf of their contributors, the people using the app who choose to send them. Every use needs an API key. The free tier covers reading and bulk downloads, and contributing is always free. Paid tiers add volume, a service level, change feeds and their webhooks, delta files and support. OTWD provides no map tiles: apps draw its points and lines on their own maps.

## Licences

| What                                                     | Licence       |
| -------------------------------------------------------- | ------------- |
| Data (records, facts, photos, descriptions)              | CC BY 4.0     |
| Server code: `services/`, `pipelines/`, `web/`, `infra/` | AGPL-3.0-only |
| `schema/`, `api/`, `sdks/` and sample clients            | Apache-2.0    |

Details are in [LICENSING.md](LICENSING.md), and full licence texts are in [LICENSES/](LICENSES/).

## Documentation

- [CONTEXT.md](CONTEXT.md): the glossary of terms used everywhere in the project
- [docs/architecture.md](docs/architecture.md): how the platform works
- [docs/adr/](docs/adr/): architecture decision records
- [docs/roadmap.md](docs/roadmap.md): build order and open questions
- [docs/contributor-terms-draft.md](docs/contributor-terms-draft.md): draft data contributor terms (not in force)
- [docs/extending.md](docs/extending.md): how to add a governed list code, fact, record type, seed source, country or endpoint
- [docs/policies/](docs/policies/): the moderation policy, the privacy policy draft and the takedown process
- [docs/supported-countries.md](docs/supported-countries.md) and [docs/seed-sources.md](docs/seed-sources.md): where OTWD operates and the open datasets it imports
- [docs/operations/disaster-recovery.md](docs/operations/disaster-recovery.md): backups and restores
- [CONTRIBUTING.md](CONTRIBUTING.md): how to contribute code and propose site types and facilities
- [CHANGELOG.md](CHANGELOG.md): changes to the schema and API from `v1.0.0` on
- [GOVERNANCE.md](GOVERNANCE.md): who runs the project and how that will change
- [SECURITY.md](SECURITY.md): how to report a vulnerability
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): expected behaviour in project spaces

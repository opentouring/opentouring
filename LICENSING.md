<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Licensing

Open Touring uses three licences: one for the data, one for the server code and one for the pieces partner apps build on. Full texts are in [LICENSES/](LICENSES/).

## By directory

| Path                                             | Licence                                        | SPDX identifier |
| ------------------------------------------------ | ---------------------------------------------- | --------------- |
| `services/`                                      | GNU Affero General Public License v3.0 only    | `AGPL-3.0-only` |
| `pipelines/`                                     | GNU Affero General Public License v3.0 only    | `AGPL-3.0-only` |
| `web/`                                           | GNU Affero General Public License v3.0 only    | `AGPL-3.0-only` |
| `infra/`                                         | GNU Affero General Public License v3.0 only    | `AGPL-3.0-only` |
| `schema/`                                        | Apache License 2.0                             | `Apache-2.0`    |
| `api/`                                           | Apache License 2.0                             | `Apache-2.0`    |
| `sdks/`                                          | Apache License 2.0                             | `Apache-2.0`    |
| `tools/`, `.claude/` and root tool configuration | Apache License 2.0                             | `Apache-2.0`    |
| Documentation (`*.md` at the root, `docs/`)      | Creative Commons Attribution 4.0 International | `CC-BY-4.0`     |
| OTWD data (bulk downloads and API responses)     | Creative Commons Attribution 4.0 International | `CC-BY-4.0`     |

Sample clients live under `sdks/` and are Apache-2.0. A directory not listed here takes the licence of its nearest listed parent.

## Source files

Every source file starts with an SPDX header naming its licence, for example:

```
// SPDX-License-Identifier: AGPL-3.0-only
```

or, in the schema, API and SDK directories:

```
# SPDX-License-Identifier: Apache-2.0
```

Copyright stays with each contributor. Code contributions are licensed under the licence of the directory they land in and are signed off under the Developer Certificate of Origin (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Data

OTWD data is published under CC BY 4.0. Attribute it as "Open Touring contributors, OTWD, CC BY 4.0" with a link to https://opentouring.org. Some facts come from seed sources that require their own attribution, and that attribution is carried in each fact's provenance and in the attribution file shipped with every bulk download.

Photos are licensed under CC BY 4.0 by the person who took them. Data contributors keep ownership of what they submit and grant the operator and its successors the rights described in the contributor terms, which are a draft and not yet in force ([docs/contributor-terms-draft.md](docs/contributor-terms-draft.md)).

OpenStreetMap data is never imported into OTWD. The website's map uses an OpenStreetMap-based basemap for display, with OpenStreetMap attribution.

## Licence texts

- [LICENSES/AGPL-3.0-only.txt](LICENSES/AGPL-3.0-only.txt), from https://www.gnu.org/licenses/agpl-3.0.txt
- [LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt), from https://www.apache.org/licenses/LICENSE-2.0.txt
- [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt), from https://creativecommons.org/licenses/by/4.0/legalcode.txt

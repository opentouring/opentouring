---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Data repository layout, otwd.json and the licence of CI files

Accepted 2026-10-22. Builds on [ADR 0046](0046-live-data-in-a-public-git-repository-per-country.md), which sets `<state>/<record-type>/<ulid>.json` and names `otwd.json`, and on [ADR 0047](0047-moderation-on-github-through-pull-requests.md), which gives each state directory its own moderators team. This decision fixes the folder names, the contents of `otwd.json` and the licence of the CI files, so that the loader, CI and anyone cloning a data repository read the same layout.

## Decision

**State folders.** A state folder is the lower-case code of a state or territory: `act`, `nsw`, `nt`, `qld`, `sa`, `tas`, `vic` or `wa`. Records that cross a border live under `interstate`, as ADR 0046 sets. No other top-level folder holds records.

**Record type folders.** A record type folder is plural and in kebab case: `sites`, `road-restrictions`, `road-segments` and `ferry-services`. A record is at `vic/sites/<ulid>.json`, as in ADR 0046. The folder name is the last segment of the `collection` field in the record type registry. A new record type gets its folder through the record type checklist in `docs/extending.md`, with no separate ADR.

**`otwd.json`.** The file at the repository root holds two values:

- `country`: the ISO 3166-1 alpha-2 code of the country the repository covers, `AU` for `opentouring/otwd-au`.
- `schema`: the tag of `opentouring/opentouring` the data conforms to, first `v1.0.0-draft.1`.

Its schema is `schema/otwd-config.schema.json`, which lands with the validator's data repository mode in a separate pull request. CI validates every pull request against the tag in `schema`, as ADR 0046 sets.

**Who checks the state folder.** CI checks only that a state folder is one of the known codes or `interstate`. The loader checks that a record's state folder matches the record's location. CI needs no boundary data, and a record in the wrong state folder is a loader error that a moderator corrects by moving the file ([ADR 0046](0046-live-data-in-a-public-git-repository-per-country.md)). The loader also reports a record under `interstate/` that does not cross a state or territory border.

**Licence of CI files.** The workflow and any scripts in a data repository, and in `otwd-template`, are Apache-2.0 and start with an SPDX header, matching `schema/`. Records stay CC-BY-4.0. Each data repository's README carries a REUSE-style note that says so. `LICENSING.md` lists the rule.

## Why

Paths and `otwd.json` are a public contract. The loader parses them, CI validates against them and anyone who clones a repository relies on them. Once a country has records, renaming a folder moves every file and breaks every clone and fork, so the names are fixed before the first record.

Putting the state check in the loader keeps CI small. Checking a record against a state's boundary needs boundary data, and CI would have to fetch and version it. The loader runs on opentouring.org, where that data can be kept without being copied into every data repository.

CI files are code, not data, and they sit in repositories whose records are CC-BY-4.0. Apache-2.0 matches the licence of `schema/`, which CI runs, and lets a partner or another country's maintainers copy the workflow without taking on the AGPL.

## Considered options

- **Upper-case or full state names as folders.** Not chosen: lower-case codes are short, sort the same on every file system and match the codes the moderators teams use in CODEOWNERS.
- **Singular record type folders.** Not chosen: the folders hold many records, and plural names match the API paths in the record type registry.
- **CI checks the state folder against boundaries.** Not chosen: it would need boundary data in CI for a check the loader makes anyway.
- **Licence the CI files CC-BY-4.0 with the records.** Not chosen: CC BY 4.0 is not designed for software, and Apache-2.0 gives an express patent grant for scripts.
- **AGPL-3.0-only, as the platform's code.** Not chosen: it would bind every fork of a data repository to copyleft for its workflow alone.

## Consequences

`schema/otwd-config.schema.json` lands with the validator's data repository mode. `otwd-template` and `opentouring/otwd-au` start with this layout, an `otwd.json` pinned to `v1.0.0-draft.1`, Apache-2.0 headers on their workflow and scripts, and the README note. The loader reports a record whose state folder does not match its location. `LICENSING.md` gains a sentence on CI files in data repositories. Changing a folder name or an `otwd.json` key needs a new ADR that supersedes this one.

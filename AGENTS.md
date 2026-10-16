<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Open Touring agent instructions

Open Touring is an open, crowd-contributed database of places travellers stop at on the road. OTWD (Open Touring and Waypoint Database) is the dataset, API and SDKs. This monorepo holds the platform: Rust API on Spin and moderation workers (`services/`), Python data pipelines (`pipelines/`), the Astro website (`web/`), infrastructure as code (`infra/`), the JSON Schema (`schema/`), the OpenAPI spec (`api/`) and generated SDKs (`sdks/`). It is in Preview: outside data contributions are off.

## Vocabulary

`CONTEXT.md` is the glossary. Use its exact terms in code, schema, API fields, docs and issues (site rather than POI or place, contributor rather than user, submission rather than edit). When a concept has no term there, flag the gap instead of coining one.

## Decisions

Before changing architecture, licensing, moderation or data handling, read the ADRs in `docs/adr/` that touch it. Work that contradicts an ADR needs a new ADR that supersedes it. `docs/architecture.md` describes how the components connect.

## Writing rules

Every file in the repo, including code comments, commit messages and UI strings:

- Punctuate with " - ", a comma, a colon or a full stop, never an em or en dash. Join independent clauses with a full stop, never a semicolon.
- Australian spelling: licence (noun), organisation, colour, optimised.
- Plain words. Banned: delve, dive in, deep dive, unpack, navigate, foster, leverage, harness, unlock, elevate, streamline, robust, seamless, cutting-edge, game-changer, holistic, tapestry, landscape, ecosystem, boasts, arguably.
- Prose when two or three sentences do the job. Sentence case headings. Bold only for headings and labels.
- Docs say what the thing does and how to use it. Comparisons and build history go in the commit message.

Check before finishing: `grep -rnE $'\u2014|\u2013' --exclude-dir=.git .` returns nothing.

## Licensing

`services/`, `pipelines/`, `web/`, `infra/` are AGPL-3.0-only. `schema/`, `api/`, `sdks/` are Apache-2.0. Data and docs are CC-BY-4.0. Start every new source file with the SPDX header for its directory. Moving code from an AGPL directory into an Apache one needs every author's agreement. Details: `LICENSING.md`.

## Commits

Sign off every commit with `git commit -s` (DCO). No CLA. The git hooks (run `npm install` once) check writing rules, schema, OpenAPI, formatting and sign-off, so fix what they report rather than skipping them. A Claude Code hook (`.claude/hooks/block-dangerous-git.sh`) blocks force pushes, pushes to `main`, `reset --hard`, `clean -f`, `branch -D`, whole-tree `checkout .` or `restore .`, `--no-verify` and stash drops. Work on a branch and open a pull request.

## Schema and vocabulary changes

Site types, facilities, structures, surfaces, vehicle access classes and vehicle classes are governed lists. A new or changed value starts as a "Governed list:" issue in the format in `CONTRIBUTING.md`, with OSM and schema.org mappings, and lands in `schema/` and `CONTEXT.md` together.

## Agent skills

### Issue tracker

GitHub Issues on opentouring/opentouring, drafted under `.scratch/` until the GitHub organisation exists. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels, unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the root. See `docs/agents/domain.md`.

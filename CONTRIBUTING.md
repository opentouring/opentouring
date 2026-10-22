<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Contributing

Open Touring is in Preview. Code, documentation and proposals for the governed list are welcome now. Data contributions from outside the project (new sites, corrections, photos) open after a not-for-profit host has signed an agreement to take on the project, because the contributor terms need that host as a stable party to grant rights to. Until then, the Preview holds seeded government data and the maintainer's own submissions.

Read [CONTEXT.md](CONTEXT.md) before writing code, schema or documentation, and use its terms. Read the [ADRs](docs/adr/) that touch the area you are changing. A change that contradicts an ADR needs a new ADR that supersedes it. [docs/extending.md](docs/extending.md) has a checklist for each kind of change: the files to touch, the review, who approves it and whether it needs an ADR.

## Code and documentation

1. Open an issue describing the change, unless it is a small fix. The issue forms cover bugs, governed list proposals, new facts and record types, seed sources, translations and moderation policy changes.
2. Fork the repository and make the change on a branch.
3. Sign off every commit (see below).
4. Open a pull request that links the issue, and work through the checklist in the pull request template.

Every source file carries an SPDX licence header matching its directory (see [LICENSING.md](LICENSING.md)). Documentation follows the project's writing style: plain Australian English, sentence case headings, no dashes used as punctuation, and text that says what the thing does and how to use it.

## Checks before every commit

Run `npm install` once after cloning. It installs the git hooks (lefthook), which check every commit for the writing rules in `AGENTS.md`, a valid schema and OpenAPI spec, Prettier formatting and a DCO sign-off. The schema check (`tools/check-schema.sh`) builds a Python virtual environment in `.tools/venv` from `schema/tools/requirements.txt`, checks the formatting of `schema/tools` with `ruff format --check` (settings in `schema/tools/ruff.toml`) and runs the validator. Run `npm run format` to fix Prettier formatting, `.tools/venv/bin/ruff format schema/tools` to fix Python formatting, and `npm run check:writing`, `npm run check:schema` or `npm run check:api` to run a check on its own. Never skip the hooks with `--no-verify`.

## Sign-off (DCO)

Open Touring uses the [Developer Certificate of Origin](https://developercertificate.org/) instead of a contributor licence agreement. By adding a sign-off line to a commit, you certify that you wrote the change or otherwise have the right to submit it under the licence of the directory it lands in.

Add the line with `git commit -s`:

```
Signed-off-by: Your Name <you@example.com>
```

Use your real name or a name you are known by in the community. Pull requests with unsigned commits cannot be merged. To sign off commits already made on your branch, run `git rebase --signoff main` and force-push the branch.

## Proposing a governed list value

Site types, facilities, structures, surfaces, vehicle access classes, vehicle classes, key schemes, pet species, self-contained schemes and location sensitivity reasons come from governed lists, so that every partner app can rely on the same values. To propose an addition or a change:

1. Check the current list in `schema/` and the existing issues, in case it is already covered or proposed.
2. Open an issue with the "Governed list proposal" form, titled "Governed list: add `<proposed_value>`" (or "change" or "retire"). It gets the `governed-list` label.
3. In the issue, give:
   - the proposed value in `snake_case`, and which governed list it belongs to
   - a one-sentence definition
   - any attributes it needs (for example `max_length_m` or `fee_aud`), with units
   - the matching OpenStreetMap tags and schema.org type or property, or "none"
   - at least two real examples, from at least two countries if possible
   - how it differs from the nearest existing value
4. Discussion runs on the issue. The maintainer (later the steering group) accepts, declines or asks for changes, and an accepted value is added in a schema release.

Values stay global: no country-specific values, metric units only, ISO 3166 codes for regions and IANA names for time zones.

## Translating the governed lists

The governed lists are written in en-AU, the reference language, and can be translated into any language. A translation is a file at `schema/i18n/<language>/<list file>` holding labels and descriptions keyed by code. It never changes codes, safety facts or mappings. Translations are contributed as pull requests and reviewed like any governed list change, by a speaker of the language. Issues and pull requests for the governed lists, translations included, carry the `governed-list` label. [schema/i18n/README.md](schema/i18n/README.md) explains the format and the steps. Write the text yourself or check every line of a draft: unreviewed machine translation is not accepted.

## Data contributions

Outside data contributions are not open yet. When they open, every contributor will accept the data contributor terms first, and partner apps will need each contributor's consent to those terms before submitting on their behalf. The plain-English draft of those terms is in [docs/contributor-terms-draft.md](docs/contributor-terms-draft.md) and is not in force.

Every change to live data arrives in the data repository for its country, such as `opentouring/otwd-au`, as a pull request, and a moderator's review on it is the moderation decision. A submission through a partner app or opentouring.org is screened first and then opened as a pull request by the Open Touring GitHub App, which names no contributor. You can also open a pull request on a data repository from your own GitHub account, once it is linked to an opentouring.org account that has accepted the contributor terms. Your GitHub handle is then public on that pull request. See [ADR 0047](docs/adr/0047-moderation-on-github-through-pull-requests.md).

If you represent a council, tourism body or park agency and can release data under CC BY 4.0 or a compatible licence, open an issue with the "Seed source proposal" form or email hello@opentouring.org. Seed sources are imported through the same moderation pipeline as other submissions and credited in every fact they supply. The sources in use and planned are listed in [docs/seed-sources.md](docs/seed-sources.md).

How submissions are moderated is published in [the moderation policy](docs/policies/moderation.md). How personal information is handled is set out in [the privacy policy draft](docs/policies/privacy-draft.md), which is not in force.

## Conduct and security

Everyone in project spaces follows the [code of conduct](CODE_OF_CONDUCT.md). Report security problems privately as described in [SECURITY.md](SECURITY.md), not in a public issue. To have a photo or text removed because it shows a person, a number plate or private property, or infringes copyright, follow [the takedown process](docs/policies/takedown.md).

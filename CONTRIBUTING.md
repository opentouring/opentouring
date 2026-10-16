<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Contributing

Open Touring is in Preview. Code, documentation and proposals for the governed list are welcome now. Data contributions from outside the project (new sites, corrections, photos) open after a not-for-profit host has signed an agreement to take on the project, because the contributor terms need that host as a stable party to grant rights to. Until then, the Preview holds seeded government data and the maintainer's own submissions.

Read [CONTEXT.md](CONTEXT.md) before writing code, schema or documentation, and use its terms. Read the [ADRs](docs/adr/) that touch the area you are changing. A change that contradicts an ADR needs a new ADR that supersedes it.

## Code and documentation

1. Open an issue describing the change, unless it is a small fix.
2. Fork the repository and make the change on a branch.
3. Sign off every commit (see below).
4. Open a pull request that links the issue.

Every source file carries an SPDX licence header matching its directory (see [LICENSING.md](LICENSING.md)). Documentation follows the project's writing style: plain Australian English, sentence case headings, no dashes used as punctuation, and text that says what the thing does and how to use it.

## Checks before every commit

Run `npm install` once after cloning. It installs the git hooks (lefthook), which check every commit for the writing rules in `AGENTS.md`, a valid schema and OpenAPI spec, Prettier formatting and a DCO sign-off. Run `npm run format` to fix formatting, and `npm run check:writing`, `npm run check:schema` or `npm run check:api` to run a check on its own. Never skip the hooks with `--no-verify`.

## Sign-off (DCO)

Open Touring uses the [Developer Certificate of Origin](https://developercertificate.org/) instead of a contributor licence agreement. By adding a sign-off line to a commit, you certify that you wrote the change or otherwise have the right to submit it under the licence of the directory it lands in.

Add the line with `git commit -s`:

```
Signed-off-by: Your Name <you@example.com>
```

Use your real name or a name you are known by in the community. Pull requests with unsigned commits cannot be merged. To sign off commits already made on your branch, run `git rebase --signoff main` and force-push the branch.

## Proposing a site type or facility

Site types and facilities come from a governed list, so that every partner app can rely on the same values. To propose an addition or a change:

1. Check the current list in `schema/` and the existing issues, in case it is already covered or proposed.
2. Open an issue titled "Governed list: add `<proposed_value>`" (or "change" or "retire").
3. In the issue, give:
   - the proposed value in `snake_case`, and whether it is a site type or a facility
   - a one-sentence definition
   - any attributes it needs (for example `max_length_m` or `fee_aud`), with units
   - the matching OpenStreetMap tags and schema.org type or property, or "none"
   - at least two real examples, from at least two countries if possible
   - how it differs from the nearest existing value
4. Discussion runs on the issue. The maintainer (later the steering group) accepts, declines or asks for changes, and an accepted value is added in a schema release.

Values stay global: no country-specific values, metric units only, ISO 3166 codes for regions and IANA names for time zones.

## Data contributions

Outside data contributions are not open yet. When they open, every contributor will accept the data contributor terms first, and partner apps will need each contributor's consent to those terms before submitting on their behalf. The plain-English draft of those terms is in [docs/contributor-terms-draft.md](docs/contributor-terms-draft.md) and is not in force.

If you represent a council, tourism body or park agency and can release data under CC BY 4.0 or a compatible licence, open an issue or email hello@opentouring.org. Seed sources are imported through the same moderation pipeline as other submissions and credited in every fact they supply.

## Conduct and security

Everyone in project spaces follows the [code of conduct](CODE_OF_CONDUCT.md). Report security problems privately as described in [SECURITY.md](SECURITY.md), not in a public issue.

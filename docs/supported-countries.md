<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Supported countries

The schema is global ([ADR 0012](adr/0012-own-versioned-json-schema-with-osm-and-schema-org-mappings.md)), but OTWD only accepts and moderates records in countries it supports. A country is supported once every item of the onboarding checklist below is done, because moderating safety facts needs boundaries, authorities and people who know the place. The fixed checks reject a submission whose location is outside a supported country ([docs/architecture.md](architecture.md#moderation-pipeline)).

## Supported now

| Country   | ISO 3166-1 | Status                                                                                                                                                                                                                                   |
| --------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Australia | `AU`       | Preview. Victoria (`AU-VIC`) is the first state to be seeded and moderated ([ADR 0024](adr/0024-one-state-first.md)), then New South Wales and Western Australia. Other states and territories open once their checklist items are done. |

Within a country, states and territories (ISO 3166-2 subdivisions) open one at a time on the same checklist, because fire authorities, road authorities and seed sources differ between them.

## Onboarding a new country

Open a tracking issue titled "Country: `<ISO 3166-1 code>` onboarding" and tick each item on it with a link to the evidence. A subdivision of a supported country uses the same list and skips the items already done for the country.

1. **Boundaries.** An openly licensed source of the country's border and its ISO 3166-2 subdivisions, under a compatible licence, for the fixed checks and derived values. The IANA time zones that cover it.
2. **Fire authorities.** The fire authorities or equivalents, their district boundaries as a seed source, and the address of each authority's official live fire ban information, so the fire district can be computed ([ADR 0026](adr/0026-fire-policy-not-fire-bans.md)). Where the country has no fire districts, an ADR says what replaces them.
3. **Road and ferry authorities.** The authorities that close roads seasonally, sign vertical clearances and limits, and run or license ferries, with the links seasonal closures and temporary closures will point to.
4. **Seed sources.** Each candidate checked with the licence checklist in [docs/extending.md](extending.md#new-seed-source) and added to [docs/seed-sources.md](seed-sources.md). A country can open with no seed sources, but the issue says so.
5. **Moderators.** At least two moderators approved by the steering group who know the country's roads and travel, and can read its main languages.
6. **Language.** The languages travellers there use. Governed list translations into them, or a decision recorded on the issue that en-AU labels serve until translations come ([ADR 0031](adr/0031-governed-lists-and-the-api-are-translatable.md)).
7. **Key schemes and other national lists.** Any national scheme a governed list needs, such as the central key that opens accessible toilets (ADR 0033) or the self-contained vehicle certification that camping rules accept (ADR 0043), and any new governed list codes, proposed through the governed list process.
8. **Units and formats.** Confirmation that local signs can be recorded in metric units. Where signs show imperial units, moderators convert them and the issue records how.
9. **Legal review.** Advice on publishing contributed data and photos of that country under its law: privacy law for contributors there, any database right, and rules on photographing people and property. Changes the advice needs go into [the privacy policy draft](policies/privacy-draft.md), [the takedown process](policies/takedown.md) or the contributor terms.
10. **Safety facts.** A check that the existing safety facts cover what travellers there rely on. A new safety fact follows [its own process](extending.md#new-safety-fact).
11. **Decision.** An ADR recording the country's support, approved by the steering group, and a row in the table above.

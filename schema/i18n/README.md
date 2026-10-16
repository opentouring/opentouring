<!-- SPDX-License-Identifier: Apache-2.0 -->

# Governed list translations

The governed lists in `schema/` are written in en-AU, the reference language. This folder holds their translations into other languages, one file per governed list per language:

```
i18n/
└── <language>/
    ├── facilities.json
    ├── site-types.json
    └── ...
```

`<language>` is a BCP 47 tag, such as `de`, `fr-CA` or `pjt` (Pitjantjatjara). Use the base language (`de`) for text that suits every region, and add a regional tag (`de-AT`) only for the entries that differ there: a missing entry falls back from `de-AT` to `de` and then to en-AU, so nothing shows blank.

## What a translation holds

A translation follows `../translation.schema.json`. It names its `list`, its `language` (the same as its folder) and the `reference_version` of the governed list it was translated from, and gives the text for each code it covers:

```json
{
  "$schema": "https://schema.opentouring.org/otwd/v1/translation.schema.json",
  "list": "facilities",
  "language": "de",
  "reference_version": "1.0.0",
  "entries": {
    "toilets": {
      "label": "...",
      "description": "...",
      "attributes": { "kind": "..." }
    }
  }
}
```

It holds labels, descriptions and attribute descriptions only. Codes, safety facts, attributes, ranks, passages and mappings stay in the reference list, so a translation can never change what a code means. Every code and attribute it names must exist in the reference list. Leave out any code you have not translated.

## Adding or changing a translation

1. Copy the label and description of each entry from the reference list and write them in your language. Write them yourself, or check every line of a draft against the reference: unreviewed machine translation is not accepted.
2. Save the file as `i18n/<language>/<list file>`, with `reference_version` set to the version of the list you translated from.
3. Run `npm run check:schema`. It checks the file against the schema, the reference list and its folder.
4. Open a pull request titled "Governed list: `<language>` translation of `<list>`", with the governed-list label. It is reviewed like any governed list change, by a speaker of the language, before it merges.

When the reference list gains entries, they show in en-AU until someone translates them and raises `reference_version`.

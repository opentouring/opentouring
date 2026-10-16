---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Governed lists and the API are translatable, with en-AU as the reference language

OTWD is global from the start ([ADR 0012](0012-own-versioned-json-schema-with-osm-and-schema-org-mappings.md)), so the text the project writes is not locked to Australian English. en-AU is the reference language: the governed lists, their labels and descriptions, and the documentation are written in it, and every other language is a translation keyed by code. A label or description with no translation falls back from the requested tag to its base language (de-AT to de) and then to en-AU, so nothing shows blank.

Translations live in `schema/i18n/<BCP 47 tag>/`, one file per governed list, such as `schema/i18n/de/facilities.json`, and follow `schema/translation.schema.json`. A translation holds only text keyed by code: labels, descriptions and attribute descriptions. Codes, safety facts, attributes, ranks, passages and mappings stay only in the reference list, so a translation can never change what a code means or whether it is a safety fact. `schema/tools/validate.py` checks that every code and attribute a translation names exists in the reference list, that it carries no other fields and the SPDX header, and that its language matches its folder and is not en-AU. Language tags compare case-insensitively, and folder names use the tag's canonical case, such as `en-US`.

Translations are contributed as pull requests and reviewed like any governed list change, by a speaker of the language. A web tool for people who do not use git, planned to be Weblate (open source, with free hosting for libre projects), can come later and write the same files.

The governed list endpoints of the API honour `Accept-Language`, answer with `Content-Language` and send `Vary: Accept-Language`, and an entry that fell back to another language says so in `label_lang` or `description_lang`. Record responses are not translated: they carry codes, which apps label from the governed lists in the traveller's language, and `LocalisedText`, whose free text stays in the language the contributor wrote, with its `lang` tag. A machine translation that a partner app or the website shows is marked as machine translated, and it is never submitted or stored as a fact, because it is not anyone's own words and it may be wrong.

## Considered options

- **en-AU only.** Rejected: OTWD is global, and travellers who read another language would see labels they cannot read on every record.
- **Translations inside the reference files**, as a map of labels by language on each entry. Rejected: every translation would touch the file that holds safety flags and mappings, so a translation pull request could change what a code means, and the reference files would grow with every language.
- **Machine-translate the governed lists and descriptions on the fly.** Rejected as a source of facts: the text would be unreviewed, could be wrong on a safety fact, and would carry no contributor's provenance. Apps may still show their own machine translation, marked as such.

## Consequences

The validator checks `schema/i18n` and the translation examples on every commit. The schema ships with no translations yet: the folder holds only a README explaining how to add one, and the examples (en-US labels such as "Restrooms" and "RV park") show the format without being published. The website will get per-language routes later. Free text in records keeps one language per entry, so a description can be offered in several languages only when contributors write it in each.

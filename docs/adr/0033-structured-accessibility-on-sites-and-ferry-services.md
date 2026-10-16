---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Structured accessibility on sites and ferry services

OTWD records access for people with disability as a structured `accessibility` fact on sites and on ferry services. The fact gives wheelchair access per feature as yes, limited or no with a note, the detail of accessible toilets, accessible parking, step-free access, paths and hearing loops, and a basis that says what the fact rests on. The `accessible_facilities` facility stays, read from the new fact like `pets_allowed` is read from `pets`. A traveller with a disability plans a stop around whether they can use the toilet, the shower and the path between them, and a single "accessible" flag cannot tell them that.

A site's features are arrival (the entrance, reception or wherever a traveller arrives), toilets, showers, parking, paths, pitches, cabins and the camp kitchen. A ferry service's features are boarding, seating and toilets, and access at its terminals is recorded on the terminal sites. Three values per feature follow OSM's `wheelchair=yes|limited|no`, which travellers and mappers already use, and limited carries a note because the reason (a steep ramp, a narrow door, help needed) decides whether a particular traveller can manage.

Accessible toilets record wheelchair accessible and ambulant counts separately, whether there is a Changing Places toilet and how many, and the central key that opens them. A count is recorded only when someone counted. A source that only says yes or no sets wheelchair access to the toilets, or `ambulant` for ambulant toilets, and leaves the count unknown, because a count of 1 invented from a yes would tell a traveller there is exactly one. The ferry service fact carries the same toilet detail as a site, because a long crossing with no accessible toilet matters as much as a stop without one.

Key schemes are a new governed list (`key-schemes.json`) with the countries each is used in, from primary sources: MLAK in Australia, the RADAR key (National Key Scheme) in the United Kingdom, and the Eurokey in Germany, Austria, Switzerland and Czechia (`docs/research/mapping-verification.md`). A record's key scheme must be one used in its country, a check the validator applies. A country joins a scheme by proposal when a source names it.

The basis is one of assessed to a named standard (the standard as free text, such as AS 1428.1-2021, because each country publishes its own), signposted, reported by the operator, or observed by a contributor. It sits inside the value, beside the usual provenance, because provenance says who reported the fact and the basis says how they know: a contributor can report an access audit the operator published, and a seed source can carry a council's own observation. Operator reported is a basis of its own because seed imports and operators' own pages are neither an assessment against a standard, nor a sign at the site, nor something a contributor saw. Folding them into one of the other three would claim more than the source says.

`accessible_facilities` is derived by one rule. It is absent when no feature is recorded. It is not available when arrival is no or every recorded feature is no, because a traveller who cannot get in cannot use the rest, and OSM gets `wheelchair=no`. Otherwise it is available, with `wheelchair` yes when arrival is yes and every recorded feature is yes, and limited in every other case, including an arrival nobody recorded, which gives limited at best. The validator checks the compact form against the rule.

Accessibility is not a safety fact and does not join the always-human list. It does not decide whether a vehicle can reach a site or whether a traveller has water, and routing every change to moderators would slow the many small corrections it attracts. A wrong yes, though, can strand a traveller who drove hours on the strength of it, while a wrong no or limited costs far less. So the fixed checks flag a submission that raises wheelchair access for any feature to yes, sets step-free access or Changing Places to true, or says no key is needed. The flag is recorded as `accessibility_raised` in the moderation decision's `routing.fixed_check_flags`, routing sends the submission to a person once automatic approval is enabled, and a decision by a routing rule on it fails validation. It is a fixed-check result, not a membership of the always-human list, because it depends on the values submitted and not only on the fields touched, and the always-human list follows from the kind and the fields alone. Lowering a value stays eligible for automatic approval.

The site list endpoint gains `wheelchair`, `wheelchair_feature`, `key_scheme` and `accessibility_known` filters, and the ferry service list gains `wheelchair_boarding` and `accessibility_known`, with one meaning on both: a record with no accessibility fact, or none for a feature the request filters on, is left out. They let a partner app answer the question travellers ask, such as which caravan parks along a route have an accessible shower that opens with an MLAK key. The key schemes are served at `/v1/key-schemes` like every other governed list.

## Considered options

- **Keep the facility with a features list.** Rejected: yes or absent per feature cannot say limited, hides ambulant toilets and key schemes, and records nothing on ferry services.
- **A facility per feature (`accessible_toilets`, `accessible_showers` and so on).** Rejected: it multiplies facility codes, splits one assessment across many facts with separate provenance, and still has nowhere for the basis.
- **Mark accessibility as a safety fact.** Rejected for the reasons above. The `accessibility_raised` fixed check carries the asymmetry between a wrong yes and a wrong no instead.
- **An enum of national standards for the basis.** Rejected: the schema stays global, and a free-text standard name serves every country without a governed list that would only ever grow.
- **Record a seed source's yes as a count of 1.** Rejected: it invents a number the source never published.

## Consequences

The `accessible_facilities` facility changes shape: it is now read from the `accessibility` fact, so the full form and submissions reject it in the facilities map, and the compact form fills it in by the rule above. Its attribute values become the feature names of the new fact. The schema is a draft until v1.0.0 ([ADR 0030](0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)), so this ships without a version bump. Seed sources map onto the fact as set out in `schema/README.md`: the National Public Toilet Map and the National Formal Rest Areas (both blocked on their licences), the state rest area datasets' accessible toilet flags and the Victorian Recreation Sites disability access field, all with the basis operator reported and no invented counts.

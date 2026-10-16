---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Structured accessibility on sites and ferry services

OTWD records access for people with disability as a structured `accessibility` fact on sites and on ferry services. The fact gives wheelchair access per feature as yes, limited or no with a note, the detail of accessible toilets, accessible parking, step-free access, paths and hearing loops, and a basis that says what the fact rests on. The `accessible_facilities` facility stays, read from the new fact like `pets_allowed` is read from `pets`. A traveller with a disability plans a stop around whether they can use the toilet, the shower and the path between them, and a single "accessible" flag cannot tell them that.

A site's features are arrival (the entrance, reception or wherever a traveller arrives), toilets, showers, parking, paths, campsites, cabins and the camp kitchen. A ferry service's features are boarding, seating and toilets, and access at its terminals is recorded on the terminal sites. Three values per feature follow OSM's `wheelchair=yes|limited|no`, which travellers and mappers already use, and limited carries a note because the reason (a steep ramp, a narrow door, help needed) decides whether a particular traveller can manage. Accessible toilets record wheelchair accessible and ambulant counts separately, whether there is a Changing Places toilet, and the central key that opens them. Key schemes are a new governed list (`key-schemes.json`) with the countries each is used in: MLAK in Australia and New Zealand, the RADAR key in the United Kingdom and the Eurokey in central Europe. A site's key scheme must be one used in its country, a check the validator applies.

The basis is one of assessed to a named standard (the standard as free text, such as AS 1428.1-2021, because each country publishes its own), signposted, reported by the operator or a seed source, or observed by a contributor. It sits inside the value, beside the usual provenance, because provenance says who reported the fact and the basis says how they know: a contributor can report an access audit the operator published, and a seed source can carry a council's own observation.

Accessibility is not a safety fact and does not join the always-human list. It does not decide whether a vehicle can reach a site or whether a traveller has water, and routing it all to moderators would slow the many small corrections it attracts. Moderators still treat a change to yes with care, because a wrong yes can strand a traveller who drove hours on the strength of it, and a change to no or limited costs far less if it is wrong.

## Considered options

- **Keep the facility with a features list.** Rejected: yes or absent per feature cannot say limited, hides ambulant toilets and key schemes, and records nothing on ferry services.
- **A facility per feature (`accessible_toilets`, `accessible_showers` and so on).** Rejected: it multiplies facility codes, splits one assessment across many facts with separate provenance, and still has nowhere for the basis.
- **Mark accessibility as a safety fact.** Rejected for the reasons above. The moderation guidance carries the asymmetry between a wrong yes and a wrong no instead.
- **An enum of national standards for the basis.** Rejected: the schema stays global, and a free-text standard name serves every country without a governed list that would only ever grow.

## Consequences

The `accessible_facilities` facility changes shape: it is now read from the `accessibility` fact, so the full form and submissions reject it in the facilities map, and the compact form fills it in with a `wheelchair` attribute (yes when every recorded feature is yes, limited otherwise) and the features whose access is yes. Its attribute values become the feature names of the new fact. The schema is a draft until v1.0.0 ([ADR 0030](0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)), so this ships without a version bump. The site list endpoint gains `wheelchair`, `wheelchair_feature`, `key_scheme` and `accessibility_known` filters, the ferry service list gains `wheelchair_boarding`, and the key schemes are served at `/v1/key-schemes`. Seed sources map onto the fact as set out in `schema/README.md`: the National Public Toilet Map (still blocked on its licence), the rest area datasets' accessible toilet flags and the Victorian Recreation Sites disability access field.

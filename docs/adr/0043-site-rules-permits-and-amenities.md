---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Camping rules, permits, tidal access and site rules

OTWD records the standing rules a traveller needs before they set off, following the fire policy approach ([ADR 0026](0026-fire-policy-not-fire-bans.md)): the rule as the authority publishes or signs it, the authority, and a link to its page, never enforcement or day-to-day decisions. Seven facts carry them.

`camping_rules`, on sites and road segments, says whether overnight camping is allowed, restricted or prohibited, with the council or land manager that sets the rule and its page. Restricted covers every conditional case, such as marked bays only, a permit or a self-contained vehicle, and `self_contained` says whether only certified self-contained vehicles may camp and which certification schemes the authority accepts. The rule comes from the authority, not the site: in New Zealand, section 10 of the Freedom Camping Act 2011 permits freedom camping on council land in a tent or a self-contained vehicle unless a bylaw restricts or prohibits it, and permits it in a vehicle that is not self-contained "only if it is permitted in that area" by a bylaw under section 11A or other legislation. In Australia, councils set camping rules in their local laws, such as Logan City Council: "Our local laws changed in 2022 to prohibit camping on Council owned or controlled land which includes roadsides, footpaths, road reserves, parks and other public places."

Self-contained certification schemes are a new governed list (`self-contained-schemes.json`) with the countries each is used in, like key schemes ([ADR 0033](0033-structured-accessibility-on-sites-and-ferry-services.md)), and `statutory`, true when the certificate is issued under a law. It starts with two entries:

- `nz_self_containment`: the certificate of self-containment under the Plumbers, Gasfitters, and Drainlayers Act 2006, which the Freedom Camping Act defines as what makes a vehicle self-contained. Section 87U(4)(a) of the 2006 Act requires a toilet "permanently fixed to the vehicle" and "usable within the vehicle". The Plumbers, Gasfitters and Drainlayers Board is the regulator, and its page says: "From 7 June 2026, only vehicles certified with a green warrant are recognised as self-contained. Vehicles with the old blue warrant certification cannot be used for freedom camping." The old blue certificates therefore get no code.
- `cmca_scv`: the Campervan and Motorhome Club of Australia's self-contained vehicle accreditation, which is not a law. The club's page says "Vehicle owners must sign a declaration that they will comply with the SCV policy" and that qualified vehicles "will display an accreditation card", and Burnie City Council deems a vehicle self-contained for its RV camping permit "if it is accredited by the Campervan and Motorhome Club of Australia".

A record's scheme must be one used in its country, and `required` true makes camping restricted. The validator checks both.

`permits`, on sites and road segments, lists the permits a traveller needs: to enter a park (`park_entry`), to camp (`camping`), to enter land held by its traditional owners or a community (`land_entry`), to travel along a road through such land (`transit`), or another kind described in notes. Each permit names the authority that issues it and its page, whether it must be obtained in advance, and whether it is free. OTWD records that a permit is needed, never a traveller's permit. Aboriginal land permits are the reason the record names the issuer rather than the land: the Central Land Council says "Our permits are a legal requirement under federal and Northern Territory (NT) laws" and "We issue transit and simple permits free of charge", the Northern Land Council says "Commonwealth and Northern Territory law says that entry to Aboriginal land requires a written permit", and in Western Australia "A Transit Permit is required when traveling between the Northern Territory border and Laverton along the Great Central Road" and "Transit Permits are issued free-of-charge". Park passes work the same way, such as South Australia's Desert Parks Pass, a "12-month vehicle entry and camping for desert parks permit".

`tidal_access`, on sites and road segments, says that reaching the site or driving the segment depends on the tide, with the hours either side of low tide the signs or the authority advise, the tide station, and the tide authority's prediction page, such as the Bureau of Meteorology's "Tide Predictions for Australia, South Pacific and Antarctica" or Land Information New Zealand's tide predictions. OTWD never stores tide times, which the authority publishes for every day. It is a safety fact: a traveller caught by the tide on a beach drive can lose the vehicle or their life, so every change goes to a moderator.

Sites gain four more facts. `quiet_hours` holds local clock times read in the site's time zone ([ADR 0032](0032-utc-for-instants-local-time-for-schedules.md)). `age_rules` says whether children are allowed, the age from which an adults-only site takes guests and the age of the person who books. `firewood` says whether the operator sells or provides firewood and whether travellers may collect it, which replaces the `bring_own_firewood` attribute of `fires_allowed`, so the rule is held once. `seasonal_operation` holds the periods each year the site operates, as local month and day: the operator's own season, distinct from a seasonal closure an authority declares and from a temporary closure. A site gives its season in `seasonal_operation` or as `opening_hours.seasonal_closures`, never both, so the two cannot disagree, and the validator checks it.

None of these is a safety fact except `tidal_access`. A wrong camping rule, permit or quiet hour costs a traveller a fine or a move, not their safety.

## Considered options

- **Store live enforcement or closures, such as a council's daily list of closed camping areas.** Rejected for the reason fire bans are not stored: a stale "allowed" would be wrong in a way the traveller cannot see. The authority's page is the source.
- **Self-contained schemes as an enum.** Rejected: schemes are national and new ones appear, so a governed list with countries lets a country join by proposal, as key schemes do.
- **List only statutory schemes.** Rejected: Australian councils accept the CMCA accreditation in their own rules, so a traveller there needs it. `statutory` keeps the difference visible.
- **Camping legality as a site facility.** Rejected: a facility is yes or no, and the rule needs restricted, an authority and a link.
- **Permit kinds as a governed list.** Rejected for now: the five kinds are global, and `other` with notes covers the rest. A governed list can replace the enum before v1.0.0 if new kinds keep appearing.
- **Tide times from an authority feed.** Rejected: OTWD would become a slower copy of the authority's predictions, and a wrong time is dangerous.
- **A season inside opening hours.** Rejected: `opening_hours` needs a weekly pattern or an OSM string, and many seasonal sites publish only their months.

## Consequences

The schema is a draft until v1.0.0 ([ADR 0030](0030-schema-and-api-stay-a-draft-until-v1-0-0-is-released.md)), so removing `bring_own_firewood` ships without a version bump, and the examples move it to `firewood.collection`. The site list gains `camping`, `self_contained_required`, `camping_rules_known`, `permit_kind`, `tide_dependent`, `children_allowed`, `age_rules_known` and `open_on` filters, and the road segment list gains `camping`, `self_contained_required`, `camping_rules_known`, `permit_kind` and `tide_dependent`, because "where can I camp tonight in a vehicle that is not certified" and "which roads on my route need a permit" are searches a partner app cannot answer by fetching every record. The self-contained schemes are served at `/v1/self-contained-schemes`.

Mappings, checked on the OSM wiki, taginfo and schema.org on 2026-10-16 (`docs/research/mapping-verification.md`): `camping=yes` and `camping=no` (in use) are documented for natural areas only, so they map as related. No OSM key is documented for a self-contained requirement. `access=permit` is documented on Key:access and `permit=*` is in use but documents no camping or land values, so permits map as related. `quiet_hours=*` is a proposal (status proposed). `min_age=*` is de facto, and no adults-only key is documented. No key is documented for firewood collection, and `wood_provided=*` (in use) is for fire places. `tidal=yes` describes an area in the tidal range, not access, and the `access:tide` key has 67 uses and no wiki page, so tidal access has no mapping. `seasonal=*` (de facto) and `opening_hours` month ranges map to the season. In schema.org, `Permit` has `issuedBy` and `validIn`, `openingHoursSpecification` takes `validFrom` and `validThrough`, and `typicalAgeRange` is defined only for creative works and events, so age rules, quiet hours and camping rules have no schema.org property.

## Open questions

- **4WD recovery points.** The scope named 4WD recovery points or similar. No primary source found in this session describes fixed recovery points a land manager provides on a track, OSM has no documented tag, and in four-wheel driving "rated recovery points" usually means the points on a vehicle. They are not modelled until a source shows what travellers would look for.
- **New Zealand transition regulations.** The transition period was extended by regulations made in 2025, which the regulator's page names. Their text could not be retrieved from legislation.govt.nz in this session, so the end date rests on the regulator's page.
- **Other countries.** No other national self-contained certification scheme was searched for beyond Australia. A country joins the list by proposal when a primary source names its scheme.
- **Queensland camping permits.** The Queensland Parks and Wildlife Service booking pages returned 403 in this session, so their wording is not quoted.

## Sources

- Freedom Camping Act 2011 (NZ), sections 4, 10, 11, 11A and 15: https://www.legislation.govt.nz/act/public/2011/0061/latest/whole.html
- Self-contained Motor Vehicles Legislation Act 2023 (NZ): https://www.legislation.govt.nz/act/public/2023/0024/latest/whole.html
- Plumbers, Gasfitters and Drainlayers Board, private vehicle owners: https://www.pgdb.co.nz/self_contained_vehicles/private_vehicle_owners/
- CMCA self-contained vehicle policy: https://members.cmca.au/content/scvgov
- Burnie City Council RV camping permit: https://www.burnie.tas.gov.au/Explore/Parks-and-Reserves/Cooee-Point-Reserve/RV-Camping-Permit
- Logan City Council camping: https://www.logan.qld.gov.au/about-council/local-laws-and-policies/camping-on-council-owned-or-controlled-land
- Central Land Council permits: https://www.clc.org.au/permits/
- Northern Land Council permits: https://www.nlc.org.au/permits
- Western Australia, permits to access or travel through Aboriginal land: https://www.wa.gov.au/service/aboriginal-affairs/aboriginal-heritage-conservation/apply-permit-access-or-travel-through-aboriginal-land
- Desert Parks Pass: https://www.parks.sa.gov.au/book-and-pay/desert-parks-pass
- Bureau of Meteorology tide predictions: https://www.bom.gov.au/australia/tides/
- Land Information New Zealand tide predictions: https://www.linz.govt.nz/products-services/tides-and-tidal-streams/tide-predictions

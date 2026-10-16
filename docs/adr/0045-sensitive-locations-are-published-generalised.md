---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Sensitive locations are published generalised

Some places must not have their exact position published: a sacred site or a place of restricted cultural knowledge, or a place beside a nesting beach or the habitat of a threatened species that visitors would disturb. A site can now carry a `location_sensitivity` fact with a reason from a new governed list (`location-sensitivity-reasons.json`: `cultural_heritage`, `threatened_species` and `breeding_wildlife`). The site's published `location` is then generalised to a grid: its latitude and longitude are rounded to the nearest multiple of `generalised.cell_deg`, which is 0.01 (about 1.1 km north to south), 0.1 (about 11 km) or 1 degree, and must be at least as coarse as the reason's `min_cell_deg` (0.1 for cultural heritage and threatened species, 0.01 for breeding wildlife). `accuracy_m` and the derived `locality` are left out, because both can point at the place. The exact position is held privately for moderation.

The grid follows the GBIF guidance on sensitive species data (Chapman 2020), which recommends generalising coordinates to 0.1 degrees (about 10 km) where finer locations would expose a species to disturbance or exploitation and to 0.01 degrees (about 1 km) where they would expose it to collection or damage. The same guidance says "Randomization is a methodology that I strongly recommend not be used", and a grid has a second advantage here: a rounded coordinate can be checked, so the validator proves that a sensitive site carries no exact coordinates. It also says "Data should never be altered, falsified or deleted from the stored record", which is why the exact position is kept, privately, rather than thrown away.

## Who decides and how

Anyone can ask for a site's location to be marked sensitive: a contributor through an `update_facts` submission proposing the fact, or Traditional Owners, custodians, a land council or a land manager by writing to the project privately, without saying publicly why. A moderator records every marking: `location_sensitivity` carries the `x-otwd-always-human` marker, so every submission that sets, changes or removes it is on the always-human list, and a routing rule can never decide it. The marking itself carries no free text, so nothing about the place or the request is published beyond the reason code and an optional review date.

A request from a site's Traditional Owners, custodians or land council for `cultural_heritage` is accepted without asking them to explain or prove the cultural reason. The moderator checks only that the request comes from people who speak for that place, such as through the land council. This follows the AIATSIS Code of Ethics for Aboriginal and Torres Strait Islander Research, which says "Indigenous peoples have the right to manage the collection, interpretation and use of their information" and "Where a conflict arises between accessibility and Indigenous peoples rights, then Indigenous peoples' rights should prevail", the Maiam nayri Wingara principles, under which Indigenous peoples have the right to "Exercise control of the data ... including creation, development, stewardship, analysis, dissemination, and infrastructure", and the OpenStreetMap Australian tagging guidelines, which say to "defer to that community on how it should be presented". A marking for cultural heritage is lifted only with the agreement of the people who asked for it. A marking for wildlife rests on a land manager's or wildlife agency's advice and carries a `review_on` date where they give one, because the GBIF guidance says sensitive data "should include a date for review" and that "the presumption remains in favour of release".

Once a site is marked, the fixed checks flag every later submission that changes its location, names or description, or adds a photo of it, as `sensitive_location` in the moderation decision's `routing.fixed_check_flags`. These go to a person, because each can identify the place, and a routing rule that decides one fails validation. Contributors still submit the exact position, and the AI review sees only the generalised one.

## What is never published

The exact position of a sensitive site never appears in the API (compact or full view, JSON or GeoJSON), in bulk downloads or in the change feed. The schema enforces this for every public shape that holds coordinates: the full form and the compact form require a generalised location when the site is sensitive and reject `accuracy_m` and `locality`, the GeoJSON feature (`site-feature.schema.json`) must carry exactly the published location as its geometry, and the validator rejects coordinates off the grid. The change feed names changed fields, never values. Submissions, moderation decisions and verdicts, which hold the exact position, are not published: a partner app sees only the decision summary. `bbox`, `near` and `distances_km` use the generalised position, so repeated queries cannot narrow it down. Only sites can be marked: a road restriction's location is a safety fact and stays exact, and a road segment's geometry cannot be generalised without misleading a driver.

## Considered options

- **Leave sensitive places out of OTWD.** Kept as an option for the people who speak for a place, but not the default: a site such as a walk to a rock art gallery that its custodians open to visitors still needs its permit and rules recorded. A request to remove a record entirely is a moderation matter, raised as an open question below.
- **Offset the published point by a random distance.** Rejected: the GBIF guidance advises against randomisation, a random point looks exact and can mislead, and nobody could check that a published point was generalised.
- **A circle with a stated radius.** Rejected for the same reason: the centre of the circle would be either exact or random. A grid cell is reproducible and checkable.
- **A free-text reason or the requester's name in the record.** Rejected: it would publish what the request exists to protect.
- **Let any contributor's request take effect at once.** Rejected: a false marking hides a place travellers need, and a false removal publishes one its custodians asked to protect, so a person decides every change.
- **Mark it as a safety fact to put it on the always-human list.** Rejected: it is not about a traveller's safety, so a marker of its own keeps the safety fact list honest.

## Consequences

The site's location value becomes `SiteLocation`, which adds `generalised` to the coordinates. Road restrictions keep `Location`, which has no `generalised`. Submissions reject a generalised location. Moderation decisions gain the `sensitive_location` flag, and the always-human list gains facts marked `x-otwd-always-human`, read by the fixed checks and `tools/validate.py` from the schema like the safety fact markers. The reasons are served at `/v1/location-sensitivity-reasons`. A position published before a site was marked stays in copies people already downloaded, which OTWD cannot recall: later downloads and every API response carry only the generalised position. OSM has no tag for a culturally restricted or sensitive place (checked on 2026-10-16, `docs/research/mapping-verification.md`), so the reasons map to none. schema.org has `GeoCircle` with `geoMidpoint` and `geoRadius` for an approximate area, so a website page for a sensitive site can describe the grid cell with it (related), and gives no way to mark a place sensitive.

## Open questions

- **Removing a record at its custodians' request.** Whether a record is closed, hidden or deleted when the people who speak for a place ask for it to be removed belongs with the moderation policy, and is not settled here.
- **Australian heritage registers.** The access rules of state Aboriginal heritage registers, such as NSW AHIMS, were not confirmed from a primary source in this session, so OTWD's approach is not compared with them.
- **AIATSIS access and use policy.** The AIATSIS policy on access to culturally sensitive collection material was not quoted from its primary text in this session.

## Sources

- AIATSIS Code of Ethics for Aboriginal and Torres Strait Islander Research (2020): https://aiatsis.gov.au/sites/default/files/2022-02/aiatsis-code-ethics-jan22.pdf
- Maiam nayri Wingara principles: https://www.maiamnayriwingara.org/mnw-principles
- OSM wiki, Australian Tagging Guidelines/Australia's First Peoples: https://wiki.openstreetmap.org/wiki/Australian_Tagging_Guidelines/Australia's_First_Peoples
- Chapman AD (2020) Current Best Practices for Generalizing Sensitive Species Occurrence Data. GBIF Secretariat: https://docs.gbif.org/sensitive-species-best-practices/master/en/ (https://doi.org/10.15468/doc-5jp4-5g10)
- schema.org GeoCircle: https://schema.org/GeoCircle

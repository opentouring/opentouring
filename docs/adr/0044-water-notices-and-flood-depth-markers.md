---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Water notices and flood depth markers

OTWD records two safety notices that the review found missing, both as policy plus an authority link ([ADR 0026](0026-fire-policy-not-fire-bans.md)), and both on the always-human list like bait notices ([ADR 0034](0034-pet-policies-pet-transit-and-bait-notices.md)).

## Water notices

A site's `water_notices` lists boil water and other water quality notices for its supply: the kind (`boil_water`, `do_not_drink`, `do_not_use`, or `other` with notes), the area or supply the notice covers, the local dates it runs from and to, and the authority that issued it with its page. Drinking water points are sites, so they carry the fact too. A notice with no `to` date stays until the authority lifts it, and a notice past its `to` date stays with its dates until a moderator removes it, as bait notices do.

The authority is whoever issued the notice, because that differs by place and the record must not assume it. In Australia the Australian Drinking Water Guidelines describe boil water advisories as "public announcements advising that drinking water should be boiled (or otherwise disinfected) before being consumed", which "should only be issued after consultation between the drinking water supplier and the relevant health authority". NSW Health says "A local water utility may issue a boil water alert of its own accord. However, before issuing a boil water alert, the utility should consult with their Public Health Unit." In New Zealand, Taumata Arowai describes a boil water notice as "an instruction, put in place by a water supplier". The kinds beyond boiling cover notices that tell people not to drink the water at all, which boiling does not fix.

A water notice is a safety fact. A traveller who fills a tank from a supply under a boil water notice and drinks it untreated can become seriously ill, and a wrongly removed notice is the harm the always-human list exists to prevent. OTWD records the notice as published and never follows a utility's live water quality data: notices change faster than moderation can, and the authority is the only reliable source, so apps link to `info_url`. The API's `has_water_notice` filter matches notices current on the request date as local dates in the site's time zone, and a missing notice is unknown, never proof the water is safe. Apps that show the `drinking_water` facility show current water notices beside it.

## Flood depth markers

A road restriction's `flood_depth_marker` says whether a depth marker (a post graduated in metres) stands at a ford or causeway so travellers can read the depth of water over the road, with the road authority and its page for current road conditions. It records the marker, never a live depth: water rises and falls by the hour, and a stale depth is worse than none. `present: false` is recorded too, because a crossing with no marker is one where the depth cannot be read on site.

The fact goes on road restrictions because a ford or causeway is a point on the road, and the structures governed list already has `ford` and `causeway` (which covers floodways). The validator accepts the fact only where the structure is one of those two. A road restriction needs at least one limit, and a flood depth marker fact now counts as one for this purpose, because the water over a crossing is the physical limit there and a crossing can be worth recording for its marker alone. A floodway that runs for a long stretch is recorded as a road restriction at each marked crossing, since markers stand at points. It is a safety fact: a wrong "marker present" sends a traveller to a crossing expecting to judge the depth on site.

## Considered options

- **Store live notices or gauge readings from authority feeds.** Rejected for the reason declared fire bans are not stored: a stale "no notice" or a stale depth is dangerous.
- **A boolean on the `drinking_water` facility.** Rejected: a notice has an issuer, dates and an area, and a facility attribute cannot hold them or be time-bound.
- **Flood depth markers on road segments.** Rejected: markers are points on the road, and a road segment cannot say where along it a marker stands.
- **A new structure code for floodways.** Rejected: `causeway` is already described as a causeway or floodway.
- **Water notices as an ordinary fact.** Rejected: a removed or wrong notice can make a traveller ill, the harm the always-human list exists for.

## Consequences

The site list gains `has_water_notice` and the road restriction list gains `flood_depth_marker`. Neither has a documented OSM tag, checked on 2026-10-16 (`docs/research/mapping-verification.md`): `drinking_water:legal` (in use) says that "It is not defined how to tag places signed as 'conditionally drinkable' or 'boil before drinking'", and no tag is documented for a depth marker post, while `ford=yes` (de facto) and `flood_prone=yes` (in use) describe the crossing itself. schema.org's `SpecialAnnouncement` was considered for water notices, but its own description names the coronavirus pandemic as its motivating case and its `announcementLocation` accepts only civic structures and local businesses, so the mapping is left empty.

## Open questions

- **Depth marker standards.** The primary pages of Transport for NSW (sign G9-21-2, "Road subject to flooding, indicators show depth") and of Austroads returned 403 in this session, so the national sign standard and any guidance on where markers stand are not quoted. The fact records only what a traveller sees: whether a marker is there.
- **Who issues notices in other countries.** Only Australia and New Zealand were checked. The authority field is free text for that reason.

## Sources

- Australian Drinking Water Guidelines, 3.6 Guidance for issuing and lifting boil water advisories: https://guidelines.nhmrc.gov.au/australian-drinking-water-guidelines/part-4/statistics/3.6-guidance-for-issuing-and-lifting-boil-water-advisories
- NSW Health, boil water alert guidance: https://www.health.nsw.gov.au/environment/water/Pages/boil-water-alert-guidance.aspx
- Taumata Arowai, drinking water notices: https://www.taumataarowai.govt.nz/for-the-public/drinking-water-in-an-emergency/drinking-water-notices
- OSM wiki, Key:drinking_water:legal, Key:ford, Tag:flood_prone=yes: https://wiki.openstreetmap.org/wiki/Key:drinking_water:legal, https://wiki.openstreetmap.org/wiki/Key:ford, https://wiki.openstreetmap.org/wiki/Tag:flood_prone=yes
- schema.org SpecialAnnouncement: https://schema.org/SpecialAnnouncement

<!-- SPDX-License-Identifier: Apache-2.0 -->

# Mapping to OpenStreetMap tags

This page maps OTWD governed lists and record types to the closest OpenStreetMap (OSM) tagging. The same mappings are published in machine-readable form in the `osm` field of each entry in the governed list files, and the tables of governed lists below are generated from those files.

## What the mapping is for

The mapping lets partner apps show OTWD sites alongside their own OSM-based maps, compare coverage, and translate filters from one vocabulary to the other. It does not mean OTWD data comes from OSM. OTWD never imports OSM data, because OSM is licensed under the ODbL and OTWD data is published under CC BY 4.0, which the ODbL does not allow. Mapping a tag is a statement about meaning only.

The licences also matter in the other direction. OTWD data is CC BY 4.0, and OSM accepts CC BY data only with an explicit waiver from the rights holder, so OTWD data cannot be copied into OSM on the strength of this mapping either.

## How to read it

Each entry lists one or more tag combinations. A combination with several tags means all of them together, for example `tourism=camp_site` with `fee=no`. The match column says how close the meaning is:

- **exact**: the tags mean the same as the OTWD entry.
- **broader**: the tags cover more than the entry, so some features with these tags are not this entry.
- **narrower**: the tags cover less than the entry.
- **related**: useful for finding candidates, but not equivalent.

Site types map to the tags of a whole feature. Most facilities map to attribute keys used on a campsite or caravan site feature, such as `power_supply=yes` or `sanitary_dump_station=yes`. Where OSM records the thing as a separate feature (a picnic table or a playground), the mapping says so in the note. Facilities that are observations rather than features, such as mobile coverage, have no OSM equivalent.

Rig limits have no direct mapping. OSM records `maxlength`, `maxheight` and `maxweight` on the roads and barriers that impose them, while OTWD records the effective limit for reaching and using the site.

## Site types

| Code                     | OSM tags                                                     | Match    | Note                                                                                                                 |
| ------------------------ | ------------------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------- |
| `free_camp`              | `tourism=camp_site` + `fee=no`                               | exact    |                                                                                                                      |
| `free_camp`              | `tourism=caravan_site` + `fee=no`                            | exact    | Used where the area suits self-contained vehicles only.                                                              |
| `paid_campground`        | `tourism=camp_site` + `fee=yes`                              | exact    |                                                                                                                      |
| `caravan_park`           | `tourism=caravan_site`                                       | exact    |                                                                                                                      |
| `caravan_park`           | `tourism=camp_site` + `caravans=yes`                         | related  | Some parks are mapped as camp sites.                                                                                 |
| `national_park_campsite` | `tourism=camp_site`                                          | broader  | Inside an area tagged boundary=national_park or boundary=protected_area, often with operator set to the park agency. |
| `state_forest_campsite`  | `tourism=camp_site`                                          | broader  | Inside an area tagged landuse=forest with a government operator.                                                     |
| `showground`             | `landuse=recreation_ground` + `recreation_ground=showground` | narrower | The grounds themselves. Documented as in use, not approved. Covers showgrounds but not racecourses.                  |
| `showground`             | `tourism=camp_site`                                          | related  | The camping area, mapped inside the showground.                                                                      |
| `rest_area`              | `highway=rest_area`                                          | exact    |                                                                                                                      |
| `rest_area`              | `highway=services`                                           | related  | Rest areas with fuel and food.                                                                                       |
| `rest_area`              | `tourism=camp_site` + `maxstay=*`                            | related  | Australian tagging guidelines: where camping is permitted at a rest area. maxstay gives the time limit.              |
| `dump_point`             | `amenity=sanitary_dump_station`                              | exact    |                                                                                                                      |
| `drinking_water_point`   | `amenity=water_point`                                        | exact    |                                                                                                                      |
| `drinking_water_point`   | `amenity=drinking_water`                                     | narrower | Drinking fountains, often unsuitable for filling tanks.                                                              |
| `public_toilet`          | `amenity=toilets`                                            | exact    |                                                                                                                      |
| `public_shower`          | `amenity=shower`                                             | exact    |                                                                                                                      |
| `laundromat`             | `shop=laundry` + `self_service=yes`                          | exact    |                                                                                                                      |
| `information_centre`     | `tourism=information` + `information=office`                 | exact    |                                                                                                                      |
| `information_centre`     | `tourism=information` + `information=visitor_centre`         | related  | Centres about one attraction or place of interest rather than a town or region.                                      |
| `attraction`             | `tourism=attraction`                                         | exact    |                                                                                                                      |
| `lookout`                | `tourism=viewpoint`                                          | exact    |                                                                                                                      |
| `swimming_spot`          | `leisure=swimming_area`                                      | narrower | Only an officially designated and marked swimming area within a body of water.                                       |
| `swimming_spot`          | `leisure=bathing_place`                                      | narrower | Wild swimming spots with no significant facilities. Documented as in use.                                            |
| `swimming_spot`          | `natural=beach`                                              | related  |                                                                                                                      |
| `swimming_spot`          | `leisure=swimming_pool` + `access=yes`                       | related  | Public pools.                                                                                                        |
| `boat_ramp`              | `leisure=slipway`                                            | exact    |                                                                                                                      |
| `fuel`                   | `amenity=fuel`                                               | exact    |                                                                                                                      |
| `lpg_refill_swap`        | `shop=gas`                                                   | exact    |                                                                                                                      |
| `lpg_refill_swap`        | `amenity=fuel` + `fuel:lpg=yes`                              | related  | Autogas for vehicles, which does not always include bottle refills.                                                  |
| `mechanic`               | `shop=car_repair`                                            | exact    |                                                                                                                      |
| `hospital_emergency`     | `amenity=hospital` + `emergency=yes`                         | exact    |                                                                                                                      |
| `ferry_terminal`         | `amenity=ferry_terminal`                                     | exact    |                                                                                                                      |

## Facilities

| Code                    | OSM tags                          | Match    | Note                                                                                                             |
| ----------------------- | --------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------- |
| `toilets`               | `toilets=yes`                     | exact    |                                                                                                                  |
| `toilets`               | `toilets:disposal=flush`          | related  | Maps the kind attribute value flush.                                                                             |
| `toilets`               | `toilets:disposal=pitlatrine`     | related  | Maps the kind attribute value pit. Add composting=yes when the pit toilet composts.                              |
| `toilets`               | `toilets:disposal=chemical`       | related  | Maps the kind attribute value chemical.                                                                          |
| `toilets`               | `toilets:disposal=dry_toilet`     | related  | Maps the kind attribute value composting where the toilet dehydrates or composts waste.                          |
| `showers`               | `shower=yes`                      | exact    |                                                                                                                  |
| `showers`               | `hot_water=yes`                   | narrower | Hot water available. Key:shower treats shower=hot as a tagging mistake.                                          |
| `showers`               | `shower:fee=yes`                  | related  | Maps the fee attribute.                                                                                          |
| `drinking_water`        | `drinking_water=yes`              | exact    |                                                                                                                  |
| `non_potable_water`     | `drinking_water=no`               | related  | On the tap or water point, for example man_made=water_tap.                                                       |
| `power`                 | `power_supply=yes`                | exact    |                                                                                                                  |
| `dump_point_access`     | `sanitary_dump_station=yes`       | exact    |                                                                                                                  |
| `dump_point_access`     | `sanitary_dump_station=customers` | narrower | Equivalent to guests_only true.                                                                                  |
| `bins`                  | `bin=yes`                         | exact    | A bin is available at the camp site or caravan site.                                                             |
| `bins`                  | `amenity=waste_basket`            | related  | Small bins, mapped as separate features.                                                                         |
| `bins`                  | `amenity=waste_disposal`          | related  | Large bins or skips.                                                                                             |
| `recycling`             | `amenity=recycling`               | exact    |                                                                                                                  |
| `bbq`                   | `bbq=yes`                         | exact    |                                                                                                                  |
| `bbq`                   | `amenity=bbq`                     | related  | A barbecue mapped as a separate feature.                                                                         |
| `fire_pit`              | `firepit=yes`                     | exact    | Key:fireplace is for chimneys and enclosed fireplaces, not fire pits.                                            |
| `fire_pit`              | `leisure=firepit`                 | related  | A fire pit mapped as a separate feature.                                                                         |
| `fires_allowed`         | `openfire=yes`                    | exact    |                                                                                                                  |
| `shade`                 | `shade=yes`                       | related  | Marks a feature that is in shade. Used mostly on ways and rare on camp sites.                                    |
| `picnic_tables`         | `picnic_table=yes`                | exact    | A picnic table is available at the camp site or caravan site.                                                    |
| `picnic_tables`         | `leisure=picnic_table`            | related  | Tables mapped as separate features.                                                                              |
| `playground`            | `leisure=playground`              | related  | Mapped as a separate feature.                                                                                    |
| `pool`                  | `swimming_pool=yes`               | exact    |                                                                                                                  |
| `pool`                  | `leisure=swimming_pool`           | related  | A pool mapped as a separate feature.                                                                             |
| `laundry`               | `washing_machine=yes`             | exact    |                                                                                                                  |
| `wifi`                  | `internet_access=wlan`            | exact    |                                                                                                                  |
| `mobile_coverage`       | none                              |          |                                                                                                                  |
| `pets_allowed`          | `pets=yes`                        | exact    | Documented on Key:pets as in use. pets=no when pets.allowed is no.                                               |
| `pets_allowed`          | `dog=yes`                         | narrower | Dogs only. dog=leashed when the dog rule is on_leash. See pet-species.json for other species.                    |
| `dog_off_leash`         | `leisure=dog_park`                | related  |                                                                                                                  |
| `dog_off_leash`         | `dog=unleashed`                   | related  | Dogs may be off the lead. Documented on Key:dog.                                                                 |
| `accessible_facilities` | `wheelchair=yes`                  | exact    | When the wheelchair attribute is yes.                                                                            |
| `accessible_facilities` | `wheelchair=limited`              | exact    | When the wheelchair attribute is limited.                                                                        |
| `accessible_facilities` | `wheelchair=no`                   | exact    | When available is false: arrival is no or every recorded feature is no.                                          |
| `accessible_facilities` | `toilets:wheelchair=yes`          | related  | When toilets is in features. Approved on the OSM wiki.                                                           |
| `accessible_facilities` | `capacity:disabled=*`             | related  | The count in accessibility.accessible_parking_spaces.                                                            |
| `accessible_facilities` | `centralkey=*`                    | related  | The key scheme in accessibility.toilets.key_scheme. See key-schemes.json.                                        |
| `accessible_facilities` | `changing_table:adult=yes`        | related  | When accessibility.toilets.changing_places is true. An adult change table alone is not a Changing Places toilet. |
| `accessible_facilities` | `wheelchair:description=*`        | related  | The accessibility notes.                                                                                         |
| `generators_allowed`    | none                              |          |                                                                                                                  |
| `big_rig_access`        | `maxlength=*`                     | related  | Length limits on the access road, not a property of the site.                                                    |
| `big_rig_access`        | `maxheight=*`                     | related  | Height limits on the access road, not a property of the site.                                                    |
| `big_rig_access`        | `maxweight=*`                     | related  | Weight limits on the access road, not a property of the site.                                                    |
| `drive_through_sites`   | none                              |          |                                                                                                                  |
| `ensuite_sites`         | none                              |          |                                                                                                                  |
| `cabins`                | `cabins=yes`                      | exact    |                                                                                                                  |
| `tent_sites`            | `tents=yes`                       | exact    |                                                                                                                  |
| `camp_kitchen`          | `kitchen=yes`                     | exact    |                                                                                                                  |

## Structures

| Code                 | OSM tags                    | Match    | Note                                                                                                                                                                                            |
| -------------------- | --------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bridge`             | `bridge=yes`                | exact    | Passage over: on the road way that crosses the bridge, which carries maxweight, maxaxleload and maxwidth.                                                                                       |
| `bridge`             | `maxheight=*`               | related  | Passage under: OSM has no tag for the road beneath a bridge. That road way carries maxheight and maxheight:physical, and the bridge above is a separate way with bridge=yes and a higher layer. |
| `tunnel`             | `tunnel=yes`                | exact    |                                                                                                                                                                                                 |
| `overhead_structure` | `man_made=gantry`           | narrower | Sign and toll gantries only.                                                                                                                                                                    |
| `overhead_structure` | `barrier=height_restrictor` | related  | A height barrier that warns of a low structure ahead, mapped as its own feature.                                                                                                                |
| `causeway`           | `flood_prone=yes`           | related  | On the road way. Marks a road that floods without saying whether it is built as a causeway.                                                                                                     |
| `ford`               | `ford=yes`                  | exact    |                                                                                                                                                                                                 |
| `gate`               | `barrier=gate`              | exact    |                                                                                                                                                                                                 |
| `cattle_grid`        | `barrier=cattle_grid`       | exact    |                                                                                                                                                                                                 |
| `no_structure`       | `traffic_sign=*`            | related  | The sign itself, mapped as a node beside or on the road. The limit is tagged on the road way it applies to.                                                                                     |

## Surfaces

| Code       | OSM tags              | Match    | Note                                                               |
| ---------- | --------------------- | -------- | ------------------------------------------------------------------ |
| `sealed`   | `surface=paved`       | broader  | Also covers paving stones and setts.                               |
| `sealed`   | `surface=asphalt`     | narrower |                                                                    |
| `sealed`   | `surface=chipseal`    | narrower |                                                                    |
| `sealed`   | `surface=concrete`    | narrower |                                                                    |
| `unsealed` | `surface=unpaved`     | exact    |                                                                    |
| `gravel`   | `surface=gravel`      | exact    |                                                                    |
| `gravel`   | `surface=compacted`   | exact    |                                                                    |
| `gravel`   | `surface=fine_gravel` | narrower |                                                                    |
| `gravel`   | `tracktype=grade2`    | related  | Used on highway=track ways: a firm gravel track.                   |
| `dirt`     | `surface=dirt`        | exact    |                                                                    |
| `dirt`     | `surface=earth`       | exact    |                                                                    |
| `dirt`     | `surface=ground`      | broader  |                                                                    |
| `dirt`     | `tracktype=grade4`    | related  | Used on highway=track ways: mostly soil with little hard material. |
| `sand`     | `surface=sand`        | exact    |                                                                    |
| `sand`     | `tracktype=grade5`    | related  | Used on highway=track ways: soft, uncompacted material.            |
| `clay`     | `surface=clay`        | exact    |                                                                    |
| `rock`     | `surface=rock`        | narrower | Bedrock only.                                                      |
| `rock`     | `surface=stone`       | related  |                                                                    |
| `mud`      | `surface=mud`         | exact    |                                                                    |

## Vehicle access classes

| Code                     | OSM tags                | Match    | Note                                                                                                  |
| ------------------------ | ----------------------- | -------- | ----------------------------------------------------------------------------------------------------- |
| `two_wd`                 | `4wd_only=no`           | related  | Rarely tagged. Most OSM roads without 4wd_only are passable by 2WD vehicles, but OSM does not say so. |
| `awd`                    | none                    |          |                                                                                                       |
| `four_wd_high_clearance` | `4wd_only=recommended`  | related  | A 4WD is advised but not required by sign.                                                            |
| `four_wd_only`           | `4wd_only=yes`          | exact    |                                                                                                       |
| `closed_to_vehicles`     | `motor_vehicle=no`      | exact    |                                                                                                       |
| `closed_to_vehicles`     | `access=no`             | broader  | Closed to everyone, including walkers and cyclists.                                                   |
| `closed_to_vehicles`     | `motor_vehicle=private` | narrower | Only authorised vehicles, such as a management track.                                                 |

## Vehicle classes

| Code             | OSM tags         | Match    | Note                          |
| ---------------- | ---------------- | -------- | ----------------------------- |
| `foot_passenger` | `foot=yes`       | exact    |                               |
| `bicycle`        | `bicycle=yes`    | exact    |                               |
| `motorcycle`     | `motorcycle=yes` | exact    |                               |
| `car`            | `motorcar=yes`   | exact    |                               |
| `car_towing`     | `trailer=yes`    | broader  | Any vehicle towing a trailer. |
| `car_towing`     | `caravan=yes`    | narrower | Caravans only.                |
| `motorhome`      | `motorhome=yes`  | exact    |                               |
| `heavy_vehicle`  | `hgv=yes`        | exact    |                               |
| `bus`            | `bus=yes`        | exact    |                               |

## Key schemes

| Code      | OSM tags             | Match | Note                                            |
| --------- | -------------------- | ----- | ----------------------------------------------- |
| `mlak`    | `centralkey=mlak`    | exact |                                                 |
| `radar`   | `centralkey=nks`     | exact | OSM names the scheme nks (National Key Scheme). |
| `eurokey` | `centralkey=eurokey` | exact |                                                 |

## Pet species

| Code    | OSM tags      | Match   | Note                                                                          |
| ------- | ------------- | ------- | ----------------------------------------------------------------------------- |
| `dog`   | `dog=yes`     | exact   |                                                                               |
| `dog`   | `dog=leashed` | exact   | When the species is allowed on_leash.                                         |
| `cat`   | `cat=yes`     | exact   | Documented on Key:cat as in use.                                              |
| `horse` | `horse=yes`   | related | Key:horse is access for riders on a way or area, not whether horses may stay. |

## Self-contained schemes

| Code                  | OSM tags | Match | Note                                                                                     |
| --------------------- | -------- | ----- | ---------------------------------------------------------------------------------------- |
| `nz_self_containment` | none     |       | No documented key. `self_contained=*` has 2 uses in taginfo and no wiki page.            |
| `cmca_scv`            | none     |       | No documented key. `caravans=*` and `motorhome=*` say whether a vehicle type is allowed. |

## Location sensitivity reasons

| Code                 | OSM tags | Match | Note                                                                                                                                   |
| -------------------- | -------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `cultural_heritage`  | none     |       | No documented tag. The Australian tagging guidelines for First Peoples say to "defer to that community on how it should be presented". |
| `threatened_species` | none     |       | No documented tag.                                                                                                                     |
| `breeding_wildlife`  | none     |       | No documented tag.                                                                                                                     |

## Record types and their facts

Road restrictions, road segments and ferry services are not governed lists, so their mapping is given here only. OSM records most of these facts as tags on the road way or ferry route a limit applies to.

| OTWD                                                         | OSM                                                                                        | Match   | Note                                                                                                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Road restriction                                             | `maxheight=*`, `maxwidth=*`, `maxweight=*`, `maxaxleload=*` or `maxlength=*` on a road way | related | OSM tags the way the limit applies to. OTWD records the point where it applies.                                                             |
| `vertical_clearance` measurement, basis signed               | `maxheight=*`                                                                              | exact   | In metres. OSM also accepts feet and inches, which OTWD converts.                                                                           |
| `vertical_clearance` measurement, basis surveyed or measured | `maxheight:physical=*`                                                                     | exact   |                                                                                                                                             |
| `vertical_clearance` measurement with a heading              | `maxheight:forward=*`, `maxheight:backward=*`                                              | related | OSM direction is relative to the way, OTWD's is a compass heading.                                                                          |
| `width_limit` measurement, basis signed                      | `maxwidth=*`                                                                               | exact   |                                                                                                                                             |
| `width_limit` measurement, basis surveyed or measured        | `maxwidth:physical=*`                                                                      | exact   |                                                                                                                                             |
| `weight_limit.gross_t`                                       | `maxweight=*`                                                                              | exact   |                                                                                                                                             |
| `weight_limit.axle_load_t`                                   | `maxaxleload=*`                                                                            | exact   |                                                                                                                                             |
| `length_limit.signed_m`                                      | `maxlength=*`                                                                              | exact   |                                                                                                                                             |
| Road segment                                                 | `highway=*` way                                                                            | broader | One road segment may cover several OSM ways, or part of one.                                                                                |
| `surface.condition`                                          | `smoothness=*`                                                                             | related | good: good or intermediate. fair: intermediate or bad. poor: bad or very_bad. very_poor: horrible or very_horrible. impassable: impassable. |
| `vehicle_access_class` `four_wd_only`                        | `4wd_only=yes`                                                                             | exact   | See the vehicle access class table.                                                                                                         |
| `vehicle_access_class` `closed_to_vehicles`                  | `motor_vehicle=no`                                                                         | exact   |                                                                                                                                             |
| `towing_permitted` no                                        | `trailer=no`                                                                               | exact   | `caravan=no` is narrower.                                                                                                                   |
| `towing_permitted` not_recommended                           | none                                                                                       |         | OSM has no advisory value.                                                                                                                  |
| `seasonal_closure`                                           | `motor_vehicle:conditional=no @ (Jun 10-Oct 31)`                                           | related | OSM conditional restrictions hold the period. OTWD also records the authority and its link.                                                 |
| Ferry service                                                | `route=ferry`                                                                              | exact   | On the ferry route way, with `motorcar=*`, `hgv=*`, `bicycle=*` and `foot=*` for the vehicle classes carried.                               |
| `accessibility.wheelchair` feature yes, limited or no        | `wheelchair=yes`, `wheelchair=limited`, `wheelchair=no`                                    | related | OSM tags one value on the feature itself, such as a toilet block or a path. OTWD gives one per feature of the site.                         |
| `accessibility.wheelchair.toilets` yes                       | `toilets:wheelchair=yes`                                                                   | related | OSM has no documented count for `accessibility.toilets.accessible_count`.                                                                   |
| `accessibility.toilets.ambulant` and `ambulant_count`        | none                                                                                       |         | No documented OSM key for ambulant toilets.                                                                                                 |
| `accessibility.hearing_loop`                                 | `hearing_loop=yes`                                                                         | related | Used, but the hearing loop proposal is still a draft.                                                                                       |
| `accessibility.step_free_access`                             | none                                                                                       |         | OSM records steps (`step_count=*`) and kerbs on ways and entrances, not for a whole site.                                                   |
| `pet_transit` no                                             | `dog=no` on the road way                                                                   | related | Dogs only, and OSM dog access means walking a dog, not carrying one in a vehicle.                                                           |
| `pet_transit` in_vehicle_only                                | none                                                                                       |         | OSM has no value for pets carried in a vehicle.                                                                                             |
| `bait_notices`                                               | none                                                                                       |         | No documented tag. `hazard=poison` has 6 uses and no wiki page.                                                                             |
| `pet_policy` on a ferry service                              | none                                                                                       |         | No documented tag for pets on a ferry.                                                                                                      |
| `camping_rules.camping` allowed or prohibited                | `camping=yes`, `camping=no`                                                                | related | Key:camping (in use) is documented for natural areas, not camp sites. Restricted has no value.                                              |
| `camping_rules.self_contained`                               | none                                                                                       |         | No documented key for a self-contained requirement.                                                                                         |
| `permits`                                                    | `access=permit`, `permit=*`                                                                | related | Key:access documents permit. Key:permit (in use) documents no park, camping or land values.                                                 |
| `quiet_hours`                                                | `quiet_hours=*`                                                                            | related | Key:quiet_hours is a proposal (status proposed), in opening_hours syntax.                                                                   |
| `age_rules.min_guest_age`                                    | `min_age=*`                                                                                | related | Key:min_age is de facto. No adults-only key is documented.                                                                                  |
| `firewood.provided`                                          | `wood_provided=yes`                                                                        | related | Key:wood_provided (in use) is for fire places and shelters. No key is documented for collecting firewood.                                   |
| `tidal_access`                                               | none                                                                                       |         | `tidal=yes` marks an area in the tidal range, not access. `access:tide` has 67 uses and no wiki page.                                       |
| `seasonal_operation`                                         | `opening_hours=*` with months, `seasonal=*`                                                | related | Key:seasonal is de facto and points amenities to opening_hours.                                                                             |
| `water_notices`                                              | none                                                                                       |         | Key:drinking_water:legal says tagging "boil before drinking" is not defined.                                                                |
| `flood_depth_marker`                                         | none                                                                                       |         | No documented tag for a depth marker post. `ford=yes` (de facto) and `flood_prone=yes` (in use) describe the crossing.                      |
| `location_sensitivity`                                       | none                                                                                       |         | No documented tag. OTWD publishes only the generalised location.                                                                            |
| Ferry terminal                                               | `amenity=ferry_terminal`                                                                   | exact   | A site with the `ferry_terminal` site type.                                                                                                 |
| `vehicle_limits.max_length_m` and the like                   | `maxlength=*`, `maxheight=*`, `maxweight=*` on the ferry route                             | related | Per-class limits and vehicle bands have no OSM equivalent.                                                                                  |

## Changing a mapping

Mappings belong to the governed list. A change to a mapping is proposed the same way as a new site type or facility, as described in CONTRIBUTING.md, and lands in the governed list file with this page regenerated in the same change.

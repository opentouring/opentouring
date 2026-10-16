<!-- SPDX-License-Identifier: Apache-2.0 -->

# Mapping to OpenStreetMap tags

This page maps OTWD site types and facilities to the closest OpenStreetMap (OSM) tagging. The same mappings are published in machine-readable form in the `osm` field of each entry in `site-types.json` and `facilities.json`, and the tables below are generated from those files.

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

## Facilities

| Code                    | OSM tags                          | Match    | Note                                                                                    |
| ----------------------- | --------------------------------- | -------- | --------------------------------------------------------------------------------------- |
| `toilets`               | `toilets=yes`                     | exact    |                                                                                         |
| `toilets`               | `toilets:disposal=flush`          | related  | Maps the kind attribute value flush.                                                    |
| `toilets`               | `toilets:disposal=pitlatrine`     | related  | Maps the kind attribute value pit. Add composting=yes when the pit toilet composts.     |
| `toilets`               | `toilets:disposal=chemical`       | related  | Maps the kind attribute value chemical.                                                 |
| `toilets`               | `toilets:disposal=dry_toilet`     | related  | Maps the kind attribute value composting where the toilet dehydrates or composts waste. |
| `showers`               | `shower=yes`                      | exact    |                                                                                         |
| `showers`               | `hot_water=yes`                   | narrower | Hot water available. Key:shower treats shower=hot as a tagging mistake.                 |
| `showers`               | `shower:fee=yes`                  | related  | Maps the fee attribute.                                                                 |
| `drinking_water`        | `drinking_water=yes`              | exact    |                                                                                         |
| `non_potable_water`     | `drinking_water=no`               | related  | On the tap or water point, for example man_made=water_tap.                              |
| `power`                 | `power_supply=yes`                | exact    |                                                                                         |
| `dump_point_access`     | `sanitary_dump_station=yes`       | exact    |                                                                                         |
| `dump_point_access`     | `sanitary_dump_station=customers` | narrower | Equivalent to guests_only true.                                                         |
| `bins`                  | `bin=yes`                         | exact    | A bin is available at the camp site or caravan site.                                    |
| `bins`                  | `amenity=waste_basket`            | related  | Small bins, mapped as separate features.                                                |
| `bins`                  | `amenity=waste_disposal`          | related  | Large bins or skips.                                                                    |
| `recycling`             | `amenity=recycling`               | exact    |                                                                                         |
| `bbq`                   | `bbq=yes`                         | exact    |                                                                                         |
| `bbq`                   | `amenity=bbq`                     | related  | A barbecue mapped as a separate feature.                                                |
| `fire_pit`              | `firepit=yes`                     | exact    | Key:fireplace is for chimneys and enclosed fireplaces, not fire pits.                   |
| `fire_pit`              | `leisure=firepit`                 | related  | A fire pit mapped as a separate feature.                                                |
| `fires_allowed`         | `openfire=yes`                    | exact    |                                                                                         |
| `shade`                 | `shade=yes`                       | related  | Marks a feature that is in shade. Used mostly on ways and rare on camp sites.           |
| `picnic_tables`         | `picnic_table=yes`                | exact    | A picnic table is available at the camp site or caravan site.                           |
| `picnic_tables`         | `leisure=picnic_table`            | related  | Tables mapped as separate features.                                                     |
| `playground`            | `leisure=playground`              | related  | Mapped as a separate feature.                                                           |
| `pool`                  | `swimming_pool=yes`               | exact    |                                                                                         |
| `pool`                  | `leisure=swimming_pool`           | related  | A pool mapped as a separate feature.                                                    |
| `laundry`               | `washing_machine=yes`             | exact    |                                                                                         |
| `wifi`                  | `internet_access=wlan`            | exact    |                                                                                         |
| `mobile_coverage`       | none                              |          |                                                                                         |
| `pets_allowed`          | `dog=yes`                         | narrower | Dogs only. dog=leashed when pets.allowed is on_leash.                                   |
| `dog_off_leash`         | `leisure=dog_park`                | related  |                                                                                         |
| `dog_off_leash`         | `dog=unleashed`                   | related  | Dogs may be off the lead. Documented on Key:dog.                                        |
| `accessible_facilities` | `wheelchair=yes`                  | exact    |                                                                                         |
| `generators_allowed`    | none                              |          |                                                                                         |
| `big_rig_access`        | `maxlength=*`                     | related  | Length limits on the access road, not a property of the site.                           |
| `big_rig_access`        | `maxheight=*`                     | related  | Height limits on the access road, not a property of the site.                           |
| `big_rig_access`        | `maxweight=*`                     | related  | Weight limits on the access road, not a property of the site.                           |
| `drive_through_sites`   | none                              |          |                                                                                         |
| `ensuite_sites`         | none                              |          |                                                                                         |
| `cabins`                | `cabins=yes`                      | exact    |                                                                                         |
| `tent_sites`            | `tents=yes`                       | exact    |                                                                                         |
| `camp_kitchen`          | `kitchen=yes`                     | exact    |                                                                                         |

## Changing a mapping

Mappings belong to the governed list. A change to a mapping is proposed the same way as a new site type or facility, as described in CONTRIBUTING.md, and lands in `site-types.json` or `facilities.json` with this page regenerated in the same change.

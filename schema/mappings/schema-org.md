<!-- SPDX-License-Identifier: Apache-2.0 -->

# Mapping to schema.org

This page maps OTWD site types and facilities to schema.org types and properties, for structured data on web pages (JSON-LD) and for search engines. The machine-readable form is the `schema_org` field of each entry in `site-types.json` and `facilities.json`. The tables below are generated from those files.

## Site types

A site type maps to a schema.org type. The Open Touring website marks up each site page with the type of its primary site type, for example `Campground` for a free camp and `RVPark` for a caravan park. Site types with no schema.org equivalent fall back to `Place`.

| Code                     | schema.org                 | Match   | Note                                                                                                                  |
| ------------------------ | -------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------- |
| `free_camp`              | `Campground`               | broader | Add isAccessibleForFree true.                                                                                         |
| `paid_campground`        | `Campground`               | exact   |                                                                                                                       |
| `caravan_park`           | `RVPark`                   | exact   |                                                                                                                       |
| `national_park_campsite` | `Campground`               | broader | Use containedInPlace for the park.                                                                                    |
| `state_forest_campsite`  | `Campground`               | broader |                                                                                                                       |
| `showground`             | `Campground`               | related |                                                                                                                       |
| `rest_area`              | none                       |         |                                                                                                                       |
| `dump_point`             | none                       |         |                                                                                                                       |
| `drinking_water_point`   | none                       |         |                                                                                                                       |
| `public_toilet`          | `PublicToilet`             | exact   |                                                                                                                       |
| `public_shower`          | none                       |         |                                                                                                                       |
| `laundromat`             | `DryCleaningOrLaundry`     | broader |                                                                                                                       |
| `information_centre`     | `TouristInformationCenter` | exact   |                                                                                                                       |
| `attraction`             | `TouristAttraction`        | exact   |                                                                                                                       |
| `lookout`                | `TouristAttraction`        | broader |                                                                                                                       |
| `swimming_spot`          | `Beach`                    | related | Only for beaches. Use PublicSwimmingPool for public pools. schema.org has no general type for natural swimming spots. |
| `boat_ramp`              | none                       |         |                                                                                                                       |
| `fuel`                   | `GasStation`               | exact   |                                                                                                                       |
| `lpg_refill_swap`        | none                       |         |                                                                                                                       |
| `mechanic`               | `AutoRepair`               | exact   |                                                                                                                       |
| `hospital_emergency`     | `Hospital`                 | broader | Hospital is a subtype of EmergencyService. schema.org has no property for an emergency department.                    |
| `ferry_terminal`         | `BoatTerminal`             | exact   |                                                                                                                       |

## Facilities

Most facilities map to the `amenityFeature` property with a `LocationFeatureSpecification` whose `name` is the value shown and whose `value` is the facility's `available` flag. Pets map to the `petsAllowed` property, which `Campground` inherits from `LodgingBusiness`. `RVPark` is not a `LodgingBusiness`, so pets for a caravan park are recorded with `amenityFeature` instead. Facilities marked none are left out of the markup.

| Code                    | schema.org                                 | Match | Note                                                                                                                                                                                                                   |
| ----------------------- | ------------------------------------------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `toilets`               | `amenityFeature` = "Toilets"               | exact |                                                                                                                                                                                                                        |
| `showers`               | `amenityFeature` = "Showers"               | exact |                                                                                                                                                                                                                        |
| `drinking_water`        | `amenityFeature` = "Drinking water"        | exact |                                                                                                                                                                                                                        |
| `non_potable_water`     | none                                       |       |                                                                                                                                                                                                                        |
| `power`                 | `amenityFeature` = "Powered sites"         | exact |                                                                                                                                                                                                                        |
| `dump_point_access`     | `amenityFeature` = "Dump point"            | exact |                                                                                                                                                                                                                        |
| `bins`                  | `amenityFeature` = "Rubbish bins"          | exact |                                                                                                                                                                                                                        |
| `recycling`             | `amenityFeature` = "Recycling"             | exact |                                                                                                                                                                                                                        |
| `bbq`                   | `amenityFeature` = "Barbecue"              | exact |                                                                                                                                                                                                                        |
| `fire_pit`              | `amenityFeature` = "Fire pit"              | exact |                                                                                                                                                                                                                        |
| `fires_allowed`         | none                                       |       |                                                                                                                                                                                                                        |
| `shade`                 | `amenityFeature` = "Shade"                 | exact |                                                                                                                                                                                                                        |
| `picnic_tables`         | `amenityFeature` = "Picnic tables"         | exact |                                                                                                                                                                                                                        |
| `playground`            | `amenityFeature` = "Playground"            | exact |                                                                                                                                                                                                                        |
| `pool`                  | `amenityFeature` = "Swimming pool"         | exact |                                                                                                                                                                                                                        |
| `laundry`               | `amenityFeature` = "Laundry"               | exact |                                                                                                                                                                                                                        |
| `wifi`                  | `amenityFeature` = "Wi-Fi"                 | exact |                                                                                                                                                                                                                        |
| `mobile_coverage`       | none                                       |       |                                                                                                                                                                                                                        |
| `pets_allowed`          | `petsAllowed`                              | exact | petsAllowed is defined for LodgingBusiness (so Campground) and Accommodation, and takes a boolean or text, so species and conditions can go in the text. RVPark is not a LodgingBusiness, so use amenityFeature there. |
| `dog_off_leash`         | `amenityFeature` = "Dog off-leash area"    | exact |                                                                                                                                                                                                                        |
| `accessible_facilities` | `amenityFeature` = "Wheelchair accessible" | exact |                                                                                                                                                                                                                        |
| `generators_allowed`    | `amenityFeature` = "Generators allowed"    | exact |                                                                                                                                                                                                                        |
| `big_rig_access`        | none                                       |       |                                                                                                                                                                                                                        |
| `drive_through_sites`   | `amenityFeature` = "Drive-through sites"   | exact |                                                                                                                                                                                                                        |
| `ensuite_sites`         | `amenityFeature` = "Ensuite sites"         | exact |                                                                                                                                                                                                                        |
| `cabins`                | `amenityFeature` = "Cabins"                | exact |                                                                                                                                                                                                                        |
| `tent_sites`            | `amenityFeature` = "Tent sites"            | exact |                                                                                                                                                                                                                        |
| `camp_kitchen`          | `amenityFeature` = "Camp kitchen"          | exact |                                                                                                                                                                                                                        |

## Other facts

| OTWD fact                                                                                | schema.org                                                                                                                                                                                                                           |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `names` (primary)                                                                        | `name`, other names as `alternateName`                                                                                                                                                                                               |
| `location`                                                                               | `geo` with a `GeoCoordinates` holding `latitude` and `longitude`                                                                                                                                                                     |
| `description`                                                                            | `description`                                                                                                                                                                                                                        |
| `opening_hours`                                                                          | `openingHoursSpecification`, one `OpeningHoursSpecification` per weekly entry, with `validFrom` and `validThrough` for exceptions                                                                                                    |
| `prices`                                                                                 | `priceRange` for a summary. Free sites also get `isAccessibleForFree` true                                                                                                                                                           |
| `bookings.check_in_from`, `bookings.check_out_by`                                        | `checkinTime`, `checkoutTime`                                                                                                                                                                                                        |
| `contact.phone`, `contact.website`                                                       | `telephone`, `url`                                                                                                                                                                                                                   |
| `photos`                                                                                 | `image`, each an `ImageObject` with `license` set to the CC BY 4.0 URL and `creditText` set to the photo's attribution                                                                                                               |
| `accessibility`                                                                          | `amenityFeature` = "Wheelchair accessible", true when the accessible_facilities wheelchair attribute is yes. schema.org has no property for access per feature on a place: `accessibilityFeature` is defined for `CreativeWork` only |
| `permits`                                                                                | `Permit`, with `issuedBy` for the authority and `validIn` for the area. Not a property of a place, so it is described on its own                                                                                                     |
| `seasonal_operation`                                                                     | `openingHoursSpecification` with `validFrom` and `validThrough` for each period                                                                                                                                                      |
| `camping_rules`, `quiet_hours`, `age_rules`, `firewood`, `tidal_access`, `water_notices` | none. `typicalAgeRange` is defined for creative works and events only, and `SpecialAnnouncement` was designed for the coronavirus pandemic and names only civic structures and local businesses as locations                         |
| `derived.locality`, `derived.subdivision_code`, `derived.country_code`                   | `address` with a `PostalAddress` holding `addressLocality`, `addressRegion` and `addressCountry`                                                                                                                                     |

## Example

A caravan park page carries markup like this:

```json
{
  "@context": "https://schema.org",
  "@type": "RVPark",
  "@id": "https://opentouring.org/sites/nt/pandanus-flats-caravan-park-01KR6JW0QBNHM90XV3GS9Y2G26",
  "identifier": "otwd:site:01KR6JW0QBNHM90XV3GS9Y2G26",
  "name": "Pandanus Flats Caravan Park",
  "geo": { "@type": "GeoCoordinates", "latitude": -14.4521, "longitude": 132.2705 },
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Katherine",
    "addressRegion": "AU-NT",
    "addressCountry": "AU"
  },
  "telephone": "+61855501234",
  "checkinTime": "14:00",
  "checkoutTime": "10:00",
  "petsAllowed": true,
  "amenityFeature": [
    { "@type": "LocationFeatureSpecification", "name": "Powered sites", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Dump point", "value": true },
    { "@type": "LocationFeatureSpecification", "name": "Ensuite sites", "value": false }
  ]
}
```

## Record types

Road restrictions and road segments have no schema.org equivalent and are left out of structured data, and so are pet transit rules, bait notices and flood depth markers. A ferry service's `pet_policy` has no schema.org property, because `petsAllowed` is defined for lodging and accommodation only. A ferry service maps to `BoatTrip` (related: a BoatTrip is one sailing, and a ferry service is the crossing it runs on), with `departureBoatTerminal` and `arrivalBoatTerminal` naming the two ferry terminals. Three vehicle classes map to schema.org types: `car` to `Car` (broader), `motorcycle` to `Motorcycle` and `bus` to `BusOrCoach`. Structures, surfaces and vehicle access classes have no schema.org equivalent.

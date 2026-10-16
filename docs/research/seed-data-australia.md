<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Seed data for Australia: open datasets by state and territory

Researched 16 October 2026. Every figure below was read from the publisher's own catalogue entry, API or download on that date. Where a claim could not be confirmed it says "unverified". Dates are the publisher's metadata dates. Note that data.gov.au "last updated" values are harvest dates and can differ from the true data refresh.

Test applied to each dataset: can OTWD redistribute it under CC BY 4.0? Usable means CC BY 3.0 AU, CC BY 4.0, CC0, or explicit permission. ODbL and OpenStreetMap derived data was excluded. This is a licence reading, not legal advice.

## Summary of findings

1. Victoria has the clearest licensing (CC BY 4.0 on every state source found) and the richest per-site detail for camping (fees, access description, campervan class, disability access). Its gap is Parks Victoria national park campgrounds, which have no current open dataset.
2. New South Wales has the most records (719 NPWS camping areas, 869 rest areas, 845 lookouts) but the NPWS licence is "Creative Commons Attribution" with no version stated, and NPWS camping records carry no fees or facility fields.
3. Western Australia has one excellent road dataset (1,677 road stopping places with dump point, toilet and 24 hour stay flags) but no open camping dataset. The DBCA layers are CC BY-NC and unusable.
4. The National Public Toilet Map is the only national source for dump points, drinking water and showers (about 25,600 records), but its terms conflict with its licence field. Treat it as blocked until the Department confirms in writing.
5. The National Formal Rest Areas dataset (5,036 records) has no open licence and says it includes material from parties other than the Commonwealth. Use the state sources instead.
6. No usable open dataset was found for showgrounds, visitor information centres (outside Victoria and Tasmania) or drinking water outside the toilet map. Those need council and tourism outreach.

## Federal and national sources

### National Public Toilet Map

- Publisher: Department of Health, Disability and Ageing
- Catalogue: https://data.gov.au/data/dataset/national-public-toilet-map
- Licence field: cc-by, "Creative Commons Attribution 3.0 Australia" (http://creativecommons.org/licenses/by/3.0/au/)
- Conflict: the dataset description on the same page carries bespoke terms ("the Terms"). They grant a "non-exclusive, perpetual, royalty free, non-transferable and world-wide licence", state "You may not sublicense your rights under these Terms to any person", require copies to be updated "as soon as reasonably practicable" after each release (clause 5.1), say the Commonwealth owns all IPRs in the Database (6.1), and allow termination on breach (8.1). Another person who wants the data "must obtain a copy of the Database from the data.australia.gov.au website" (3.2). That reads as incompatible with republishing the rows under CC BY 4.0.
- Site statement: https://toiletmap.gov.au/copyright says the site material may be reproduced "in unaltered form only" for personal, non-commercial use or use within an organisation, and that the data licence is described on data.gov.au.
- Verdict: licence unclear, flag as restrictive until the Department confirms CC BY applies to the data. Contact on the record: helpline@toiletmap.gov.au.
- Format: CSV (12.1 MB, 25,624 rows read), resource dated 2026-09-30. Published at the start of each month per https://toiletmap.gov.au/copyright.
- Direct file: https://data.gov.au/data/dataset/553b3049-2b8b-46a2-95e6-640d7986a8c1/resource/34076296-6692-4e30-b627-67b7c4eb1027/download/toiletmapexport_261001_074429.csv
- Fields (read from the CSV header): FacilityID, URL, Name, FacilityType, Address1, Town, State, AddressNote, Latitude, Longitude, Parking, ParkingAccessible, ParkingNote, KeyRequired, MLAK24, PaymentRequired, AccessNote, ChangingPlaces, BabyChange, DumpPoint, DPWashout, DPAfterHours, DumpPointNote, OpeningHours, OpeningHoursNote, Male, Female, Unisex, Ambulant, Accessible, ToiletNote, SharpsDisposal, DrinkingWater, SanitaryDisposal, Shower. No rig size limits. Fee is a boolean (PaymentRequired) with no amount.
- Counts per state (my tally of the CSV):

| State | Facilities                    | Dump point = True | Drinking water = True | Shower = True |
| ----- | ----------------------------- | ----------------- | --------------------- | ------------- |
| NSW   | 7,959                         | 347               | 1,070                 | 725           |
| VIC   | 6,090                         | 181               | 651                   | 335           |
| QLD   | 4,784                         | 323               | 694                   | 388           |
| WA    | 2,925                         | 247               | 423                   | 360           |
| SA    | 2,175                         | 201               | 185                   | 132           |
| TAS   | 1,013                         | 81                | 82                    | 53            |
| ACT   | 344                           | 1                 | 38                    | 7             |
| NT    | 332                           | 23                | 59                    | 40            |
| Total | 25,622 (plus 2 with no state) | 1,404             | 3,202                 | 2,040         |

- Related older copies: "DSS - National Public Toilets (Point) 2017" (CC-BY-3.0-AU, https://data.gov.au/data/dataset/au-govt-dss-national-public-toilets-2017-na), "Department of Health - National Toilet Map - June 2018" (CC-BY-3.0-AU, https://data.gov.au/data/dataset/au-govt-doh-national-toilet-map-2018-06-na) and "Public Toilets 2004-2014 for Australia" from the University of Queensland (CC-BY-2.5-AU, https://data.gov.au/data/dataset/uq-erg-public-toilets-na). These are historical snapshots with a clearer licence field but the same underlying records and older data. Whether the bespoke terms still bind them is unverified.

### National Formal Rest Areas (National Freight Data Hub)

- Publisher: Department of Infrastructure, Transport, Regional Development, Communications, Sport and the Arts (National Freight Data)
- Catalogue: https://data.gov.au/data/dataset/national-formal-rest-areas
- Licence field: notspecified. The ArcGIS item (https://spatial.infrastructure.gov.au/portal/sharing/rest/content/items/ef0554e05c37463ba16040a7036b7436) carries only a disclaimer and says the data "includes material provided by parties other than the Commonwealth of Australia".
- Verdict: no licence. Do not use. Use the state inputs in each section below.
- Format: CSV (https://aueprod01ckanstg.blob.core.windows.net/public-catalogue/public/abdbf139-d8dc-41ab-b89a-8a54412d8695/nra.csv) and an ArcGIS FeatureServer. Resource dated 2026-09-27, refreshed quarterly per the item description.
- Records: 5,036 (NSW 855, QLD 1,197, WA 1,650, VIC 651, NT 211, SA 391, TAS 81).
- Fields: state, type, provider_type, name, road_name, locality, direction_of_travel, heavy_vehicle_area, paved, toilet, disabled_toilet, lighting, shelter, water, bin, table_or_chair, bbq, shade, power, latitude, longitude. The columns off_the_road and waste_water are empty in every row.
- Useful as a map of which state sources exist. The per-state input catalogue entries are https://catalogue.data.infrastructure.gov.au/dataset/rest-areas-state-maintained-qld (licence CC BY 3.0 AU), -vic (CC BY 4.0), -nt (licence not specified), -nsw, -sa (CC BY 4.0), -tas (CC BY 3.0 AU) and -wa. The NSW and WA entries show "Creative Commons Attribution 4.1", which is not a real CC version, so treat those two as unclear and use the state portals.

### Other national or cross-state sources checked

- Australian Tourism Data Warehouse (ATDW) API, listed on data.sa.gov.au as https://data.sa.gov.au/data/dataset/australian-tourism-data-warehouse-api: licence "notspecified", last updated 2017-05-29. ATDW is distributed to licensed distributors, not published openly (https://tourism.tas.gov.au/marketing/atdw/ describes the model). Not usable without written permission from the state tourism organisations. This is the main source of visitor information centres and attractions, so it is an outreach item.
- Geoscience Australia topographic data (possible source of campground and lookout points): not examined. Unverified.
- No federal dataset for dump points, drinking water taps or showgrounds was found on data.gov.au (searches "dump point", "drinking water tap", "showground", run 2026-10-16 at https://data.gov.au/data/api/3/action/package_search).

## New South Wales

### NPWS Asset Infrastructure - Visitor Area (camping areas and day use areas)

- Publisher: NSW Department of Climate Change, Energy, the Environment and Water
- URL: https://data.nsw.gov.au/data/dataset/asset-infrastructure-visitor-area
- Licence: cc-by, "Creative Commons Attribution", linked to http://www.opendefinition.org/licenses/cc-by with no version. Usable in principle, but confirm the version with the publisher.
- Format: zipped shapefile (https://datasets.seed.nsw.gov.au/dataset/2d53a537-a6e1-402a-bbf4-7075123e3751/resource/18d89454-3bef-42b1-a269-0b5a95924b75/download/infrastructure_npws_visitorarea.zip). Record verified from the file: VERDATE 20260807, catalogue modified 2026-10-03.
- Records: 1,631, of which 719 are "Camping Area" and 896 "Day Use Area" (16 are cemeteries). Camping area types: Vehicle Based 574 across all subtypes, Remote Walk-in 71, Short Walk-in 38, Boat 33 (counts are by asset type across all subtypes).
- Fields: AssetName, subtype, asset type, NPWS branch, LGA, Comments (populated on 143 camping rows, for example "Vehicle access by permit"), coordinates. No fees, no facilities, no rig limits, no booking flag.

### NPWS Asset Infrastructure - Facility Point

- URL: https://data.nsw.gov.au/data/dataset/asset-infrastructure-facility-point (licence as above, zip at https://datasets.seed.nsw.gov.au/dataset/a60d2562-0c36-4745-9200-bacdefce3acd/resource/9269c237-0754-46dc-b1c8-db43f43a92a6/download/infrastructure_npws_facilitypoint.zip)
- Records: 10,217 points: Picnic Table 3,290, BBQ/Fireplace 2,967, Shelter 1,102, Fee Collection Station - Unmanned 107, and others. Toilets are not among the top subtypes read. A separate toilet layer was not found. Unverified.
- The points have no link to a parent campground, so facilities cannot be attached to a camp without a spatial join.

### NPWS Asset Infrastructure - Lookout

- URL: https://data.nsw.gov.au/data/dataset/asset-infrastructure-lookout (licence as above)
- Records: 845 (Viewing Platform 338, OnGround Lookout 317, ViewPoint 115, Camping Platform 75). Name, subtype, branch, LGA and coordinates only.

### NSW Rest Areas (Transport for NSW)

- URL: https://data.gov.au/data/dataset/nsw-2-nsw-rest-areas, source https://opendata.transport.nsw.gov.au/data/dataset/37a56f96-feb7-49c4-9a7d-06957ccf7368
- Licence: cc-by, "Creative Commons Attribution 3.0 Australia" (http://creativecommons.org/licenses/by/3.0/au/)
- Format: CSV, KML, shapefile, and an API (OpenAPI YAML), plus a temporary closures API. Catalogue modified 2026-06-26 ("14 rest areas were added" in June 2026). Largest row timestamp in the CSV: 2026-08-24.
- Records: 869 (CSV). Site status is blank on 566 rows, Open 299.
- Fields: coordinates, category (Class 4 and 5 heavy vehicle, light vehicle only, service centre, informal), light and heavy parking capacity, toilets (count), disabled_toilet, picnic_table, bbq, playground, shelter, lighting, litter_bins, emergency_phones, driver_reviver, fuel_available, food_available, pets_allowed, boat_ramp. Columns caravan_disposal, water_supply_type, lookout and tourist_information exist but are empty in every row read. No fees.

### NSW sources with no usable licence or no relevant content

- NSW Spatial Services "General Cultural Point" features (https://data.gov.au/data/dataset/nsw-1-a2e7194076d24a4f8b551a9572343359), licence notspecified. Not usable as published.
- City of Sydney drinking fountain and information kiosk datasets (https://data.nsw.gov.au/data/dataset/5-cityofsydney--drinking-fountains-water-bubblers), licence "License Not Specified".
- Forestry Corporation: only the "State Forest" boundary dataset (https://data.nsw.gov.au/data/dataset/state-forest, cc-by). No campground points found.
- Dump points, showgrounds and visitor information centres: no dataset found on data.nsw.gov.au (searches run 2026-10-16).

## Victoria

### Recreation Sites (State Forest)

- Publisher: Department of Energy, Environment and Climate Action
- URL: https://discover.data.vic.gov.au/dataset/recreation-sites
- Licence: cc-by, "Creative Commons Attribution 4.0 International" (https://creativecommons.org/licenses/by/4.0/)
- Format: WFS/GeoJSON (https://opendata.maps.vic.gov.au/geoserver/wfs, layer open-data-platform:recweb_site), shapefile, GDB, DWG via https://datashare.maps.vic.gov.au. Updated daily per the metadata, version date 2026-10-15.
- Records: 532, all published. 360 flag camping, 145 flag campervanning (59 "SMALL CARAVAN", 57 "CAMPER TRAILER").
- Fields (read from the live layer): name, site_class (BASIC 284, MID 142, VERY BASIC 98, HIGH 8), fee (populated on 14 rows only), access_dsc (driving directions and road standard in free text), dis_access (NONE 413, PARTIAL 68, FULLY 5), camping and camping_c (description), camping_r (number of sites), campervan_type, campervan_c, activity flags (fishing, paddling, horse riding and others), bbq counts, maintained_by, photo ids, x_coord and y_coord. This is the best rig suitability signal found in any state dataset, though only as free text and two campervan classes.

### Recreation Assets (State Forest)

- URL: https://discover.data.vic.gov.au/dataset/recreation-assets (CC BY 4.0, daily)
- Records: 3,176. Toilet blocks 298 (UNISEX 260, SEPARATE MALE/FEMALE 32), information shelters 143, picnic shelters 90, viewing platforms 56, "Water Supply" category 53, and "PUMP OUT SEALED UNIT" 251 (this is a toilet system type, not a caravan dump point).
- Linkage to sites is by an is_part_of field. A parent id join was not tested.

### Recreation Carpark (State Forest)

- URL: https://discover.data.vic.gov.au/dataset/recreation-carpark (CC BY 4.0, daily). Record count and fields not read. Unverified.

### Vicmap Features of Interest

- Publisher: Vicmap (Department of Transport and Planning)
- URL: https://discover.data.vic.gov.au/dataset/vicmap-features-of-interest-rest-api
- Licence: cc-by, "Creative Commons Attribution 4.0 International". Weekly update per metadata (catalogue modified 2025-07-10).
- Format: Esri REST FeatureServer https://services-ap1.arcgis.com/P744lA0wf4LlBZ84/arcgis/rest/services/Vicmap_Features_of_Interest/FeatureServer/1 (point layer).
- Counts by feature_subtype read from the live layer: camp ground 1,680, picnic site 835, rest area 575, lookout 495, tourist attraction 464, tourist information centre 148, fire lookout 96, hut 104, day visitor area 401, school camp 23, information bay 12.
- Fields: name, feature_subtype, status, parent name, geometry. No facilities, fees or access. Useful as a name and location seed and for deduplication against the richer sets. No caravan park, dump point or toilet subtype appears in the layer.

### Parks Victoria Camp Grounds and Huts (GovHack 2016)

- URL: https://discover.data.vic.gov.au/dataset/parks-victoria-camp-grounds-and-huts
- Licence field: CC BY 4.0 on the Victorian portal (data.gov.au shows CC BY 3.0 AU). Shapefile and XLSX, resources dated 2019-04-25.
- Caveat in the record: "This data is not official Parks Victoria data and has only been published (temporarily) for the intent of use by Govhack (2016) participants." Treat as an unofficial, ageing snapshot. Record count not read. Unverified.

### Rest areas (Department of Transport and Planning)

- A "Rest Area" dataset is cited as the Victorian input to the national set (https://catalogue.data.infrastructure.gov.au/dataset/rest-areas-state-maintained-vic, licence CC BY 4.0, source https://discover.data.vic.gov.au/dataset/rest-area).
- That source URL returned a redirect loop (HTTP 302 to itself) on 2026-10-16 and the CKAN API returned 404 for ids "rest-area" and "truck-rest-areas". The dataset appears to be withdrawn or moved. Unverified. The national copy shows 651 Victorian rows (CAMPING AREA 27, PICNIC AREA 144, SCENIC LOOKOUT 22, TRUCK PARKING BAY 180) but carries no open licence.

### Councils (examples)

- Many Victorian councils publish toilets, drinking fountains and caravan parks. Licences vary: "other-open" (City of Melbourne, Ballarat, Casey: https://discover.data.vic.gov.au/dataset/public-toilets1), CC BY 2.5 AU (Northern Grampians, Horsham, Hindmarsh, West Wimmera toilets), CC BY 3.0 AU (Greater Geelong caravan parks https://data.gov.au/data/dataset/geelong-caravan-parks, Southern Grampians tourist information centres https://data.gov.au/data/dataset/southern-grampians-tourist-information-centres). "other-open" is not CC BY and needs checking per council. Record counts for these were not read.

## Queensland

### Roadside amenities - Queensland (Transport and Main Roads)

- URL: https://www.data.qld.gov.au/dataset/roadside-amenities-queensland
- Licence: CC-BY-3.0, "Creative Commons Attribution 3.0" (https://creativecommons.org/licenses/by/3.0/au/)
- Content: "the position of roadside amenities, facilities and effluent dump sites in Queensland". Quarterly per metadata, but the record was last modified 2022-10-28. Resource is a spatial data download via QSpatial (http://qldspatial.information.qld.gov.au/catalogue/custom/search.page?q=%22Roadside%20amenities%20-%20Queensland%22), 3 MiB.
- Record count and field list not read (download is behind the QSpatial catalogue). Unverified. The national set holds 1,197 Queensland rows from this family of sources (provider types RA 533, HVSP 331, HV 150, SS 36, UN 32), but that set has no open licence.

### Queensland Picnic and Camping Areas (Points) 2015

- URL: https://data.gov.au/data/dataset/qld-govt-dnrm-qld-recreation-points-picnic-camping-2015-na
- Licence: CC-BY-4.0. Position and names only, from topographic mapping, delivered through the AURIN WFS. Snapshot data, 2015 vintage, count unverified.

### QPWS camping permits

- URL: https://www.data.qld.gov.au/dataset/camping-and-vehicle-permits (CC-BY-4.0, quarterly CSV, latest "July 2026 to September 2026")
- This is permit issue data, not a campground register. A fetch of the CSV was blocked by a Cloudflare challenge, so the columns are unverified. It may help rank popularity but it is not a source of locations.

### Other Queensland findings

- No open QPWS campground point dataset exists on data.qld.gov.au. Searches for "QPWS", "campground", "camping areas" and "protected area facilities" returned only access tracks (https://www.data.qld.gov.au/dataset/queensland-parks-and-wildlife-service-access, CC-BY-4.0), fire layers and permit data.
- SunWater recreation areas (https://www.data.qld.gov.au/dataset/sunwater-recreational-areas, CC-BY-4.0) is only a link to a web page, not updated since 2014.
- Brisbane City Council public toilets (https://www.data.qld.gov.au/dataset/public-toilets-in-brisbane) and park drinking fountain taps (https://data.gov.au/data/dataset/park-drinking-fountain-tap-locations) are CC-BY-4.0 but are HTML link records.
- Gold Coast caravan parks and public toilets (https://data.gov.au/data/dataset/caravan-parks, https://data.gov.au/data/dataset/public-toilets) are CC BY 3.0 AU with GeoJSON and WFS. Counts not read.

## Western Australia

### Road Stopping Places (Main Roads WA)

- URL: https://catalogue.data.wa.gov.au/dataset/mrwa-road-stopping-places
- Licence: cc-by, "Creative Commons Attribution 4.0" on the WA catalogue. The data.gov.au mirror of the sibling datasets says CC BY 3.0 AU (https://data.gov.au/data/dataset/mrwa-major-rest-area). The record includes a required notice: "The Commissioner of Main Roads is the creator and owner of the data and Licenced Material, which is accessed pursuant to a Creative Commons (Attribution) Licence, which has a disclaimer of warranties and limitation of liability."
- Format: ArcGIS REST (https://gisservices.mainroads.wa.gov.au/arcgis/rest/services/OpenData/RoadAssets_DataPortal/MapServer/19), GeoJSON, CSV, KML, shapefile, WFS, WMS. Updated weekly per the record, catalogue modified 2026-10-14.
- Records: 1,677 (Minor Rest Area 1,271, Heavy Vehicle Rest Area 240, Major Rest Area 126, Roadhouse 40).
- Fields: ROAD_NAME, REST_AREA_NAME, REST_AREA_TYPE, STAY_24_HOUR (Yes 44, No 1,631), OWNERSHIP, INFORMATION_BOARD, SCENIC_LOOKOUT (Yes 27), SURFACE_TYPE, SURFACE_AREA, CONSTRUCTED_SHELTER, NATURAL_SHADE, LIGHTING_PRESENT, NUMBER_OF_BINS, NUMBER_OF_TOILETS, ACCESSIBLE_TOILETS, EFFLUENT_DUMP_SITE (Yes 49), NUMBER_OF_TABLES, geometry. No fees (none expected). Surface area and surface type give a partial rig suitability signal.
- Sibling layers with the same licence: Major Rest Area (126), Minor Rest Area (1,271), Heavy Vehicle Rest Area (240) at https://catalogue.data.wa.gov.au/dataset/mrwa-major-rest-area and the matching minor and heavy vehicle records. They are subsets of the layer above.

### WA sources that are not usable or not found

- DBCA (parks agency) layers such as Lands of Interest and Regional Parks carry cc-nc, "Creative Commons Attribution Non-Commercial 4.0" (https://catalogue.data.wa.gov.au/dataset/dbca-lands-of-interest). Not usable.
- No DBCA campground or recreation site point dataset, no visitor centre dataset, and no dump point dataset (apart from the MRWA flag) was found on https://catalogue.data.wa.gov.au (searches "campsite", "DBCA recreation", "visitor centre", "dump point").
- City of Perth toilet accessibility (https://catalogue.data.wa.gov.au/dataset/perth-toilet-accessibility) is CC BY 4.0, city only.

## South Australia

### Rest Areas - State Maintained

- Publisher: Department for Infrastructure and Transport
- URL: https://data.sa.gov.au/data/dataset/rest-areas-state-maintained (also https://data.gov.au/data/dataset/rest-areas-state-maintained)
- Licence: the download includes License.txt: "Creative Commons Attribution 3.0 Australia (CC BY 3.0 AU)". The SA portal field shows "cc-by" without a version.
- Format: GeoJSON, KML, shapefile (https://www.dptiapps.com.au/dataportal/StateMaintainedRestAreas_geojson.zip). Resources dated 2023-07-15, metadata 2018-07-16. Currency is therefore uncertain.
- Records: 391 polygons, all "Operating" (Minor 211, Truck Parking Bays 108, Truck Informal Parking 49, Major 22).
- Fields: restareatype, surface, size, truck parking flag, condition, bins, tables, shelters, toilet blocks (7 sites), water tanks (17 sites), phones (8 sites), comments. No dump point field, no fees.

### SA other

- No national park campground, visitor centre or dump point dataset found on https://data.sa.gov.au (searches "camping", "national park", "caravan", "visitor", "lookout").
- Council toilet and fountain data exists for Adelaide (https://data.sa.gov.au/data/dataset/park-land-toilets, cc-by) and Burnside. Statewide coverage is not available.

## Tasmania

### LIST Points of Interest

- URL: https://data.gov.au/data/dataset/list-points-of-interest, service https://services.thelist.tas.gov.au/arcgis/rest/services/Public/OpenDataWFS/MapServer/36
- Licence: the data.gov.au field is "notspecified", but the service layer copyright text shows the Creative Commons Attribution 3.0 Australia badge with "the LIST (c) State of Tasmania". The service notes a 2,000 feature limit per request.
- Records: 8,032 facility points. Relevant subtypes (COM_TYPE2) read from the layer: Caravan Park 853, Picnic Area 299, Natural 62, Information 18 (includes named visitor centres such as "Tamar Visitor Centre"), Camp and Camping Ground 7. The 853 caravan park count looks high and should be checked against the data before relying on it. Unverified.
- Fields: NAME, COM_TYPE1, COM_TYPE2, PID, coordinates. No facilities or fees.

### Parks and Wildlife Service layers on the LIST

- Campsites (PWS), Toilets and Waste Systems (PWS), Basic Visitor Facilities (PWS) and Recreation Site RSF (PWS): https://data.gov.au/data/dataset/campsites-pws and siblings. Licence notspecified, and each record says "View Dataset (permission required)". Not open. Treat as restricted until Tasmania PWS grants permission.
- The open "Campground" layer in https://services.thelist.tas.gov.au/arcgis/rest/services/Public/PWSPublic/MapServer/20 has 89 points but only NAME, CF_ALLOWED and CF_RULES (campfire rules).
- "Campground/site" (https://data.gov.au/data/dataset/campground-site, licence notspecified, contact listhelp@nre.tas.gov.au) is described as camping and caravan sites and areas, with no download resource listed.

### Roadside Stops (State Owned)

- URL: https://data.gov.au/data/dataset/roadside-stops-state-owned, service https://data.stategrowth.tas.gov.au/ags/rest/services/PUBLIC/ROADSIDESTOPS/MapServer/0
- Licence: notspecified on data.gov.au and the service copyright text is blank. The national input catalogue lists the Tasmanian rest area input as CC BY 3.0 AU (https://catalogue.data.infrastructure.gov.au/dataset/rest-areas-state-maintained-tas). Confirm with the Department of State Growth.
- Records: 81. Fields: SITE_NAME, TYPE, ROAD_NAME, AUTHORITY, CAR_PARK, SHELTER, BBQ, TOILET, RUBBISH_BIN, INFO_SIGN, PICNIC_AREA, PLAY_GROUND, COMMENTS. Temporal coverage 2017.

## Australian Capital Territory

- ACTGOV Public Toilet Assets: https://www.data.act.gov.au/api/views/5ba7-2j7e.json. 229 rows. Fields include cubicle counts, TOILET_ACCESS, WATER_SUPPLY, TOILET_SYSTEM, OPERATIONAL_STATE. Data updated 2026-09-07 per the catalogue search at https://api.us.socrata.com/api/catalog/v1?domains=www.data.act.gov.au.
- ACTGOV Drinking Fountain Assets: https://www.data.act.gov.au/api/views/xfiz-thuk.json. 266 rows. Fields include DOG_BOWL, DISABLED_ACCESS, OPERATIONAL_STATE.
- ACTGOV Park Sign Assets: https://www.data.act.gov.au/api/views/5p4z-aik6.json. 6,982 rows (signs, not a facility register).
- Licence: the dataset-level licence field is empty (null) on all three, and data.gov.au shows "notspecified". The site-wide statement at https://www.act.gov.au/copyright says content is "licensed under a Creative Commons Attribution 4.0 licence" unless stated otherwise, with exceptions for third party material. Whether that statement covers the open data portal is unverified. Ask ACT City Services to confirm.
- No camping, rest area or visitor centre datasets found (searches "camp", "rest area", "caravan", "visitor" on the ACT portal catalogue).

## Northern Territory

- https://data.nt.gov.au holds park boundaries (https://data.nt.gov.au/dataset/natural-resource-maps---nt-parks-and-reserves, cc-by "Creative Commons Attribution" with no version) but no campground, rest area, toilet, dump point or visitor centre points (searches "camping", "rest area", "toilet", "caravan" returned 0 results).
- Rest stops are published as a web page only: https://nt.gov.au/driving/safety/road-rest-stops-in-nt (the licence on the national input record is "not specified": https://catalogue.data.infrastructure.gov.au/dataset/rest-areas-state-maintained-nt). The national set shows 211 NT rows (TRUCK PARKING BAY 149, ROADSIDE STOP 42, REST AREA 20) but that set is unlicensed.
- Parks and Wildlife NT campground data: nothing found. An outreach item.
- Toilet map coverage: 332 facilities, 23 dump points, 59 drinking water, 40 showers (licence caveat above).

## Dataset gaps by category

| Category                               | Open and usable coverage found                                                                                                     | Gap                                                                                                     |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| National park and state forest camping | NSW NPWS (719), VIC state forest (532 sites, 360 camping), VIC Vicmap names (1,680), QLD 2015 points, TAS open campfire layer (89) | QLD QPWS, WA DBCA, SA NPWS, NT PWNT, TAS PWS (permission required), VIC Parks Victoria (national parks) |
| Rest areas (road authorities)          | NSW 869, WA 1,677, SA 391, QLD roadside amenities (count unverified), TAS 81 (licence to confirm)                                  | VIC (dataset withdrawn or moved), NT (web page only)                                                    |
| Dump points                            | WA flag (49), QLD roadside amenities (unverified), toilet map flag (1,404, licence blocked)                                        | Everywhere else. No state publishes a dedicated dump point register                                     |
| Public toilets                         | National Toilet Map (licence blocked), ACT 229, VIC state forest toilet blocks (298), council sets                                 | Clean state-level sets                                                                                  |
| Drinking water                         | Toilet map flag (licence blocked), VIC state forest water supply (53), ACT fountains 266, council fountain sets                    | Rural taps, tank and standpipe locations                                                                |
| Visitor information centres            | VIC Vicmap (148), TAS LIST (18), a few councils                                                                                    | ATDW is closed. NSW, QLD, WA, SA, NT have none open                                                     |
| Showgrounds and council camps          | None found as a dataset. Council caravan park sets exist (Gold Coast, Greater Geelong)                                             | Needs council outreach                                                                                  |
| Attractions and lookouts               | NSW NPWS lookouts (845), VIC Vicmap lookouts (495) and attractions (464), WA lookout flag (27)                                     | Descriptions, access and opening details                                                                |

## Ranking of states by usable coverage

Scores are my judgement from the evidence above. Records counts include only datasets with a usable licence.

| Rank | State | Usable datasets                                                                                                     | Usable records (approx.)                                                 | Licence clarity                                                                                     | Facility detail                                                                                               |
| ---- | ----- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1    | VIC   | 4 clear (Recreation Sites, Recreation Assets, Vicmap FOI, Recreation Carpark) plus 1 caveated (Parks Victoria 2016) | 532 sites, 3,176 assets, about 6,100 FOI points of the relevant subtypes | High: CC BY 4.0 on all four, same licence as OTWD                                                   | High for state forest camping (fee, access text, campervan class, disability access, site count). Low for FOI |
| 2    | NSW   | 4 (NPWS Visitor Area, Facility Point, Lookout, Rest Areas)                                                          | 719 camping, 845 lookouts, 869 rest areas, 10,217 facility points        | Medium: NPWS "Creative Commons Attribution" with no version. Rest areas CC BY 3.0 AU                | Medium for rest areas, low for NPWS camping (no fees or facilities per camp)                                  |
| 3    | WA    | 1 (Road Stopping Places and subsets)                                                                                | 1,677                                                                    | High: CC BY 4.0 (WA catalogue), with a 3.0 AU label on the data.gov.au mirror                       | High for roadside stops (toilets, dump, 24 hour stay, lookout). None for camping                              |
| 4    | QLD   | 2 to 3 (Roadside amenities, 2015 camping points, council sets)                                                      | Unverified for the amenities set                                         | Medium: CC BY 3.0 and 4.0 stated clearly, but the data is old and the download is behind QSpatial   | Low to medium. Dump sites flagged but not counted                                                             |
| 5    | SA    | 1 (Rest Areas)                                                                                                      | 391                                                                      | High: licence file shipped in the download (CC BY 3.0 AU)                                           | Medium (toilets, water tanks, shelters, truck parking). Currency uncertain                                    |
| 6    | TAS   | 1 to 2 (LIST Points of Interest, Roadside Stops if confirmed)                                                       | About 1,200 relevant POI plus 81 stops                                   | Low to medium: layer text says CC BY 3.0 AU, catalogue says notspecified, PWS data needs permission | Low (names only) apart from the 81 roadside stops                                                             |
| 7    | ACT   | 0 confirmed (3 pending licence confirmation)                                                                        | 229 toilets, 266 fountains pending                                       | Low: licence field empty, site-wide CC BY 4.0 statement                                             | Medium for toilets                                                                                            |
| 8    | NT    | 0                                                                                                                   | 0                                                                        | Not applicable                                                                                      | None                                                                                                          |

The National Public Toilet Map would lift every state's dump point, water and shower coverage if the licence is cleared (25,622 records, VIC 6,090, NSW 7,959). It is excluded from the ranking above until it is.

## Recommendation: seed Victoria first

Reasons:

1. Licence match. Every Victorian state dataset used carries "Creative Commons Attribution 4.0 International", the same licence OTWD will publish under. NSW and SA lean on CC BY 3.0 AU or an unversioned CC BY, which needs a licence compatibility check before bulk import.
2. Detail where travellers need it. The Recreation Sites layer holds fee, access directions, site count, campervan class (small caravan or camper trailer) and disability access for 532 state forest sites, with 3,176 related assets including 298 toilet blocks. No other state publishes this much per-site detail openly.
3. Easy ingestion. The sources are WFS or Esri REST services with GeoJSON output, a stable schema and daily or weekly refresh, so the importer can re-run without manual downloads.
4. Cross-reference for deduplication. Vicmap Features of Interest gives 1,680 camp ground names, 575 rest areas, 495 lookouts, 464 attractions and 148 tourist information centres under the same licence, which allows name and location matching against the richer layers.
5. Dense travel corridor. Victoria is the smallest mainland state by area, so 532 sites plus the FOI points give visible coverage quickly, which suits a first launch.

Risks to carry into the Victorian seed:

- The fee field is populated on only 14 of 532 sites. Fees need another source.
- Parks Victoria national park campgrounds, which are the bulk of Victorian camping, are not in the open data. The 2016 GovHack set is unofficial, ageing and labelled as temporary.
- The Department of Transport and Planning rest area dataset is no longer reachable at its cited URL, so Victorian road rest areas rely on the FOI "rest area" points (575, names only).
- Dump points and drinking water have no clean Victorian source until the Toilet Map position is settled.

Suggested second wave: NSW (719 NPWS camping areas and 869 rest areas) once the NPWS licence version is confirmed, and WA road stopping places (1,677, strong dump and toilet flags) as a standalone rest area and dump point layer.

## Gaps that council and tourism outreach would need to fill

1. **National Toilet Map terms.** Ask the Department of Health, Disability and Ageing (helpline@toiletmap.gov.au) for written confirmation that the dataset may be republished under CC BY 4.0 without the non-sublicensable, update and termination terms. This one answer unlocks about 1,400 dump points, 3,200 drinking water points and 2,000 showers.
2. **Parks agencies.** Parks Victoria, QPWS, DBCA (CC BY-NC today), SA NPWS, Tasmania PWS ("permission required") and Parks and Wildlife NT. Ask for a campground register with coordinates, fees, booking requirement, vehicle and rig limits, and facilities under CC BY 4.0.
3. **NPWS NSW.** Confirm the CC BY version and ask for a link between facility points and parent campgrounds and for fee data.
4. **Dump points.** No state publishes a register. Ask councils (many own dump points at caravan parks and rest areas), the Caravan Industry Association and state road authorities. Queensland TMR roadside amenities is the one open source that names dump sites, and its count and age need checking.
5. **Showgrounds and council campgrounds.** No dataset exists. Councils and showground trusts would need to supply listings with fees, power, rig size limits and booking details. Council caravan park sets from Gold Coast and Greater Geelong show the format is feasible.
6. **Visitor information centres and attractions.** ATDW holds the authoritative list but is closed. Ask each state tourism organisation and Tourism Australia for permission to publish centre name, address, coordinates and opening hours under CC BY 4.0. Victoria (148) and Tasmania (18) names exist openly but without hours.
7. **ACT and Tasmania licence statements.** Ask ACT City Services to put a licence on the three asset datasets. Ask Land Tasmania and State Growth to state the licence on the Roadside Stops and PWS layers.
8. **Victorian rest areas.** Ask the Department of Transport and Planning whether the Rest Area dataset is being republished.
9. **NT.** Ask the Department of Infrastructure, Planning and Logistics for the rest stop list in a machine readable form.
10. **Rig limits.** No dataset except WA surface area and Victoria's two campervan classes carries size, height or turning limits. This field would have to be crowdsourced or collected from operators.

## Method notes and unverified items

- Catalogue queries used the CKAN action API on data.gov.au, the Victorian, Queensland, South Australian, Western Australian, NSW and NT portals, the Socrata catalogue for the ACT, and ArcGIS REST endpoints. All were run on 2026-10-16.
- Counts for NPWS, SA, NSW rest areas, WA, Victorian state forest and the toilet map come from files or endpoints I downloaded and read directly. Counts for Vicmap and the Tasmanian LIST layers come from live REST queries.
- Unverified: Queensland roadside amenities record count and fields, Queensland 2015 camping point count, QPWS permit CSV columns, Victorian Recreation Carpark fields, Parks Victoria 2016 record count, Tasmanian "Caravan Park" count, ATDW terms, Geoscience Australia topographic features, council dataset record counts, and whether the NSW Spatial Services FOI layers carry an open licence.
- Licence field disagreements noted: WA road data (CC BY 4.0 on the WA catalogue, 3.0 AU on data.gov.au), Parks Victoria 2016 (4.0 versus 3.0 AU), and the Toilet Map (CC BY 3.0 AU field versus bespoke terms).

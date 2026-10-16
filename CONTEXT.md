<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Open Touring

Open Touring is an open, crowd-contributed database of the places travellers stop at on the road, and of the road restrictions, road segments and ferry services on the way there, published as OTWD under an open data licence. This glossary fixes the words used in the schema, the API, the code and the documentation.

## Language

### The project

**Open Touring**:
The public name of the project, its website and its community.
_Avoid_: OCDB, the app

**OTWD**:
The Open Touring and Waypoint Database: the technical name for the dataset, the API and the SDKs.
_Avoid_: the database (when the dataset is meant), OCDB

**Host**:
The existing not-for-profit organisation that auspices Open Touring and holds its assets for the project under a written agreement.
_Avoid_: owner, sponsor, parent company

**Steering group**:
The group, set up under the host agreement, that governs Open Touring's direction, policies and relicensing votes.
_Avoid_: board, committee

**Sponsor**:
An organisation that funds Open Touring in return for acknowledgement, with no extra rights over the data.
_Avoid_: investor, owner

### Records and what is known about them

**Record**:
One thing OTWD keeps facts about under its own public ID: a site, a road restriction, a road segment or a ferry service.
_Avoid_: entity, object, feature, item

**Record type**:
The kind of record: site, road restriction, road segment or ferry service. Every record type shares public IDs, facts with provenance, closures, merges and submissions.
_Avoid_: entity type, layer, collection

**Site**:
Any place a traveller stops at that OTWD records, such as a campsite, caravan park, rest area, dump point, ferry terminal or attraction. A point record.
_Avoid_: POI, place, listing, location

**Location**:
The latitude and longitude of a site or road restriction, and nothing more.
_Avoid_: address, site (when only the coordinates are meant)

**Geometry**:
The line a road segment or ferry service follows, in WGS84.
_Avoid_: shape, path, polyline, route

**Site type**:
The governed category of a site, such as `free_camp`, `caravan_park`, `rest_area` or `dump_point`. A site has one primary site type and may have more.
_Avoid_: category, kind, tag

**Facility**:
A governed feature a site offers, such as `toilets`, `drinking_water`, `power` or `dump_point_access`, with optional facility attributes.
_Avoid_: amenity, feature, service

**Facility attribute**:
A typed detail of a facility, defined with the facility in the governed list, such as the amperage of `power` or whether `drinking_water` is treated.
_Avoid_: property, option, sub-field

**Governed list**:
A versioned set of allowed codes, such as site types, facilities, structures, surfaces, vehicle access classes, vehicle classes and key schemes, which the community extends by proposal and the steering group approves.
_Avoid_: enum, taxonomy, tag list

**Fact**:
One field value about a record, such as a facility, a price, opening hours, a rig limit or a vertical clearance, carrying its own provenance.
_Avoid_: property, field (when the value is meant)

**Safety fact**:
A fact a traveller relies on for safety: drinking water, road access, rig limits, the site's fire policy and its fire district, a road restriction's location and every limit on it, a road segment's geometry, vehicle access class, towing permitted, seasonal closure and limits, and a ferry service's geometry, terminals, accepted vehicle classes, ferry vehicle limits and seasonal closure. A site's location is not one. Always human-moderated. Declared fire bans and day-to-day road closures are never facts: OTWD links to the authority instead.
_Avoid_: critical field

**Fire district**:
The fire authority and fire district a site falls in, computed from its location against published district boundaries, with a link to the authority's official live fire ban information. A safety fact. OTWD records it so apps can send travellers to current bans, and never stores the bans themselves.
_Avoid_: fire ban, fire danger rating, fire zone

**Rig limit**:
A fact that restricts which vehicles can use a site, such as maximum length, height, weight or a ban on towing. Each is the largest vehicle that fits.
_Avoid_: vehicle restriction, size limit

**Accessibility**:
Access for people with disability at a site or on a ferry service: wheelchair access per feature (yes, limited or no), accessible and ambulant toilets, Changing Places, the key scheme, accessible parking, step-free access, paths and hearing loops, with its accessibility basis. Not a safety fact, but moderators treat a yes with care, because a wrong yes can strand a traveller.
_Avoid_: disability access, wheelchair friendly, accessible (as a yes or no flag)

**Accessibility basis**:
What an accessibility fact rests on: an assessment against a named access standard, signs at the site, the operator's or a seed source's own statement, or a contributor's observation. It sits beside provenance, which says who reported the fact.
_Avoid_: certification, accessibility rating

**Key scheme**:
A central key that opens accessible toilets and other facilities for people with disability, from a governed list with the countries each is used in, such as MLAK in Australia and New Zealand.
_Avoid_: disability key, access key (on its own)

**Description**:
A short original text about a record, written by a contributor and published under the data licence.
_Avoid_: review, blurb

**Photo**:
An image of a record, such as a site or the sign at a road restriction, licensed under the data licence by the person who took it, with its embedded location removed.
_Avoid_: image upload, media

**Public ID**:
The identifier a record keeps for life. It never changes or gets reused, and a merged record's public ID redirects to the surviving record.
_Avoid_: key, slug, row ID

**Closure**:
A record that no longer operates or applies, such as a site that shut or a road restriction whose structure was replaced. It keeps its public ID and history.
_Avoid_: delete, removal

**Temporary closure**:
A record closed for a time, such as a bridge shut after flood damage or a ferry service suspended, with the authority that declared it, a link to its information and, when known, an expected reopening. Short incident closures stay with the authority.
_Avoid_: outage, suspension (as the term)

**Merge**:
Combining duplicate records of one record type, where the losing record's public ID redirects to the surviving one.
_Avoid_: dedupe (as a noun), deletion

### Roads and ferries

**Road restriction**:
A point where a physical or legal limit applies to vehicles, such as a low rail bridge, a bridge with a weight limit or a narrow gate.
_Avoid_: hazard, obstacle, low bridge (as a record type)

**Structure**:
The built thing at a road restriction, from a governed list: bridge, tunnel, overhead structure, causeway or floodway, ford, gate, cattle grid, or no structure when the limit is only signed.
_Avoid_: asset, object, obstruction

**Passage**:
How the road passes a structure: over it (weight and width matter), under it (vertical clearance matters), through it, or along an open road.
_Avoid_: direction, orientation

**Vertical clearance**:
The height a vehicle must be under to pass a road restriction, in metres, as one or more signed, surveyed or measured figures, per direction of travel or lane where they differ. A rig is compared with the lowest figure. A safety fact.
_Avoid_: height limit, headroom, max height (for the clearance at a road restriction)

**Lowest figure**:
The lowest of a vertical clearance's or width limit's figures, whatever its basis. A measured figure below the sign is the one that strikes a vehicle, so every rig filter uses the lowest figure, never the signed figure alone.
_Avoid_: minimum (on its own), effective clearance

**Signed figure**:
A limit as shown on the sign, which is the legal limit.
_Avoid_: posted limit, legal height

**Surveyed figure**:
A limit measured by the road authority or a surveyor, often with a survey certificate.
_Avoid_: physical limit, true clearance

**Measured figure**:
A limit a contributor measured, for example with a tape or a height pole.
_Avoid_: reported limit, user measurement

**Width limit**:
The width a vehicle must be under to pass a road restriction, in metres, recorded like vertical clearance and compared using the lowest figure. A safety fact.
_Avoid_: narrow bridge, max width (for the limit at a road restriction)

**Weight limit**:
The signed gross mass and axle load a vehicle may have, in tonnes, at a road restriction or along a whole road segment. A safety fact.
_Avoid_: load limit, mass limit, max weight (for a signed limit)

**Length limit**:
The longest vehicle or combination allowed, as signed, in metres, at a road restriction or along a whole road segment. A safety fact.
_Avoid_: max length (for a signed limit), rig limit (the term for limits on reaching a site)

**Road segment**:
A stretch of road or track with line geometry, recorded for its surface, vehicle access class, towing and closures.
_Avoid_: road, track, way, link (as the record name)

**Surface**:
What a road segment is made of, from a governed list (sealed, unsealed, gravel, dirt, sand, clay, rock, mud), with how rough it is at the time observed.
_Avoid_: road type, pavement, seal (on its own)

**Vehicle access class**:
The least capable vehicle that can use a road segment, from a ranked governed list: 2WD, AWD, 4WD high clearance, 4WD only, closed to vehicles. A safety fact.
_Avoid_: track grade, difficulty, 4WD rating

**Towing permitted**:
Whether vehicles may tow a trailer or caravan on a road segment: yes, not recommended, or no. A safety fact that comes from contributors, never from a seed source.
_Avoid_: caravan suitable, trailer access

**Seasonal closure**:
The recurring periods a road segment or ferry service closes each year or after rain, with the authority that closes it and a link to its current information. A safety fact. Day-to-day closures stay with the authority.
_Avoid_: road closure (for the recurring rule), wet season closure

**Ferry terminal**:
A site where a ferry loads and unloads, from a ramp on a riverbank to a port terminal.
_Avoid_: wharf, landing, jetty, port (as the site type)

**Ferry service**:
A crossing between two ferry terminals, with line geometry, the vehicle classes it carries, its ferry vehicle limits, fares and hours.
_Avoid_: ferry route, punt, ferry (as the record name)

**Operator**:
The organisation that runs a site or a ferry service, whose public contact details OTWD records.
_Avoid_: owner, provider, company

**Ferry vehicle limits**:
The largest vehicle a ferry service carries, by length, height, width and mass, overall and for each vehicle class. The ferry service's counterpart of a site's rig limits. A safety fact.
_Avoid_: ferry restrictions, vehicle restrictions

**Vehicle class**:
A governed category of traveller a ferry service carries and charges for: foot passenger, bicycle, motorcycle, car, car towing a trailer or caravan, motorhome or campervan, heavy vehicle or bus.
_Avoid_: vehicle type, ticket type

**Vehicle band**:
A range of vehicle lengths or heights, including the drawbar and anything towed, that a ferry fare covers. Whether a vehicle may board at all is decided by the accepted vehicle classes and the ferry vehicle limits, not by a fare's band.
_Avoid_: size class, length category

**Fare**:
The price of one ferry crossing, or a return crossing, for one vehicle class and vehicle band, or one foot passenger.
_Avoid_: ticket price, toll

**Route**:
The path a traveller plans to drive, sent by a partner app to find records along it. OTWD never stores routes.
_Avoid_: trip, itinerary, journey

**Corridor**:
The band either side of a route, of a width the partner app chooses, within which a record counts as along the route.
_Avoid_: buffer, swath

### Provenance and sources

**Provenance**:
Who supplied a fact, through which partner app or seed source, when, and with what confidence.
_Avoid_: source (on its own), metadata, history

**Seed source**:
An external open dataset imported under a compatible licence, such as a state parks dataset, recorded as provenance.
_Avoid_: import, feed, scrape

**Compatible licence**:
A licence on outside data that allows OTWD to republish it under CC BY 4.0.
_Avoid_: open licence (when compatibility has not been checked)

**Mapping**:
A published correspondence between OTWD terms and another vocabulary, such as OpenStreetMap tags or schema.org types.
_Avoid_: crosswalk, conversion

**Derived value**:
A value OTWD computes from a record's location or geometry rather than receives from a contributor: country, subdivision, locality, time zone and, for a line, its length. The fire district is computed from the location too, but it is a fact with provenance, because its boundaries come from a seed source.
_Avoid_: inferred field, calculated location

**Confirmation**:
A later report that an existing fact is still true, recorded as provenance without changing the value.
_Avoid_: re-verification, upvote

### People and applications

**Contributor**:
A person who submits changes, either directly (signed in) or through a partner app (pseudonymous ID).
_Avoid_: user, author, editor

**Direct contributor**:
A contributor who signs in to Open Touring itself and is known by a display name.
_Avoid_: member, account holder

**Pseudonymous ID**:
The stable identifier a partner app sends for one of its contributors, unique per contributor per partner app, carrying no name or email.
_Avoid_: user ID, anonymous ID

**Partner app**:
A third-party application holding an API key that reads OTWD data and may submit changes on behalf of its contributors.
_Avoid_: client, integrator, consumer

**Founding partner**:
The first partner app to read and contribute back to OTWD, on the same terms as any other partner app.
_Avoid_: owner, launch customer

**API key**:
The credential every reader of OTWD holds, free or paid, that binds them to the terms of service and measures their use.
_Avoid_: token, licence key

**Tier**:
A level of API service, from the free tier up to paid tiers that add volume, a service level, change feeds, delta files and support.
_Avoid_: plan, subscription, licence

**Moderator**:
A person who records moderation decisions. Moderators work to one standard for every submission, whichever tier sent it.
_Avoid_: admin, reviewer

**Trust score**:
The measured reliability of a contributor or an API key, used in routing.
_Avoid_: reputation, karma

**Contributor terms**:
The terms every contributor accepts before a submission, granting the host and its successors the rights to publish what they contribute.
_Avoid_: CLA, user agreement

### Submitting and moderating

**Submission**:
A proposed change (new record, edit to facts, photo, closure, merge request) sent by a contributor. It never changes live data directly.
_Avoid_: edit, proposal, PUT

**Submission log**:
The append-only record of every submission and every moderation decision, from which live data is built.
_Avoid_: queue, staging table, edit history

**Fixed checks**:
The deterministic checks every submission passes through before any AI review, such as schema validity, distance to existing records and outlier detection.
_Avoid_: validation (on its own), pre-filter

**Duplicate candidate**:
An existing record of the same record type that a submission may describe, found by distance and name similarity.
_Avoid_: dupe, match

**Verdict**:
The AI's structured recommendation on a submission (category, confidence, reasons, evidence). Not a decision.
_Avoid_: AI decision, score, ruling

**Routing**:
The fixed code that sends each submission to a human queue or, where allowed, to automatic approval, based on its type, its verdict and trust scores.
_Avoid_: triage (by the AI), dispatch

**Always-human list**:
The kinds of submission that routing always sends to a person: new records of every record type, closures, merges and any change to a safety fact. Membership follows from the submission's kind and the safety facts it touches, never from a flag routing sets for itself.
_Avoid_: exceptions, manual list

**Moderation decision**:
The recorded outcome for a submission (approved, rejected, edited and approved, needs info), with who or what decided and why.
_Avoid_: verdict, review, approval (as a noun for the record)

**Amendment**:
A moderator's correction to a submission before approving it, recorded in the moderation decision with the submitted and the applied value. A decision with amendments has the outcome edited and approved.
_Avoid_: edit, override, moderator change

**Appeal**:
A contributor's request for a moderator to reconsider a moderation decision.
_Avoid_: dispute, complaint

**Evaluation set**:
The collection of human moderation decisions used to measure how well verdicts predict them.
_Avoid_: training data, ground truth

### Publishing

**Live data**:
The current state of every record, built from approved changes, which the API and bulk downloads serve.
_Avoid_: production table, master data

**Change**:
An approved submission once applied to the live data, with a sequence number in the change feed.
_Avoid_: update, edit, commit

**Change feed**:
The ordered stream of changes, by sequence number, that partner apps on paid tiers can follow or receive as webhooks.
_Avoid_: changelog, diff stream, firehose

**Full form**:
The representation of a record in which every fact carries its own provenance.
_Avoid_: verbose view, detailed record

**Compact form**:
The representation of a record with plain values plus an attribution list, used by default in the API.
_Avoid_: flat view, summary

**Bulk download**:
A full or delta export of one record type as files (GeoParquet, GeoJSON), with point or line geometry.
_Avoid_: dump, tiles, extract

**Delta file**:
A bulk download holding only the changes between two sequence numbers.
_Avoid_: diff, patch

**Preview**:
The public concept build of Open Touring, running on the production stack with seeded data and submissions from maintainers only, before outside contributions open.
_Avoid_: beta, demo, MVP

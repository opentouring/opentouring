<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Open Touring

Open Touring is an open, crowd-contributed database of the places travellers stop at on the road, published as OTWD under an open data licence. This glossary fixes the words used in the schema, the API, the code and the documentation.

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

### Sites and what is known about them

**Site**:
Any place a traveller stops at that OTWD records, such as a campsite, caravan park, rest area, dump point or attraction.
_Avoid_: POI, place, listing, location

**Location**:
The latitude and longitude of a site, and nothing more.
_Avoid_: address, site (when only the coordinates are meant)

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
The versioned set of allowed site types and facilities, which the community extends by proposal and the steering group approves.
_Avoid_: enum, taxonomy, tag list

**Fact**:
One field value about a site, such as a facility, a price, opening hours or a rig limit, carrying its own provenance.
_Avoid_: property, field (when the value is meant)

**Safety fact**:
A fact a traveller relies on for safety: drinking water, road access, height and weight limits, the site's fire policy and its fire district. Always human-moderated. Declared fire bans are never facts: OTWD links to the fire authority instead.
_Avoid_: critical field

**Fire district**:
The fire authority and fire district a site falls in, computed from its location against published district boundaries, with a link to the authority's official live fire ban information. A safety fact. OTWD records it so apps can send travellers to current bans, and never stores the bans themselves.
_Avoid_: fire ban, fire danger rating, fire zone

**Rig limit**:
A fact that restricts which vehicles can use a site, such as maximum length, height, weight or a ban on towing.
_Avoid_: vehicle restriction, size limit

**Description**:
A short original text about a site, written by a contributor and published under the data licence.
_Avoid_: review, blurb

**Photo**:
An image of a site, licensed under the data licence by the person who took it, with its embedded location removed.
_Avoid_: image upload, media

**Public ID**:
The identifier a site keeps for life. It never changes or gets reused, and a merged site's public ID redirects to the surviving site.
_Avoid_: key, slug, row ID

**Closure**:
A site that no longer operates. It keeps its public ID and history.
_Avoid_: delete, removal

**Merge**:
Combining duplicate sites, where the losing site's public ID redirects to the surviving one.
_Avoid_: dedupe (as a noun), deletion

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
A value OTWD computes from a site's location rather than receives from a contributor: country, subdivision, locality and time zone. The fire district is computed from the location too, but it is a fact with provenance, because its boundaries come from a seed source.
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
A proposed change (new site, edit to facts, photo, closure, merge request) sent by a contributor. It never changes live data directly.
_Avoid_: edit, proposal, PUT

**Submission log**:
The append-only record of every submission and every moderation decision, from which live data is built.
_Avoid_: queue, staging table, edit history

**Fixed checks**:
The deterministic checks every submission passes through before any AI review, such as schema validity, distance to existing sites and outlier detection.
_Avoid_: validation (on its own), pre-filter

**Duplicate candidate**:
An existing site that a submission may describe, found by distance and name similarity.
_Avoid_: dupe, match

**Verdict**:
The AI's structured recommendation on a submission (category, confidence, reasons, evidence). Not a decision.
_Avoid_: AI decision, score, ruling

**Routing**:
The fixed code that sends each submission to a human queue or, where allowed, to automatic approval, based on its type, its verdict and trust scores.
_Avoid_: triage (by the AI), dispatch

**Always-human list**:
The kinds of submission that routing always sends to a person: new sites, closures, merges and any change to a safety fact.
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
The current state of every site, built from approved changes, which the API and bulk downloads serve.
_Avoid_: production table, master data

**Change**:
An approved submission once applied to the live data, with a sequence number in the change feed.
_Avoid_: update, edit, commit

**Change feed**:
The ordered stream of changes, by sequence number, that partner apps on paid tiers can follow or receive as webhooks.
_Avoid_: changelog, diff stream, firehose

**Full form**:
The representation of a site in which every fact carries its own provenance.
_Avoid_: verbose view, detailed record

**Compact form**:
The representation of a site with plain values plus an attribution list, used by default in the API.
_Avoid_: flat view, summary

**Bulk download**:
A full or delta export of the dataset as files (GeoParquet, GeoJSON).
_Avoid_: dump, tiles, extract

**Delta file**:
A bulk download holding only the changes between two sequence numbers.
_Avoid_: diff, patch

**Preview**:
The public concept build of Open Touring, running on the production stack with seeded data and submissions from maintainers only, before outside contributions open.
_Avoid_: beta, demo, MVP

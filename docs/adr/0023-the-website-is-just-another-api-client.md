---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# The website is just another API client

The Open Touring website is built with Astro and reads and writes only through the public API, with its own API key, and has no private access to the database. Site pages are rendered on demand on the server and cached at the CDN with stale-while-revalidate, then purged by change events. The map is a MapLibre GL island on a free OSM-based basemap, the developer portal is Starlight with reference pages generated from the OpenAPI spec, and the contribute and moderate pages are signed-in islands.

Any gap the website hits is a gap partner apps would hit too, so it gets fixed in the API.

## Consequences

Moderation tools need API endpoints of their own, restricted to moderators. Site page URLs take the form `/sites/<state>/<slug>-<id>`, where only the public ID is needed to find the site, so a renamed site keeps working links. Site pages carry schema.org `Campground` structured data.

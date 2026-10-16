---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# No map tiles, with point and line geometry

Supersedes [ADR 0007](0007-points-only-no-map-tiles.md). Open Touring provides no map tiles of any kind, vector or raster. Sites and road restrictions are points (a location). Road segments and ferry services are lines (a GeoJSON LineString or MultiLineString in WGS84), because a track's surface or a ferry crossing cannot be told as a point. The API and bulk downloads serve both as plain geometry, and partner apps draw them on their own basemaps.

Tiles would still multiply CDN cost, pull in basemap licensing questions and duplicate work map providers already do well, while every app that would use OTWD already has a map. Lines change none of that.

## Consequences

Bulk downloads hold one record type per file, as GeoParquet and GeoJSON with point or line geometry, and are never called tiles. The API finds records by bounding box, by distance from a point, or along a route whose geometry a partner app sends encoded, with a corridor width either side. OTWD never stores routes. Site outlines remain out of scope.

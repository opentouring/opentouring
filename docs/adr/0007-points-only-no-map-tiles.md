---
status: superseded by ADR 0028
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Points only, no map tiles

OTWD records each site as a single latitude and longitude, and Open Touring provides no map tiles of any kind, vector or raster. Partner apps draw OTWD points on their own basemaps. Tiles would multiply CDN cost, pull in basemap licensing questions and duplicate work map providers already do well, while every app that would use OTWD already has a map.

## Consequences

The website's own map draws OTWD points on a free OSM-based basemap for display only. Site outlines and access tracks are out of scope for version 1. Bulk downloads are point files (GeoParquet, GeoJSON) and are never called tiles.

Superseded by [ADR 0028](0028-no-map-tiles-points-and-lines.md), which keeps the no-tiles rule and adds line geometry for road segments and ferry services.

---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Object storage deferred: a Singapore bucket for infrastructure state only

The platform starts without Linode Object Storage for anything a contributor or partner app touches. Public bulk downloads and photos live in Bunny Storage in Sydney behind Bunny CDN ([ADR 0021](0021-bunny-cdn-and-crowdsec-instead-of-cloudflare.md)), database backups and point-in-time restore come with the managed Postgres service ([ADR 0017](0017-postgres-with-postgis.md)), the cluster holds no data because Argo CD rebuilds it from this repository, and logs sit on a persistent volume with short retention. The one remaining need is OpenTofu state, which must live outside the infrastructure it describes, so it goes in a single Linode Object Storage bucket in Singapore (`sg-sin-2`, an E3 endpoint) with OpenTofu state encryption turned on.

Sydney had no Linode Object Storage endpoint in October 2026 and Melbourne's endpoint was limited availability, while the API, database and Valkey stay in Sydney for latency (28 ms from an Australian client against 178 ms to Singapore, measured 16 October 2026).

## Consequences

E2 and E3 endpoints support neither CORS policies nor custom domains with TLS, so nothing browser-facing ever uses Linode Object Storage. Contributors' photos are uploaded to the API host, never to a presigned storage URL: `POST /v1/photo-uploads` returns an upload URL on the API, which receives the file, checks its size, type and hash and strips EXIF location before writing it to Bunny Storage, so no file reaches storage unchecked. The Singapore bucket holds only encrypted state, never contributor data. Endpoint features are listed at https://techdocs.akamai.com/cloud-computing/docs/endpoint-types.

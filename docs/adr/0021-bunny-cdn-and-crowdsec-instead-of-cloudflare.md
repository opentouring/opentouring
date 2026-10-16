---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Bunny CDN and CrowdSec instead of Cloudflare

Bulk downloads and the website are served through Bunny CDN, and CrowdSec blocks abusive traffic at the gateway. Bunny has Oceania points of presence, simple per-gigabyte pricing and no terms that tie a not-for-profit to one vendor's platform. Cloudflare is used only if it later proves the best option on cost and terms. Fastly's Fast Forward programme for open source is a later option. Whether Bunny Shield (Bunny's web application firewall) is worth its price is still to be checked, and does not change this decision.

## Consequences

Bulk download files and photos are stored in Bunny Storage with a Sydney region, because Linode Object Storage has no Sydney endpoint (Melbourne is by support request and Singapore is the nearest generally available region), and storing next to the CDN keeps egress simple. Bunny Shield Basic, the free level, is enabled. Prices and regions are in `docs/research/platform-costs.md`.

CDN purges are driven by change events. Edge rules and CrowdSec configuration are kept as code with the rest of the infrastructure.

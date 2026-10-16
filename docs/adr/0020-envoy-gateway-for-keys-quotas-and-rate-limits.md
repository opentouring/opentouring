---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Envoy Gateway for keys, quotas and rate limits

API key checks, quotas and rate limits are enforced at the edge of the cluster by Envoy Gateway, configured through the Kubernetes Gateway API, with CrowdSec blocking abusive clients there. Keeping this in the gateway means the API code never handles key enforcement and tiers can change without a deploy.

## Considered options

- **Kong.** Rejected: several of the features this project needs sit in its paid editions, and its configuration model sits beside the Gateway API rather than on it.
- **Traefik.** Rejected for the API edge: its quota and rate-limit support is thinner for per-key tiers.

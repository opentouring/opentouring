---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Valkey for cache and rate limits

Caching and rate-limit counters use Valkey, the BSD-licensed fork of Redis governed by the Linux Foundation. Redis moved to source-available licences in 2024 and added AGPL-3.0 in 2025. Valkey keeps a permissive licence under open governance, speaks the same protocol, and Linode offers it as a managed service (Valkey 8.1 and 9.1 on 16 October 2026), so it can run managed rather than as another service in the cluster.

## Consequences

Any Redis-protocol client works. Features added to Redis after the fork must not be relied on. Managed Valkey is preferred while the project is run by a maintainer and agents. Running it in the cluster stays an option if latency or cost requires it.

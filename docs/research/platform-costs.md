<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Platform costs for the Open Touring concept build

Researched 2026-10-16. Primary sources only. All figures are USD unless stated. No AUD figure was read on any vendor page, so nothing here is converted to AUD. Where a figure was not read from a vendor source, it is marked **unverified**.

## How the figures were read

- Akamai Cloud (Linode) prices come from the public Linode API, which is the vendor's own price source:
  - https://api.linode.com/v4/linode/types
  - https://api.linode.com/v4/lke/types
  - https://api.linode.com/v4/nodebalancers/types
  - https://api.linode.com/v4/volumes/types
  - https://api.linode.com/v4/object-storage/types
  - https://api.linode.com/v4/network-transfer/prices
  - https://api.linode.com/v4/databases/types
  - https://api.linode.com/v4/databases/engines
  - https://api.linode.com/v4/regions
- Each API item has a base `price` and a `region_prices` list. In every response above the only regions with an override are `id-cgk` (Jakarta) and `br-gru` (Sao Paulo). Sydney (`ap-southeast`) has no override, so the base price applies. This is an inference from the absence of an override. The akamai.com pricing page returned HTTP 403 to a scripted fetch and the page that WebFetch could read had no per-product figures, so the Sydney price was not read as a number on a rendered pricing page.
- Bunny figures come from https://bunny.net/pricing/, https://bunny.net/pricing/storage/ and https://bunny.net/shield/ (read as rendered HTML).
- Akamai docs figures come from techdocs.akamai.com pages fetched as Markdown (URLs cited per line).

## 1. LKE in Sydney

| Item                                          | Price                                                                              | Source                                                                                                                                                                                           |
| --------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Control plane, standard (`lke-sa`)            | $0/month                                                                           | https://api.linode.com/v4/lke/types                                                                                                                                                              |
| Control plane, HA (`lke-ha`)                  | $60/month per cluster (base price, no Sydney override). Jakarta $72, Sao Paulo $84 | https://api.linode.com/v4/lke/types, and "starts at $60/month per cluster, depending on region" at https://techdocs.akamai.com/cloud-computing/docs/high-availability-ha-control-plane-on-lke.md |
| Control plane, LKE Enterprise (`lke-e`)       | $300/month (not needed for the concept)                                            | https://api.linode.com/v4/lke/types                                                                                                                                                              |
| Shared CPU 4 GB (`g6-standard-2`, 2 vCPU)     | $24/month, $0.036/hour, 4000 GB transfer                                           | https://api.linode.com/v4/linode/types                                                                                                                                                           |
| Shared CPU 8 GB (`g6-standard-4`, 4 vCPU)     | $48/month, $0.072/hour, 5000 GB transfer                                           | https://api.linode.com/v4/linode/types                                                                                                                                                           |
| Dedicated CPU 4 GB (`g6-dedicated-2`, 2 vCPU) | $36/month, $0.054/hour, 4000 GB transfer                                           | https://api.linode.com/v4/linode/types                                                                                                                                                           |
| Dedicated CPU 8 GB (`g6-dedicated-4`, 4 vCPU) | $72/month, $0.108/hour, 5000 GB transfer                                           | https://api.linode.com/v4/linode/types                                                                                                                                                           |
| NodeBalancer                                  | $10/month, $0.015/hour. No transfer allowance of its own                           | https://api.linode.com/v4/nodebalancers/types, https://techdocs.akamai.com/cloud-computing/docs/network-transfer-usage-and-costs.md                                                              |
| Block storage                                 | $0.10 per GB per month                                                             | https://api.linode.com/v4/volumes/types                                                                                                                                                          |
| Transfer overage                              | $0.005 per GB (base, Sydney has no override). Jakarta $0.015, Sao Paulo $0.007     | https://api.linode.com/v4/network-transfer/prices                                                                                                                                                |

Transfer allowance rules, quoted from https://techdocs.akamai.com/cloud-computing/docs/network-transfer-usage-and-costs.md:

- "Most core data centers have their transfer allowance and usage tracked in a **global network transfer pool**."
- "Outbound transfer sent from Linodes and NodeBalancers to destinations outside of the origin data center (over both IPv6 and IPv4) and within the same data center if a public IPv4 address is used" is metered. All inbound transfer is free.
- Each node adds its plan allowance to the pool. Three shared 4 GB nodes add 12,000 GB. Object Storage adds 1 TB to the global pool.
- Sydney is a core region in the API (`ap-southeast`, capabilities include Kubernetes, NodeBalancers, Block Storage, Managed Databases). Whether Sydney is in the global pool or a region-specific pool was not stated on a page I read, so treat the pooled allowance as **unverified** for Sydney.
- The Akamai docs describe "Newer data centers" with their own pools. The page names Jakarta and Sao Paulo as examples, and the API has price overrides only for those two.

Melbourne (`au-mel`) is also listed with Kubernetes, Managed Databases and Premium Plans. Prices for Melbourne are also the base price per the API.

## 2. Linode managed Postgres

Plan prices (no Sydney override, so base), from https://api.linode.com/v4/databases/types. Monthly price by node count:

| Plan                                           | 1 node | 2 nodes     | 3 nodes |
| ---------------------------------------------- | ------ | ----------- | ------- |
| Shared Nanode 1 GB (`g6-nanode-1`, 9 GB disk)  | $16    | not offered | $37     |
| Shared 2 GB (`g6-standard-1`, 30 GB disk)      | $32    | not offered | $74     |
| Shared 4 GB (`g6-standard-2`, 58 GB disk)      | $63    | not offered | $147    |
| Shared 8 GB (`g6-standard-4`, 130 GB disk)     | $126   | not offered | $294    |
| Dedicated 4 GB (`g6-dedicated-2`, 58 GB disk)  | $68    | $143        | $206    |
| Dedicated 8 GB (`g6-dedicated-4`, 130 GB disk) | $136   | $285        | $410    |

Engines offered by the API: PostgreSQL 15, 16, 17, 18 (https://api.linode.com/v4/databases/engines). Sydney lists "Managed Databases" in its region capabilities (https://api.linode.com/v4/regions).

Docs facts (https://techdocs.akamai.com/cloud-computing/docs/aiven-manage-database.md):

- "Each MySQL and PostgreSQL Managed Database includes daily backups of your data, taken on a 24 hour cadence. Up to 14 days backups are stored for each database cluster."
- A 2 or 3 node cluster is a high availability cluster: "Your data is replicated across every other node in the cluster. If one goes down, any traffic is redirected to the other available nodes."
- Maximum connections for PostgreSQL are 100 per GiB of plan RAM, capped at 2000 (https://techdocs.akamai.com/cloud-computing/docs/database-engines-plans.md).
- The service is "Akamai Managed Databases powered by Aiven" (same page).
- Linode lists PgBouncer connection pools as a feature of the managed database (the engines page links to "manage PgBouncer connection pools").

### Sales pause (resolved: not paused)

**Update 2026-10-16:** Shane checked the Linode Cloud Manager create-cluster screen on 16 October 2026. It offers PostgreSQL v18, v17, v16 and v15, Valkey v9.1 and v8.1, and MySQL v8.4, with Dedicated, Shared and Premium CPU plans. New managed databases can be ordered, so the reported pause does not apply. PostGIS still needs the live test below.

A web search summary of the Linode docs pages for Managed Databases (Guides, Developers, Resources) reported that Akamai "has paused the sale of our Managed Database offering for all customers who do not have an active database deployed" and that existing deployments stay supported "until our next-generation database solution is available". I could not read those pages directly: https://www.linode.com/docs/... returned HTTP 403 to a scripted fetch. The techdocs.akamai.com Managed Database pages I did read (fetched 2026-10-16, last updated September to October 2026) contain no such notice, and akamai.com product pages still market the service. The pause is therefore **unverified and the sources conflict**. The public API still lists the plans, which does not prove a new account can order one.

### PostGIS statement

- The Akamai Postgres page says only: "To learn about extensions, visit Aiven website: Extensions on Aiven for PostgreSQL" and links https://aiven.io/docs/products/postgresql/reference/list-of-extensions (https://techdocs.akamai.com/cloud-computing/docs/aiven-postgresql.md). Akamai itself gives no list and makes no PostGIS statement.
- Aiven's own extension list (https://aiven.io/docs/products/postgresql/reference/list-of-extensions.md) names, under "Geographical features": "postgis. PostGIS geometry and geography spatial types and functions", plus postgis_raster, postgis_topology, postgis_sfcgal, postgis_tiger_geocoder, postgis_legacy, pgrouting and h3_postgis.
- That list describes Aiven's own service. Whether the Akamai-operated clusters expose the same set, and which PostGIS version, is **unverified** until a live test.

### What a live test must confirm

1. A new account can create a PostgreSQL cluster in (confirmed available on 2026-10-16, see above) `ap-southeast` Sydney, on a 2 GB or 4 GB plan.
2. `SELECT * FROM pg_available_extensions WHERE name LIKE 'postgis%';` returns rows.
3. `CREATE EXTENSION postgis;` succeeds as the default admin user, then `SELECT postgis_full_version();` gives the PostGIS, GEOS and PROJ versions. Repeat for `postgis_raster` and `h3_postgis` if the data model needs them.
4. The PostgreSQL major version selected (15 to 18) pairs with a PostGIS build the app supports. Record both.
5. Backups: the daily backup exists and a restore to a new cluster brings PostGIS back (extensions and spatial reference table intact). Check "Newest full backup plus incremental" works with a PostGIS database.
6. Replicas: the plan with 2 nodes (dedicated only) or 3 nodes (shared) fails over, and the standby carries the extension. The docs describe only HA nodes, not separate read replicas. Whether a read replica endpoint exists and whether it can be used for queries is **unverified**.
7. Connectivity: IPv6 hostname from LKE in the same region, access control list entries, PgBouncer pool creation, and the connection cap (100 per GiB RAM).
8. Region stability: confirm the cluster region matches the LKE region for latency and transfer charges ("use the hostname with an IPv6 address to avoid network transfer charges").

### In-cluster alternative

CloudNativePG on LKE with block storage avoids the unknowns above. Cost is the block storage at $0.10 per GB per month plus the node memory it consumes. Block storage in Sydney lists "Block Storage Encryption" and "Block Storage Migrations" as capabilities (https://api.linode.com/v4/regions).

## 3. Object storage near Sydney

Linode Object Storage is **not available in Sydney** in the current docs or API. The Sydney region's capabilities do not include "Object Storage" (https://api.linode.com/v4/regions), and Sydney does not appear in the endpoint table at https://techdocs.akamai.com/cloud-computing/docs/endpoint-types.md.

Nearest entries in that table (endpoint type, hostname):

| Location    | Region     | Endpoint type                                                                  | Hostname                       |
| ----------- | ---------- | ------------------------------------------------------------------------------ | ------------------------------ |
| Melbourne   | `au-mel`   | E2 marked "LA" (limited availability, request access through a support ticket) | `au-mel-1.linodeobjects.com`   |
| Singapore 2 | `sg-sin-2` | E3, generally available                                                        | `sg-sin-1.linodeobjects.com`   |
| Singapore   | `ap-south` | E0 "LA" (legacy)                                                               | `ap-south-1.linodeobjects.com` |
| Jakarta     | `id-cgk`   | E1, generally available                                                        | `id-cgk-1.linodeobjects.com`   |
| Tokyo 3     | `jp-tyo-3` | E3, generally available                                                        | `jp-tyo-1.linodeobjects.com`   |

The page says "Access to endpoints that are in Limited Availability (LA) can be requested through a support ticket", and "All new customers or projects should start with the standard endpoints (E2 or E3)". Melbourne E2 is the closest standard endpoint but needs approval.

Pricing (https://api.linode.com/v4/object-storage/types):

- Object Storage plan: $5/month, with 1000 GB of outbound transfer added to the global pool. The same price applies in Jakarta and Sao Paulo.
- Outbound overage: $0.02 per GB base. Jakarta $0.024, Sao Paulo $0.028.
- Included stored GB at $5 was not read from a vendor page: **unverified**.
- No per-request charges today. The docs say "Per request charges will not appear on monthly invoices any earlier than October 1, 2027" (https://techdocs.akamai.com/cloud-computing/docs/object-storage-pricing.md).
- Outbound from Object Storage is metered even to services in the same data centre (network transfer page above), so pulls by Bunny CDN count against the pool.
- Linode documents using the object storage with the Akamai CDN, not Bunny. Origin-pull from a Linode bucket by Bunny works as an ordinary HTTPS origin. Not tested.

Bunny Storage (https://bunny.net/pricing/storage/):

- Standard tier (HDD): $0.01/GB for a single region, $0.02/GB for two, $0.025/GB for three, and +$0.005/GB per additional region, up to 9 regions.
- Edge tier (SSD): $0.02/GB per region, up to 15 regions.
- "$1 monthly minimum", "Free traffic to Bunny CDN", "No API fees", "Free API egress".
- The region map lists Sydney, Singapore, Tokyo, Hong Kong, Los Angeles and others. Whether Sydney is available on the Standard tier or only the Edge tier is not stated on the page: **unverified**.
- Egress from Bunny Storage to Bunny CDN is free (above). Egress to other destinations (direct downloads) was not priced on the page I read: **unverified**.

## 4. Bunny CDN and Shield

CDN, Standard network (https://bunny.net/pricing/):

- Europe and North America $0.01/GB, South America $0.045/GB, **Asia and Oceania $0.03/GB**, Middle East and Africa $0.06/GB.
- "$1 monthly minimum." No request fees.
- Volume network (10 PoPs, single global rate) is $0.005/GB for the first 500 TB. It has far fewer PoPs, and whether any is in Oceania was not stated: **unverified**.
- Whether Sydney traffic is billed in the "Asia and Oceania" zone was not spelled out on the page. I have assumed so.

Bunny Shield (https://bunny.net/shield/ pricing table, read from rendered HTML):

| Tier       | Price         | Notes from the table                                                                                                                                                                                                      |
| ---------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic      | FREE          | 71 basic WAF rules, 2 rate limit rules, 1 custom access list with 1k entries, 6 curated threat lists, OWASP Top 10 protection "Basic", simple bot mitigation, block page "bunny.net branded", body inspection limit 256KB |
| Advanced   | $9.5/month    | 255 WAF rules, 10 custom WAF rules, 10 rate limit rules, upload scanning 500k scans CSAM and AV                                                                                                                           |
| Business   | $99/month     | 255 WAF rules, 25 custom WAF rules, 25 rate limit rules                                                                                                                                                                   |
| Enterprise | Contact sales |                                                                                                                                                                                                                           |

The docs (https://docs.bunny.net/shield/pricing.md) confirm four tiers (Basic, Advanced, Business, Enterprise). They state Basic "Includes the baseline WAF package, full DDoS protection, basic inspection features, and custom access control list definitions like IP and ASN-based rules" and point to bunny.net/pricing for prices. The HTML table's request-per-month row lists "25M inc. $0.70/million overage", "50M inc. $0.65/million overage" and "250M inc. $0.60/million overage" for three tiers. The text extraction does not show which tier each value belongs to, so the Basic request cap and overage rate are **unverified**. The Shield price table is not in the docs and the pricing overview page does not list Shield.

## 5. Minimum monthly estimate

Assumptions: Sydney `ap-southeast` base prices, 3 shared 4 GB nodes, 50 GB block storage, 100 GB object storage, 200 GB CDN egress, Shield Basic. All figures USD per month.

| Line                                                                                     | Qty    | Unit                                   | Monthly     | Source                                                       |
| ---------------------------------------------------------------------------------------- | ------ | -------------------------------------- | ----------- | ------------------------------------------------------------ |
| LKE standard control plane                                                               | 1      | $0                                     | $0.00       | https://api.linode.com/v4/lke/types                          |
| Shared CPU 4 GB nodes (`g6-standard-2`)                                                  | 3      | $24                                    | $72.00      | https://api.linode.com/v4/linode/types                       |
| NodeBalancer                                                                             | 1      | $10                                    | $10.00      | https://api.linode.com/v4/nodebalancers/types                |
| Block storage 50 GB (CNPG volumes and other PVCs)                                        | 50 GB  | $0.10/GB                               | $5.00       | https://api.linode.com/v4/volumes/types                      |
| Postgres, option B: CloudNativePG, 2 instances in the cluster                            | 2      | uses the nodes and block storage above | $0.00 extra | derived from the lines above, memory fit **unverified**      |
| Object storage, Linode (nearest GA endpoint, Singapore 2 E3, or Melbourne E2 on request) | 1      | $5                                     | $5.00       | https://api.linode.com/v4/object-storage/types               |
| Bunny CDN, Oceania                                                                       | 200 GB | $0.03/GB                               | $6.00       | https://bunny.net/pricing/                                   |
| Bunny Shield Basic                                                                       | 1      | $0                                     | $0.00       | https://bunny.net/shield/                                    |
| Transfer overage                                                                         |        |                                        | $0.00       | allowance pool size for Sydney **unverified**, see section 1 |
| LLM moderation                                                                           |        |                                        | excluded    | no price page read                                           |
| **Total, option B (CNPG)**                                                               |        |                                        | **$98.00**  |                                                              |

Variants, each changing only the lines named:

| Variant                                                                              | Change                                                         | Monthly total                                                                |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Option A: managed Postgres, Dedicated 4 GB, 2 nodes (`g6-dedicated-2`) replaces CNPG | adds $143.00                                                   | $241.00 (subject to the PostGIS test, section 2)                             |
| Option A2: managed Postgres, Shared 2 GB, 3 nodes                                    | adds $74.00                                                    | $172.00 (same caveats)                                                       |
| Option A3: managed Postgres, Nanode 1 GB, 3 nodes                                    | adds $37.00                                                    | $135.00 (same caveats, 1 GB RAM is small for PostGIS, sizing **unverified**) |
| Bunny Storage Standard, 1 region, replaces Linode Object Storage                     | $1.00 for 100 GB (Sydney tier **unverified**) instead of $5.00 | $94.00                                                                       |
| Dedicated CPU 4 GB nodes (`g6-dedicated-2`) instead of shared                        | 3 x $36 = $108.00 instead of $72.00                            | $134.00 (option B)                                                           |
| Shield Advanced instead of Basic                                                     | adds $9.50                                                     | $107.50 (option B)                                                           |

Notes on the arithmetic:

- Total, option B: 0 + 72 + 10 + 5 + 0 + 5 + 6 + 0 = $98. Everything but the transfer pool and CNPG fit rests on a read price.
- Bunny has a $1 monthly minimum for CDN and for Storage. Both are exceeded here by CDN alone, and whether the minimum applies once per account or per product is not stated: **unverified**. It does not change the total above.
- Node memory for the full stack (Spin, Postgres, PgBouncer, Valkey, NATS, Envoy Gateway, Zitadel or Keycloak, Prometheus, Grafana, Loki, Astro, CrowdSec) on 3 x 4 GB is a sizing question, not a price. It was not measured. If it does not fit, 3 x 8 GB shared nodes (`g6-standard-4`) would be $144 instead of $72, which raises option B to $170.
- Backups of nodes (Linode Backups add-on) are $5 per month per 4 GB node per the API (`g6-standard-2` addon `backups`). They are not in the table above because the concept did not ask for them. Three nodes would add $15.
- No AUD figure was read. Convert at the invoice rate when a quote is needed.

## Live PostGIS test on Linode managed Postgres (16 October 2026)

Run on Shane's `shanelord2` Linode account (not FuelOracle's), with Shane's approval, then deleted.

| Step                 | Result                                                                                                                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create               | Cluster 540084, `g6-nanode-1` (1 GB, US$0.024 an hour), `postgresql/18`, `ap-southeast` Sydney, single node, IP allow list. Created 01:55:32 UTC through `POST /v4/databases/postgresql/instances`.     |
| Active               | 02:02:18 UTC (about 7 minutes). Version 18.6. Endpoints: primary on port 20958 and a `primary-connection-pool` on port 20959. Weekly maintenance window. Point-in-time restore available from 02:01:33. |
| DNS                  | The hostname under `g2a.akamaidb.net` took several more minutes to resolve on public DNS after the cluster reported active.                                                                             |
| Extensions available | postgis 3.6.4, postgis_raster, postgis_topology, postgis_sfcgal, postgis_tiger_geocoder, pg_trgm 1.6, unaccent 1.1, pgcrypto 1.4, h3 4.5.0, pgrouting 4.0.1                                             |
| `CREATE EXTENSION`   | postgis, pg_trgm and unaccent all succeeded on the default database (`defaultdb`). `postgis_full_version()`: POSTGIS 3.6.4, PGSQL 180, GEOS 3.14.1, PROJ 9.8.1.                                         |
| Spatial query        | `ST_Distance` between Melbourne and Sydney as geography returned 713,858 m.                                                                                                                             |
| Delete               | `DELETE` returned 200 at 02:03:56 UTC. The instance returned 404 at 02:04:04 and the account listed no databases.                                                                                       |

Conclusion: PostGIS is supported on Linode managed Postgres 18 in Sydney. ADR 0017 is accepted on this basis.

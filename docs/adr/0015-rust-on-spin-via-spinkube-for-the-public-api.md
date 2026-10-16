---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Rust on Spin via SpinKube for the public API

The public query and submit API is written in Rust and runs as WebAssembly on Spin, scheduled by SpinKube inside the project's own Kubernetes cluster. Moderation workers are also Rust, in ordinary containers. Spin apps start in milliseconds and pack densely, so the API can scale to zero and back on a small cluster, and Rust gives memory safety and predictable performance for a service that will be public and long-lived.

## Considered options

- **Akamai Functions.** Rejected for now: limited availability, and no Postgres connection to Linode's managed database yet. SpinKube runs the same Spin apps, so moving later stays possible.
- **TypeScript (Node).** Rejected for the API: TypeScript is used for the website, but the API benefits from Rust's safety and footprint.
- **Python with FastAPI.** Rejected: Python is kept for the data pipelines, where GDAL, Shapely and GeoPandas live, but not for a high-volume public API.

## Consequences

Spin's Postgres and outbound networking support constrains which Rust libraries the API can use. Heavy work (moderation, bulk download builds) stays out of the Spin apps and runs in workers and pipelines.

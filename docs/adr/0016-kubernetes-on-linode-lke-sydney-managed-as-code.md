---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Kubernetes on Linode LKE Sydney, managed as code

Open Touring runs on Linode's managed Kubernetes (LKE) in Sydney. Infrastructure is defined with OpenTofu and deployments with Helm through Argo CD (GitOps). It starts at minimum size (a small cluster, one database plus a replica) and scales out by design. Everything as code means a host can audit the platform and take it over as a repository, and Sydney keeps Australian contributors' data and latency local.

## Consequences

A Kubernetes cluster costs more to run at preview size than a single server, accepted so that the preview is the production design and not a prototype to rewrite. Moving providers is a matter of new OpenTofu modules rather than a re-architecture.

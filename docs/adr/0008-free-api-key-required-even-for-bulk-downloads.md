---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Free API key required, even for bulk downloads

Every read of OTWD needs an API key, including bulk downloads. The free tier costs nothing and contributing is always free. The submissionDecided webhook, which tells a partner app the outcome of its own submissions, belongs to the contribute path and so is free on every tier, while the change feed, its webhook and data webhooks stay on paid tiers. The key is where a reader accepts the terms of service (including the contribute-back obligations that cannot live in the data licence), it gives usage numbers that sponsors and grant bodies ask for, and it lets the operator revoke abusers.

## Considered options

- **Anonymous bulk downloads.** Rejected: the files would be mirrored with no terms accepted and no way to count or contact the people building on the data. The data licence still lets anyone redistribute a file they have downloaded.

## Consequences

Bulk download files are served from the CDN through signed or key-checked URLs. The website uses an API key like any other partner app.

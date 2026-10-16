---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# No anonymous edits, pseudonymous partner IDs

Every submission is tied to a contributor. Partner apps send a stable pseudonymous ID for each of their contributors (unique per contributor per app, with no names or emails), and direct contributors sign in through OIDC with a display name. Anonymous submissions are not accepted. Trust scores, rate limits, appeals and takedowns all need a stable identity to attach to, while holding partner apps' personal data would create privacy obligations the project does not need.

## Consequences

Open Touring cannot contact a contributor who came through a partner app. Requests for more information go back through the partner app, and the API supports that. Trust scores are kept both per contributor and per API key, so a partner app that sends poor data is visible as a whole.

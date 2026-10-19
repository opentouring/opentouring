---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Stable public IDs and provenance on every fact

Every site gets a public ID that never changes or gets reused. A closure keeps its ID and history, and a merge redirects the losing site's ID to the surviving site. Every fact carries its own provenance (who supplied it, through which partner app or seed source, when, and with what confidence), rather than provenance being recorded once per site.

Partner apps store OTWD IDs in their own databases, so an ID that changes or disappears breaks them. Per-fact provenance lets a newer government seed source update opening hours without overwriting a contributor's newer price, lets moderators weigh conflicting facts, and lets attribution be traced fact by fact.

## Consequences

Storage and payloads are larger, and the API offers a compact form without provenance for readers who do not need it. Merges are always human-moderated because they are hard to undo once partner apps have followed the redirect.

Amended by [ADR 0046](0046-live-data-in-a-public-git-repository-per-country.md): provenance stays per fact in the record files, and the read model adds `change_seq` and `confidence` when it loads them.

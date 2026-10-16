---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# The website and developer portal target WCAG 2.2 AA

The Open Touring website and the developer portal meet the Web Content Accessibility Guidelines 2.2 at level AA. WCAG 2.2 is a W3C Recommendation, current version dated 12 December 2024 ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)), with 9 success criteria added since WCAG 2.1 and 4.1.1 Parsing removed ([What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)). WCAG 3.0 is a Working Draft that its own page says should not be cited "as other than a work in progress" ([WCAG 3.0](https://www.w3.org/TR/wcag-3.0/)), so 2.2 is the standard to build to.

Every pull request that touches `web/` runs an automated checker (axe-core, through Playwright, against the built pages) in CI, and a failure blocks the merge. Automated tools find only part of the problems: the W3C says "some accessibility checks just cannot be automated and require manual intervention" ([evaluation tools](https://www.w3.org/WAI/test-evaluate/tools/)). Before each release a person checks the changed pages by keyboard alone, with a screen reader, at 400% zoom and for colour contrast, and records the result in the release notes.

Travellers with disability are among the people OTWD serves, and the structured accessibility facts (ADR 0033) would ring hollow on a website they cannot use. Building to the standard from the first page costs far less than fixing a finished site.

## Considered options

- **WCAG 2.1 AA.** Rejected: 2.2 is the current Recommendation and adds AA criteria (such as 2.4.11 Focus Not Obscured, 2.5.8 Target Size and 3.3.8 Accessible Authentication) that matter on phones, where travellers use the site.
- **Level AAA.** Rejected as a blanket target: the W3C says "it is not recommended that Level AAA conformance be required as a general policy for entire sites" because some content cannot meet every AAA criterion ([Understanding conformance](https://www.w3.org/WAI/WCAG22/Understanding/conformance)). Individual AAA criteria are adopted where they are cheap.
- **Automated checks only.** Rejected for the reason above.

## Consequences

The map is a MapLibre GL island ([ADR 0023](0023-the-website-is-just-another-api-client.md)), and a map cannot be made fully usable by everyone, so every map view has a list of the same records beside it that works without the map. The website publishes an accessibility statement with the target, known gaps and a contact. Partner apps are encouraged to meet the same standard but are not bound by it.

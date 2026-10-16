---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Fire policy, not fire bans

OTWD records a site's standing fire policy (the `fires_allowed` facility) as a safety fact, plus the fire district the site falls in: the fire authority, the district name and a link to the authority's official live fire ban information. The fire district is computed from the location against a seed source's district boundaries. Fire bans declared by fire authorities are never stored. Total fire bans and other declared bans change daily, faster than crowd moderation can follow, and a stale "no ban" could lead a traveller to light a fire on a dangerous day. The fire authority is the only reliable source, so apps link to it.

## Considered options

- **Store declared bans from the authorities' feeds.** Rejected: OTWD would become a second, slower copy of safety information that already has an official source, and every delay or missed update would be dangerous.

## Consequences

Apps that show `fires_allowed` show the fire district's `ban_info_url` beside it. The fire district is a safety fact, so a change to it goes to a moderator like any other safety fact.

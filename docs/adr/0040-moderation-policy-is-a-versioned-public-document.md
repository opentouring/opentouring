---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# The moderation policy is a versioned public document

The rules moderators and routing follow are published as one document, [docs/policies/moderation.md](../policies/moderation.md), changed only by pull request, with steering group approval once a steering group exists (the maintainer until then). The policy carries a version written `routing-<major>.<minor>`, and every moderation decision records the version it was made under in `routing.policy_version`. A change that alters where a submission goes or what outcome it can get is a major version, and wording changes are minor. Routing code ships with the policy version it implements.

Contributors and partner apps need to know how their submissions will be treated before they send them, and an appeal is only fair if the decision can be read against the rules that applied when it was made. The steering group is given moderation policy and appeals by [GOVERNANCE.md](../../GOVERNANCE.md), and a pull request gives that decision an open record. Automatic approval ([ADR 0010](0010-ai-recommends-fixed-code-routes-humans-decide.md)) switches on group by group, and each switch-on is a policy version with its measurements attached, so the evidence for every automatic approval is public.

## Considered options

- **Moderator guidelines kept private.** Rejected: contributors could not tell why a submission was rejected, and vandals learn the rules anyway from the outcomes.
- **Policy in the routing code only.** Rejected: code says what happens, not why, and people who do not read Rust could not take part in changing it.
- **A separate version scheme from the one decisions already record.** Rejected: `routing.policy_version` already exists in `schema/moderation-decision.schema.json`, and the examples use `routing-1.0`, so the policy uses that form.

## Consequences

The first version is `routing-1.0`. A change to the always-human list itself still needs an ADR, because that list follows from the safety fact markers ([ADR 0027](0027-road-restrictions-road-segments-and-ferry-services-as-record-types.md)), and the policy can only add to what goes to a person, never take away. The steps for proposing a change are in [docs/extending.md](../extending.md#changed-moderation-rule), and the "Moderation policy change" issue form starts one.

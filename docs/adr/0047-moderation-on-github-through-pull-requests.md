---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Moderation on GitHub through pull requests

With live data in a public git repository per country ([ADR 0046](0046-live-data-in-a-public-git-repository-per-country.md)), a submission that passes screening is a pull request, and a moderation decision is a review on it. Moderators are organised in GitHub teams, admins are the organisation's owners, and nothing merges to `main` without an approving review, apart from automatic approval once the moderation policy switches it on. The stages in the moderation policy (fixed checks, AI review, routing, decision, apply) and the rule that the AI recommends and fixed code routes ([ADR 0010](0010-ai-recommends-fixed-code-routes-humans-decide.md)) are unchanged. This decision says where each stage happens.

## Decision

**Who opens pull requests.** The Open Touring GitHub App opens a pull request for each screened submission from the website or a partner app. Seed source pipelines open pull requests through the App too. A person with a GitHub account may also open a pull request by hand. A required check confirms their GitHub account is linked to an opentouring.org account that has accepted the contributor terms. If it is not, the App comments with a sign-in link and the check fails until it is. Hand-made pull requests get the same fixed checks, screening and review as the App's.

**Who reviews.** Each state directory has a moderators team named in CODEOWNERS, and a national team owns `interstate/`. A ruleset on `main` requires an approving review from a code owner, squash merges only, linear history and the merge queue. Moderators review under their own GitHub accounts, so their handles appear publicly on every approval. This is an exception to [ADR 0038](0038-contributor-identity-in-published-data.md)'s rule that moderator IDs are never published, accepted because a moderator's approvals do not reveal where they have travelled and moderators agree to it when they join. A private moderator view on opentouring.org that acts through the App may be added later without another ADR.

**What the checks do.** CI on every pull request validates the files against the pinned schema and runs the fixed checks that need only the repository: on-land, inside a supported country, duplicate candidates and outliers. Checks that need private data, such as trust scores and rate limits, run on opentouring.org and report back as a check run. The AI review runs on opentouring.org too, never in an Action, because repository secrets are not available to pull requests from forks and the model must never see a contributor's identity. Its verdict is posted as a pull request comment.

**Routing on GitHub.** Routing still decides which queue a submission goes to. It sets labels on the pull request: `always-human` for anything on the always-human list, `accessibility-raised` and `sensitive-location` when the fixed checks set those flags ([ADR 0045](0045-sensitive-locations-are-published-generalised.md)), and labels for the record type and state. A moderator's queue is a saved search on those labels.

**The decision record.** The squash commit carries the public parts of the moderation decision as trailers:

```
Decision: otwd:decision:01JB...
Outcome: approved
Moderation-policy: routing-3.0
Verdict-model: <model version>
Routing: human
```

The full moderation decision, with the verdict, the reasons and any amendments, is kept by opentouring.org, which records it from GitHub's pull request webhook and sends `submissionDecided` to the partner app. Moderators' private notes stay in opentouring.org's database and are deleted on the privacy policy's schedule. They never go to GitHub.

**Asking for more information.** A moderator who needs more asks on the pull request. The App labels it `info-requested` and relays the question to the contributor, through the partner app or by email for a direct contributor. The answer comes back through opentouring.org and the App posts it on the pull request. The moderation policy sets how long a pull request waits before it is closed.

**Appeals, reverts and takedowns.** An appeal against an approved change is a revert pull request the App opens, and an appeal against a rejection reopens the submission as a new pull request. Both carry the `appeal` label, and a required check blocks approval by the moderator who made the original decision. A revert or takedown a moderator starts ([ADR 0036](0036-record-lifecycle-and-change-origins.md)) is a pull request too, with the change origin in a `Change-origin:` trailer.

**History rewrites.** A takedown for personal information or copyright removes the content in a commit and then rewrites history to remove it from every earlier commit. Only an organisation owner does the rewrite, by hand, outside the agent hooks that block force pushes. GitHub Support is then asked to purge cached views of the old commits. The takedown process says plainly that clones and forks made before the rewrite cannot be recalled. Every other removal is an ordinary commit.

**Seed imports in batches.** A seed source import or refresh is one pull request per seed source per refresh. A moderator approves the batch on the fixed check report and a random sample, with any safety fact flagged in the report. The sample size is a figure in the moderation policy, which needs changing by its own process before the first batch.

**Automatic approval later.** When the moderation policy switches on automatic approval for a group of submissions, the App approves and merges as a ruleset bypass actor and writes `Routing: automatic` in the trailer. It never bypasses review for a pull request labelled `always-human`, `accessibility-raised` or `sensitive-location`, and fixed code, never the model, makes the call.

## Considered options

- **Every moderator works through a private view on opentouring.org from the start.** Not chosen for now: in Preview the maintainer is the only moderator, and GitHub's review interface is enough. The App can take over merging later, which keeps this path open.
- **Run the AI review as a GitHub Action.** Rejected: secrets are not available to pull requests from forks, and running untrusted pull request code with secrets is the main risk with `pull_request_target`.
- **Keep the full moderation decision in the repository.** Rejected: moderators' private notes must be deletable, and anything committed is public for good.

## Consequences

The moderation policy describes where each stage runs and gains the seed batch sample size, the `info-requested` time limit and the appeal check. The website gains contribute and appeal pages that write to opentouring.org, not to GitHub. The moderator endpoints under `/v1/moderation/` lose the queue, claims and decisions, which live on GitHub, and keep the case (found by submission ID or by pull request), an API key's changes, and reverts and takedowns, which now open pull requests. A moderator needs a GitHub account and joins a state team. The always-human list, appeals by a different moderator and the record of every decision all carry over.

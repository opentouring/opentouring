---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# AI recommends, fixed code routes, humans decide

Moderation runs in three stages. Fixed checks run first. An AI model then returns a structured verdict (category, confidence, reasons, evidence), using a small fast model for every submission and a stronger model only for uncertain or high-risk cases. Routing is then decided by fixed code, never by the model. The always-human list (new sites, closures, merges and any change to a safety fact) always goes to a person, and the AI never deletes or merges anything.

At launch every submission is reviewed by a human, with the verdict as a pre-check. Automatic approval switches on for low-risk changes only once enough labelled human decisions exist to measure verdict accuracy against them.

## Consequences

Submissions are passed to the model strictly as data, and the model has no tools that write, so text written to manipulate the model can at worst produce a wrong recommendation. Every moderation decision records who or what made it, the model version and the reasons. Human decisions form the evaluation set. Moderators are the maintainer and agents first, with volunteers drawn from trusted contributors later, and contributors can appeal any decision.

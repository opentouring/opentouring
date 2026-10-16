---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# DCO sign-off instead of a CLA

Code contributions are accepted under the Developer Certificate of Origin: each commit carries a `Signed-off-by` line, and the contribution is licensed under the licence of the directory it lands in. No contributor licence agreement is used. A CLA that assigns or broadly licenses code to the operator would let the operator relicense the AGPL code as proprietary, which is exactly the risk the AGPL is there to prevent, and it puts off contributors.

## Consequences

Nobody, the host included, can relicense the server code without every author's agreement. Data contributions are a separate matter and use the contributor terms (see ADR 0006), because the data licence and the code licences serve different purposes.

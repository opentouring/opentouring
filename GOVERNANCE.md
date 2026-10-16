<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Governance

Open Touring is meant to be owned by its community through a not-for-profit host. This document describes the interim arrangement during the Preview and how the project will move to the host.

## Interim arrangement

Until a host agrees, Open Touring is maintained by Shane Lord as a sole trader under his ABN. Every account the project depends on (the GitHub organisation, domains, cloud and CDN accounts, the AI provider) is created under an Open Touring email address and kept separate from any other business, so that handing the project over is a set of ownership transfers.

The maintainer decides on code, schema and the governed list, records significant decisions as ADRs in [docs/adr/](docs/adr/), and runs moderation of the Preview data. Outside data contributions stay closed during this period.

FuelOracle, a fuel-planning app also built by Shane Lord, is the founding partner app. It uses OTWD as a customer on the same terms as any other partner app and has no ownership of or special rights over Open Touring or its data.

## Planned host

The project will ask an existing Australian not-for-profit to host (auspice) it. OSGeo Oceania is approached first, and a proposal to Linux Australia is prepared in parallel as the realistic default. The arrangement will be set out in a written memorandum of understanding covering:

- the host holding Open Touring's assets (domains, accounts, trade marks, data rights, funds) for the project
- the project's right to transfer those assets to a successor entity, such as an incorporated association formed for Open Touring
- a project steering group and how its members are chosen
- fees payable to the host
- how either party can end the arrangement, and what happens to the assets if it ends

Insurance for publishing contributed content (public liability and media cover) is not expected from the host agreement. Open Touring arranges it itself before outside contributions open.

## Steering group

Once the host agreement is signed, a steering group takes over decisions from the interim maintainer. Its expected responsibilities are the project's direction, the governed list, [moderation policy](docs/policies/moderation.md) and appeals, approval of new moderators, the contributor terms, use of funds and any vote on relicensing the data to another free and open licence. Its membership and procedures will be written down in this document when the host agreement is made.

## Transfer intent

The interim maintainer intends to transfer every Open Touring asset to the host, or to a successor entity the steering group chooses, when the host agreement is signed. The data contributor terms grant rights to the operator and any successor, so contributions made before the transfer remain usable after it.

The transfer hands over the data as well as the accounts. The outgoing operator produces a final export as set out in [the disaster recovery runbook](docs/operations/disaster-recovery.md#host-handover-export) ([ADR 0041](docs/adr/0041-disaster-recovery-and-backups.md)) and hands over:

- the submission log, moderation decisions and live data
- contributor identity links and the sign-in service's data, in a separately encrypted file, because they are personal information the host takes responsibility for under [the privacy policy](docs/policies/privacy-draft.md)
- the photo files
- the backup decryption keys and every other secret needed to run and restore the platform, outside this repository
- control of the domains, the GitHub organisation, the cloud, CDN and storage accounts, the OpenTofu state bucket and the AI provider account

The host confirms it can restore the export in its own accounts before the old accounts are closed.

## Extending the project

Every kind of change, from a governed list code to a new country, follows a checklist in [docs/extending.md](docs/extending.md) that names who approves it and whether it needs an ADR.

## Changing this document

During the interim period the maintainer changes this document by pull request, with the reason recorded in the commit message. After the host agreement, changes need steering group approval.

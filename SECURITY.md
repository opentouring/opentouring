<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Security policy

## Reporting a vulnerability

Email security@opentouring.org with a description of the problem, the steps to reproduce it and the impact you expect. Do not open a public issue for a vulnerability.

You will get an acknowledgement within five business days. The maintainer will confirm the problem, work on a fix and agree a disclosure date with you, normally within 90 days of the report. Reporters are credited in the release notes unless they ask not to be.

## Scope

In scope: the code in this repository, the Open Touring website, the OTWD API, bulk download delivery and the moderation tools.

Also in scope, because they protect contributors and travellers: ways to bypass moderation and write to live data directly, ways to recover the identity behind a pseudonymous ID, location data surviving in published photos, and ways to make the AI review take actions instead of returning a verdict.

Out of scope: reports from automated scanners with no demonstrated impact, denial of service by volume, and social engineering of the maintainer or moderators.

## API keys

An API key is a server-side secret. Keep it on your own servers and never ship it in a mobile app, a browser page, a public repository or a support ticket. A mobile app talks to OTWD with short-lived tokens that your server obtains with its key, and the key itself never reaches the device. Rotate keys from the developer portal whenever someone who held one leaves, and at least once a year. The token flow, rotation and the optional device attestation are part of the API contract (ADR 0039) and are documented in [api/README.md](api/README.md) once released.

**If your key leaks**, rotate it in the developer portal straight away, then email security@opentouring.org with the key's ID (never the key itself), when and where it was exposed, and whether you saw use you did not make. If you find someone else's key, email security@opentouring.org with where you found it and do not use it.

**Revocation.** The maintainer revokes a key that has leaked, that is used to abuse the service, or whose holder breaks the API terms of service. Revocation takes effect at the gateway, and submissions already accepted under the key stay in moderation. The holder is told by the contact on the key, and can appeal by replying.

## Supported versions

During the Preview only the latest commit on `main` and the running Preview environment are supported.

## Wrong data

Incorrect or unsafe data about a site (for example drinking water that is not drinkable, or a wrong vertical clearance) is a data problem, not a vulnerability. Report it through a submission or by email to hello@opentouring.org so it goes through moderation.

## Takedowns

A photo or text that shows a person's face, a readable number plate or private property, or that infringes copyright, is removed through [the takedown process](docs/policies/takedown.md), not as a security report.

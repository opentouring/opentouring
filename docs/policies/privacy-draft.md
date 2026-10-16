<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Privacy policy (draft)

**Draft for legal review, not in force.** This is a plain-English draft of the privacy policy Open Touring intends to publish before outside data contributions open. It has not been reviewed by a lawyer, it is not legal advice, and it binds nobody. It is written for the Privacy Act 1988 (Cth) and the Australian Privacy Principles (APPs), and the questions a lawyer needs to answer are listed at the end.

## Who we are

Open Touring publishes OTWD, an open database of the places travellers stop at on the road. "We" means the operator of Open Touring: currently Shane Lord, trading as a sole trader, and later the not-for-profit host and any successor named in [GOVERNANCE.md](../../GOVERNANCE.md). Contact us about privacy at privacy@opentouring.org.

## The approach

OTWD is a database of places, not of people. We collect the least personal information that lets us moderate contributions, stop abuse, credit contributors and answer appeals, and we publish none of it unless a contributor chooses to be named.

- Published data names the partner app a fact came through and the date it was recorded. It carries no contributor identifier, unless a feature needs one. When it does, the identifier is an opaque ID for that one record, computed with a secret only we hold, so the same contributor's IDs on two records cannot be linked to each other or to the contributor (ADR 0038).
- A display name is published only when a direct contributor turns it on.
- The link between a contributor and their submissions is kept privately, for moderation, trust scores and appeals, and only moderators can follow it.

The OAIC notes that information "may be personal information in one situation, but de-identified information in another", and that "de-identified information may still carry some risk of re-identification" ([De-identification and the Privacy Act](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/handling-personal-information/de-identification-and-the-privacy-act)). We therefore treat pseudonymous IDs and the private identity links as personal information, and protect them as such.

## What we collect

**From partner apps, about their contributors.** Partner apps never send names or email addresses. For each submission a partner app sends:

- a pseudonymous ID, stable for one contributor within that partner app and meaningless outside it
- a record that the contributor accepted the contributor terms (the terms version and when they accepted)
- the submission itself: the facts reported, the record they concern, when the contributor made the submission and observed what they report, an optional note to moderators, and any photo or description

Partner apps hold their API keys on their own servers. When a partner app's mobile app talks to OTWD directly with a short-lived token (ADR 0039), we also receive the device's IP address and, if the app uses it, a device attestation result.

**From direct contributors** who sign in to Open Touring: an email address and sign-in details held by our own sign-in service ([ADR 0022](../adr/0022-self-hosted-oidc-for-direct-contributors.md)), a display name (published only if you turn that on), and the same submission content as above.

**From everyone who uses the website or the API:** IP addresses, request details and the API key used, in server and gateway logs, for security and rate limits.

**In photos.** Photos are of records, not people, but a photo can show a face, a number plate or private property. We remove embedded location data before storing any photo, moderators check every photo before it is published, and anyone can ask for a photo to be taken down ([the takedown process](takedown.md)).

We do not ask for sensitive information, such as health information. We do not collect government identifiers. We do not use personal information for direct marketing or sell it.

## Why we use it

We use personal information to receive and moderate submissions, credit contributors who choose to be named, calculate trust scores, answer appeals and needs-info questions through the partner app, prevent abuse and keep the service secure, and meet legal obligations. These are the purposes we collect it for ([APP 6](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-6-app-6-use-or-disclosure-of-personal-information)).

**AI review.** Every submission is reviewed by an AI model, which returns a recommendation to a human moderator ([ADR 0010](../adr/0010-ai-recommends-fixed-code-routes-humans-decide.md)). We send the model the submission content as data, never the contributor's pseudonymous ID, email or display name. At launch a person decides every submission. If automatic approval of low-risk changes is switched on under [the moderation policy](moderation.md), this policy will describe the kinds of decision made that way. APP 1.7 and 1.8 require that information in an APP privacy policy from 10 December 2026 where a computer program makes, or does a thing substantially and directly related to, a decision that "could reasonably be expected to significantly affect the rights or interests of an individual" ([APP guidelines, chapter 1](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-1-app-1-open-and-transparent-management-of-personal-information)).

## Who we disclose it to

We do not publish or share contributor identities. We share personal information only with:

- the partner app a contributor used, which already knows them, when we send it the outcome of their submission or a moderator's question
- the service providers that run the platform, listed below, under contracts that limit them to providing that service
- anyone the law requires us to disclose it to

## Where it is held

| What                                                            | Provider and region                                                                                                                  | Notes                                                                                                                                                                                         |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Database, submission log, identity links, sign-in service, logs | Linode (Akamai), Sydney ([ADR 0016](../adr/0016-kubernetes-on-linode-lke-sydney-managed-as-code.md))                                 | Includes the managed database's own backups.                                                                                                                                                  |
| Photos and bulk downloads                                       | Bunny Storage, Sydney region, behind Bunny CDN ([ADR 0021](../adr/0021-bunny-cdn-and-crowdsec-instead-of-cloudflare.md))             | Bunny's privacy notice gives its address as BunnyWay d.o.o., Ljubljana, Slovenia ([bunny.net/privacy](https://bunny.net/privacy/)). Published photos are served from CDN locations worldwide. |
| Encrypted off-site backups                                      | Bunny Storage, Sydney region ([ADR 0041](../adr/0041-disaster-recovery-and-backups.md))                                              | Encrypted before upload with keys Bunny does not hold.                                                                                                                                        |
| Infrastructure state                                            | Linode Object Storage, Singapore ([ADR 0029](../adr/0029-object-storage-deferred-singapore-bucket-for-infrastructure-state-only.md)) | Holds no contributor data.                                                                                                                                                                    |
| Submission content for AI review                                | The AI model provider                                                                                                                | Not yet chosen. Named here, with its country, before outside contributions open.                                                                                                              |

APP 1.4(f) and (g) ask a privacy policy to say whether personal information is likely to be disclosed to overseas recipients and, where practicable, the countries they are in ([APP guidelines, chapter 1](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-1-app-1-open-and-transparent-management-of-personal-information)). Under APP 8 an entity that discloses personal information overseas must take reasonable steps to ensure the recipient does not breach the APPs, and is accountable for the recipient's acts under s 16C ([APP guidelines, chapter 8](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-8-app-8-cross-border-disclosure-of-personal-information)). Whether any row above is an overseas disclosure is a question for the legal review.

## How long we keep it

| Information                                                                  | Kept for                                                                                                                                                        |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Server, gateway and error logs, including IP addresses                       | 30 days                                                                                                                                                         |
| Rate limit counters                                                          | Until the limit window ends, at most 24 hours                                                                                                                   |
| A direct contributor's email address and sign-in details                     | Until the account is closed, then deleted within 30 days                                                                                                        |
| Identity links (pseudonymous ID or account to the contributor's submissions) | While the contributor has submissions under moderation or appeal, or until they ask us to erase them. Reviewed for deletion after 5 years without a submission. |
| Notes to moderators and moderators' internal notes                           | 2 years after the moderation decision, then deleted                                                                                                             |
| Consent records (terms version and acceptance time)                          | As long as the contribution they cover is published, because they show the right to publish it                                                                  |
| Submissions and moderation decisions, without identity links                 | For the life of the dataset, because live data is built from them ([ADR 0009](../adr/0009-event-sourced-submissions-never-direct-writes.md))                    |
| Backups                                                                      | As set out in [the disaster recovery runbook](../operations/disaster-recovery.md), at most 90 days                                                              |

When we no longer need personal information we destroy or de-identify it, as APP 11.3 asks ([APP guidelines, chapter 11](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-11-app-11-security-of-personal-information)).

## Security

Identity links and sign-in data are kept apart from live data and encrypted, and only moderators and the maintainer can reach them. Backups are encrypted before they leave the database provider. Access to production is limited to named people and recorded. We report security problems as described in [SECURITY.md](../../SECURITY.md).

If a data breach is likely to result in serious harm, we follow the Notifiable Data Breaches scheme: we assess a suspected breach within 30 calendar days and notify the people affected and the OAIC when the scheme requires it ([about the NDB scheme](https://www.oaic.gov.au/privacy/notifiable-data-breaches/about-the-notifiable-data-breaches-scheme)).

## Access, correction and erasure

You can ask for the personal information we hold about you and ask us to correct it ([APP 12](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-12-app-12-access-to-personal-information), [APP 13](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-13-app-13-correction-of-personal-information)). We aim to answer within 30 calendar days, the period the OAIC's APP 12 guidelines give as the benchmark for a reasonable time.

You can also ask us to erase your personal information. The OAIC notes that the Privacy Act has no general equivalent of the GDPR's right to erasure ([Australian entities and the EU GDPR](https://www.oaic.gov.au/privacy/guidance-and-advice/australian-entities-and-the-eu-general-data-protection-regulation)), but we offer it to everyone. Erasure removes:

- your email address, sign-in details and display name
- the identity links between you and your submissions, so nobody, moderators included, can tell which submissions were yours
- any per-record contributor IDs computed for you, from live data at once and from bulk downloads at their next rebuild
- notes you wrote to moderators
- photos that show you, through [the takedown process](takedown.md)

The facts you contributed stay in OTWD, without anything that identifies you. They are published under CC BY 4.0, a licence that cannot be withdrawn once given, and others may already hold copies ([the contributor terms draft](../contributor-terms-draft.md)). Backups that still hold your information expire on their normal schedule, and a list of erased identifiers (holding no personal information) is applied again to any backup we restore.

**If you contributed through a partner app**, we cannot tell who you are from our own records. Ask the partner app, which sends us your request with your pseudonymous ID. A partner app can also send the request on your behalf to privacy@opentouring.org from the contact address on its API key.

## Complaints

Complain to us first at privacy@opentouring.org. We will acknowledge your complaint within 5 business days and answer within 30 days. If you are not satisfied, you can complain to the Office of the Australian Information Commissioner. The OAIC asks people to complain to the organisation first and considers 30 days a reasonable time for it to respond ([complain to an organisation or agency](https://www.oaic.gov.au/privacy/privacy-complaints/complain-to-an-organisation-or-agency)).

## Contributors outside Australia

OTWD is global, and contributors in other countries may be covered by their own law. For contributors in the European Union, the European Data Protection Board's guidance is that "pseudonymised data, which could be attributed to a natural person by the use of additional information, remains information related to an identifiable natural person, and thus is personal data" ([EDPB Guidelines 01/2025 on pseudonymisation](https://www.edpb.europa.eu/our-work-tools/documents/public-consultations/2025/guidelines-012025-pseudonymisation_en), version for public consultation adopted 16 January 2025). The design above, which keeps identity links private and publishes no linkable identifier, is meant to meet that standard as well as the APPs. Whether the GDPR applies to Open Touring at all is a question for the legal review.

## Changes to this policy

We publish changes to this policy in this repository by pull request, with the date of each version, and tell partner apps before a change takes effect.

## Questions for the legal review

- **Small business exemption.** The OAIC describes a small business as "one with an annual turnover of $3 million or less" and says the Act "provides a mechanism to allow an organisation that is a small business operator to opt in" ([small business](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/organisations/small-business)). Does the interim operator or the host fall under the exemption, and should Open Touring opt in? This draft assumes the APPs are followed either way.
- **Overseas disclosure.** Is storing encrypted backups or photos with Bunny (whose notice gives a Slovenian address) in its Sydney region a disclosure under APP 8? Is sending submission content to an AI provider overseas one, given that it carries no contributor identifier?
- **Automated decisions.** Once automatic approval is on, are its decisions ones that "could reasonably be expected to significantly affect the rights or interests of an individual" under APP 1.7?
- **GDPR.** Does Article 3(2) reach Open Touring through contributors in the EU ([EDPB Guidelines 3/2018 on territorial scope](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-32018-territorial-scope-gdpr-article-3-version_en))? If it does, is an EU representative under Article 27 needed, or does an exemption apply?
- **Statutory tort.** The OAIC states that a statutory tort for serious invasions of privacy commenced on 10 June 2025 ([statutory tort](https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/statutory-tort-for-serious-invasions-of-privacy)). What does it mean for publishing contributed photos, and is the takedown process enough?
- **Minimum age.** Should contributors under a certain age be excluded, or need a parent's consent?
- **Partner app requests.** Is a request relayed by a partner app enough to verify who is asking, and what should the API offer partner apps for access and erasure requests?
- **Retention.** Are the periods above right, in particular 5 years for identity links and 2 years for notes?

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# Takedown process

This process removes published content that should not be there: a photo showing a person's face, a readable number plate or the inside of private property, content that infringes someone's copyright, and personal information in a description or other free text. It covers photos first, because they are the content most likely to show people, and applies the same way to descriptions. Wrong facts are not takedowns: report them with a submission or by email to hello@opentouring.org so they go through moderation.

## Asking for a takedown

Email takedown@opentouring.org. The website will also carry a report link on each photo. Give:

- the public ID of the record, or the photo's page address
- which of the reasons below applies
- for a photo of you or your vehicle or property, enough to show it is you (a description is enough, we do not want identity documents)

Partner apps can pass on a request from their users the same way. Anyone can ask, not only the person shown.

## Faces, number plates and private property

These are handled as privacy requests and need no proof of ownership.

1. We acknowledge the request within 2 business days.
2. A moderator checks it. A photo in which a person can be recognised, a number plate can be read, or the inside of a private home or yard can be seen is taken down unless the person shown asked for it to stay. Where blurring the face or plate leaves a useful photo, the moderator may publish a blurred copy instead, as a new photo with the same author and licence.
3. The takedown is recorded as a change without a submission with the takedown origin (ADR 0036). The record's change sequence number advances, so partner apps following the change feed see the photo go.
4. We aim to finish within 5 business days of the request.

## Copyright

A copyright owner who believes content in OTWD infringes their copyright sends a notice to takedown@opentouring.org with:

- their name and contact details, or those of the person acting for them
- the work they own, and the OTWD content they say copies it
- a statement that they believe in good faith that the use is not authorised by them or by law
- a statement that the information in the notice is accurate and that they own the copyright or act for the owner

The process:

1. We acknowledge the notice within 2 business days and take the content out of publication while it is assessed, if the notice is complete.
2. We tell the contributor through the partner app, or directly if they signed in, and give them 10 business days to reply with a counter-notice saying why the content is theirs to license (for example, they took the photo).
3. A moderator decides. Content that infringes stays down. Content shown to be the contributor's own goes back up, and the notice sender is told why.
4. A contributor with more than one upheld notice has their later submissions checked more closely, and repeated infringement leads to suspension under [the moderation policy](moderation.md#vandalism-and-reverts).

Notices and counter-notices are kept for 2 years. Whether Open Touring can rely on any statutory safe harbour is a question for the legal review (see below), so this process is a voluntary one and does not depend on it.

## What happens to the content

A takedown removes the content from everywhere OTWD serves it:

- **Data repository.** The takedown is a commit on the data repository's `main` that removes the text or the photo reference ([ADR 0047](../adr/0047-moderation-on-github-through-pull-requests.md)). For personal information or copyright, an organisation owner then rewrites the repository's history so the content is gone from every earlier commit, and asks GitHub Support to purge cached views of the old commits. Anyone who cloned or forked the repository before the rewrite still holds a copy, and OTWD cannot recall it. A takedown for any other reason is the commit alone.
- **API and website.** The photo or text leaves the read model when the loader applies the takedown commit, or rebuilds after a history rewrite. Website pages that showed it are purged from the CDN cache by the change event, like any other change ([docs/architecture.md](../architecture.md#the-three-paths)).
- **Photo files.** The file is deleted from Bunny Storage and its URL purged from Bunny CDN. A blurred replacement, if any, gets a new photo ID.
- **Bulk downloads.** The next rebuild of the full download for that record type leaves it out, and the delta file for that range carries the takedown change. Earlier full downloads that held it are deleted from storage once the rebuild is published.
- **Backups.** Backups expire on their normal schedule ([the disaster recovery runbook](../operations/disaster-recovery.md)). The takedown is applied again to any backup that is restored.
- **The submission log.** The original submission stays in the private submission log on opentouring.org, with the photo file and text removed and a note that a takedown removed them, so the history still shows what happened.

Partner apps that keep copies are told through the change feed and the `changeApplied` webhook, and the API terms of service, once written, will require them to act on takedown changes. Copies made by others under CC BY 4.0 before the takedown, clones and forks of the data repository among them, are beyond OTWD's reach. We can tell the person who asked where the content was published, so they can contact those holders.

## Appeals

The contributor and the person who asked can each appeal a takedown decision once, by replying to the decision email. A different moderator decides the appeal, as with any appeal under [the moderation policy](moderation.md#appeals).

## Questions for the legal review

- Does the safe harbour scheme in Part V Division 2AA of the Copyright Act 1968 cover Open Touring or its host? The 2018 amendments extended it to some kinds of organisation, and whether a not-for-profit open data project is one of them needs checking against the Act.
- Are the time limits above reasonable, and what records should be kept of each takedown?
- How should a photo of an identifiable person be handled when the person shown cannot be contacted and nobody has asked for a takedown?

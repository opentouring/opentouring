---
status: accepted
---

<!-- SPDX-License-Identifier: CC-BY-4.0 -->

# UTC for instants, local time and an IANA zone for schedules

OTWD keeps two kinds of time apart. An instant is a moment that happened once: when a fact was recorded, a seed source retrieved, a moderation decision made, a record created or a change applied, and every time in the change feed, webhook payloads and logs. Every instant is an RFC 3339 timestamp in UTC with the `Z` suffix, defined once as `Timestamp` in `schema/common.schema.json` and used by every date-time field in the schemas and the OpenAPI document. Its pattern rejects any other offset, so `2026-09-08T09:10:00+10:00` fails and is sent as `2026-09-08T23:10:00Z`. The database stores instants as `timestamptz` and services log in UTC. Apps show instants in the reader's own time zone.

A local schedule is a rule read on the clock and calendar where the record is: opening and reception hours, check-in and check-out times, generator hours, ferry operating hours, seasonal closures, access periods and fire policy periods. These are local clock times (`LocalTime`), local calendar dates (`LocalDate`) and days of the year (`MonthDay`, `AnnualPeriod`), read in the record's IANA time zone and never converted to UTC. A ferry that leaves at 6:00 am leaves at 6:00 am on the local clock all year, and a UTC value would move it by an hour when daylight saving starts or ends, or put it on the wrong day.

The time zone is a derived value, computed from the record's location or geometry ([ADR 0012](0012-own-versioned-json-schema-with-osm-and-schema-org-mappings.md) set IANA names for it). A point lies in one zone. A line can cross into another, such as a track over the South Australia and Victoria border, where the clocks differ by half an hour. Line records therefore carry two derived values: `time_zone`, the record's default zone (the zone at the start of the line), and `time_zones`, every zone the line passes through in order, starting with `time_zone`. A zone is listed again each time the line returns to it, so a track from South Australia into Victoria and back lists Adelaide, Melbourne, Adelaide, but never twice in a row. A schedule whose times belong to another of those zones names it in its own `time_zone`, overriding the default. `OpeningHours` and `SeasonalClosure` take this override, and so do a ferry service's `Fares`, whose seasons and validity dates would otherwise be read only in the line's start zone: one override field works the same way on every schedule. The validator checks that `time_zones` starts with `time_zone`, never repeats a zone twice in a row, and holds every schedule's `time_zone`.

## Considered options

- **Store schedules in UTC.** Rejected: local schedules follow the local clock, so every UTC value would be wrong for part of the year and would need rewriting at every daylight saving change.
- **Instants with any offset.** Rejected: two equal instants could be written many ways, sorting and comparing them as text would fail, and a reader could mistake the offset for the record's zone.
- **One time zone per line record, as before.** Rejected: a schedule on a line that crosses into another zone would be read on the wrong clock, half an hour or more out.
- **A time zone on each departure terminal, with hours per terminal.** Rejected: ferry terminals are sites that already carry their own zone, and splitting hours per terminal would duplicate most schedules and let the two copies disagree. A schedule given in one named zone is exact, because an app converts it to the other end's clock for any date.
- **Only a list of zones, with no default.** Rejected: a schedule would not say which clock it uses.

## Consequences

Every example timestamp is in UTC, and an invalid example proves an offset fails. A valid road segment example loops from South Australia into Victoria and back, with a seasonal closure read on the Victorian clock. Invalid examples name a schedule zone and a fare zone the line does not pass through, and list one zone twice in a row. Submissions carry no derived values, so the fixed checks compute the zones from the geometry and apply the same schedule rule before moderation. HTTP headers keep their own forms: `Last-Modified` is an HTTP date, which is always GMT, and the webhook signature timestamp is Unix seconds.

#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the OTWD JSON Schema, the governed lists and the examples.

Usage:
    python3 schema/tools/validate.py              # check everything
    python3 schema/tools/validate.py FILE...      # check documents of your own

A document's schema is chosen from its file name suffix: *.site.json is checked
against site.schema.json, *.site-compact.json against site-compact.schema.json,
and so on for every record type, submission, verdict, moderation decision and
change (see DOCUMENT_KINDS).

Translations of the governed lists live at i18n/<language>/<list file>, for
example i18n/de/facilities.json, and are checked against translation.schema.json
and against the reference list wherever they are found: in i18n/, and under
examples/valid/i18n and examples/invalid/i18n.

The script runs three stages:

1. Every *.schema.json file is checked against the JSON Schema 2020-12
   metaschema, the governed lists against vocabulary.schema.json and
   facilities.json against the per-facility schemas in values.schema.json.
   The governed lists are in en-AU, the reference language.
   For each record type in RECORD_TYPES it checks that the full form,
   FactValues, the compact form and the submissions name the same facts with
   the same value shapes and share one set of required facts.
2. Each document is validated against its schema with format checking on
   (date, date-time, uri, email, json-pointer).
3. Rules that JSON Schema cannot express, and that the API also enforces,
   are checked: governed list codes, ISO 3166-2 prefixes, IANA time zones
   (a line's time_zones start with its time_zone, never list one zone twice in a
   row and hold every schedule's own time_zone),
   lowest figures, the always-human list derived from the schema's safety
   fact markers, ferry terminals, translations that name only codes and
   attributes of the reference list from a folder named for their language
   and carry the SPDX header, and a few cross-field rules.

A top-level "$comment" in a document (the SPDX header of the example files)
is removed before validation against the schema.

Open enumerations (x-otwd-known-values) and record types (x-otwd-registry, checked
against record-types.json) are checked strictly, as for a producer: OTWD never
sends a value its schema version does not know. Files under examples/consumer
come from a later minor version: each must pass the plain validator a consumer
would use and fail the strict one on an unknown value (ADR 0035).

Files under examples/valid and i18n must pass. Files under examples/invalid must
fail, and examples/invalid/expected.json names a fragment of the error each one
must produce (keyed by its path below examples/invalid), so an invalid example
cannot pass by failing for the wrong reason.
The exit status is 0 when every expectation holds and 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
import zoneinfo
from dataclasses import dataclass
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, validators
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SCHEMA_DIR = Path(__file__).resolve().parent.parent
EXAMPLES = SCHEMA_DIR / "examples"
BASE = "https://schema.opentouring.org/otwd/v1/"
COMMENT_KEY = "$comment"
SPDX_COMMENT = "SPDX-License-Identifier: Apache-2.0"
SAFETY_MARKER = "x-otwd-safety-fact"
# Open enumerations list the values known at this schema version, and record IDs and record
# types name the registry that holds theirs. Producers (OTWD and the examples) are held to
# them. Consumers are not, so a document from a later minor version still validates.
KNOWN_VALUES = "x-otwd-known-values"
REGISTRY = "x-otwd-registry"
RECORD_TYPE_REGISTRY = "record-types.json"
# Every producer-only error says this, so consumer examples can tell it from other errors.
PRODUCER_ONLY = "producers may not send it"
I18N = "i18n"
REFERENCE_LANGUAGE = "en-AU"
# Fields the API adds to governed list entries when text falls back to another language.
FALLBACK_FIELDS = ("label_lang", "description_lang")

# Formats the schemas rely on. Without the packages in requirements.txt the
# jsonschema library silently skips some of them, so their absence is fatal.
REQUIRED_FORMATS = {"date", "date-time", "uri", "email", "json-pointer"}

# The governed list files, named once each.
SITE_TYPES = "site-types.json"
FACILITIES = "facilities.json"
STRUCTURES = "structures.json"
SURFACES = "surfaces.json"
ACCESS_CLASSES = "vehicle-access-classes.json"
VEHICLE_CLASSES = "vehicle-classes.json"

# Every governed list file, with the name its codes go by in error messages.
GOVERNED_LISTS = {
    SITE_TYPES: "site type",
    FACILITIES: "facility",
    STRUCTURES: "structure",
    SURFACES: "surface",
    ACCESS_CLASSES: "vehicle access class",
    VEHICLE_CLASSES: "vehicle class",
}

# Submission kinds on the always-human list for every record type, besides the
# kinds that create a record (new_<record type>).
ALWAYS_HUMAN_KINDS = {
    "report_closure",
    "request_merge",
    "request_unmerge",
    "request_split",
    "request_replacement",
}
# The top-level fields of a retracted stub: everything else was removed with the record.
STUB_FIELDS = {"schema_version", "id", "status", "created_at", "updated_at", "change_seq"}
STUB_FIELDS_COMPACT = STUB_FIELDS | {"status_reason", "attribution"}


def schema_file(stem: str) -> str:
    return f"{stem}.schema.json"


def list_file(list_name: str) -> str:
    """The governed list file that holds a list, for example vehicle-access-classes.json."""
    return f"{list_name.replace('_', '-')}.json"


def version_tuple(version: str) -> tuple[int, ...]:
    """A dotted version as numbers, so 1.10.0 sorts after 1.9.0."""
    return tuple(int(part) for part in version.split("."))


@dataclass(frozen=True)
class RecordType:
    """One record type. Its schema files, ID definition and creation kind follow from code.

    computed: facts OTWD computes and contributors never submit.
    """

    code: str
    computed: frozenset[str] = frozenset()

    @property
    def stem(self) -> str:
        return self.code.replace("_", "-")

    @property
    def full(self) -> str:
        return schema_file(self.stem)

    @property
    def compact(self) -> str:
        return schema_file(f"{self.stem}-compact")

    @property
    def camel(self) -> str:
        return "".join(part.title() for part in self.code.split("_"))

    @property
    def new_kind(self) -> str:
        return f"new_{self.code}"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_tag(tag: str) -> str:
    """A BCP 47 tag in its canonical case (RFC 5646 section 2.1.1), such as en-US or zh-Hant-TW.

    Tags compare case-insensitively, so two tags are the same language when their canonical
    forms are equal.
    """
    parts = tag.split("-")
    canonical = [parts[0].lower()]
    after_singleton = False
    for part in parts[1:]:
        after_singleton |= len(part) == 1
        if after_singleton:
            canonical.append(part.lower())
        elif len(part) == 2:
            canonical.append(part.upper())
        elif len(part) == 4 and part.isalpha():
            canonical.append(part.title())
        else:
            canonical.append(part.lower())
    return "-".join(canonical)


def record_zones(derived: dict) -> list[str]:
    """The time zones a record lies in: a line's time_zones, or a point's one time_zone."""
    time_zone = derived.get("time_zone")
    return derived.get("time_zones", [time_zone] if time_zone else [])


def load_record_types() -> tuple[RecordType, ...]:
    """The record types in the registry, record-types.json, in its order."""
    entries = load_json(SCHEMA_DIR / RECORD_TYPE_REGISTRY)["entries"]
    return tuple(
        RecordType(entry["code"], frozenset(entry.get("computed_facts", []))) for entry in entries
    )


RECORD_TYPES = load_record_types()
RECORD_TYPE_BY_CODE = {record_type.code: record_type for record_type in RECORD_TYPES}


def without_comment(document: Any) -> Any:
    if isinstance(document, dict):
        return {key: value for key, value in document.items() if key != COMMENT_KEY}
    return document


def pointer(parts: Iterable[Any]) -> str:
    return "/" + "/".join(str(part) for part in parts)


def shorten(message: str, limit: int = 240) -> str:
    """Keep long messages readable: jsonschema repeats the whole instance in some of them."""
    if len(message) <= limit:
        return message
    return message[: limit // 3] + " ... " + message[-(2 * limit) // 3 :]


def describe(error: ValidationError) -> str:
    return f"{pointer(error.absolute_path)}: {error.message}"


def all_errors(errors: Iterable[ValidationError]) -> list[str]:
    """Every error and every nested oneOf/anyOf sub-error, as 'path: message'."""
    messages: list[str] = []
    stack = list(errors)
    while stack:
        error = stack.pop()
        messages.append(describe(error))
        stack.extend(error.context or [])
    return messages


def record_type_of(record_id: str) -> RecordType:
    """The record type named by the kind segment of a public ID, for example road_segment."""
    return RECORD_TYPE_BY_CODE[record_id.split(":")[1]]


def ref_name(schema: dict) -> str | None:
    """The definition a {"$ref": ...} points at, as file#name or #name, or None."""
    ref = schema.get("$ref")
    return ref.replace("#/$defs/", "#") if ref else None


def registry_code(value: str) -> str:
    """The record type a registry-checked value names: a record type code or a record ID."""
    return value.split(":")[1] if value.startswith("otwd:") else value


def producer_keywords() -> dict[str, Callable]:
    """Keywords that hold a producer to the values known at this schema version."""

    def known_values(validator: Any, known: list[str], instance: Any, schema: dict) -> Iterable:
        if isinstance(instance, str) and instance not in known:
            yield ValidationError(
                f"{instance!r} is not a known value of this open enumeration "
                f"({', '.join(known)}): consumers accept it, producers may not send it"
            )

    registered = {record_type.code for record_type in RECORD_TYPES}

    def registry(validator: Any, file_name: str, instance: Any, schema: dict) -> Iterable:
        if isinstance(instance, str) and registry_code(instance) not in registered:
            yield ValidationError(
                f"{registry_code(instance)!r} is not a record type in {file_name}: "
                "consumers skip it, producers may not send it"
            )

    return {KNOWN_VALUES: known_values, REGISTRY: registry}


# The producer validator applies the open enumeration keywords. The consumer validator is the
# plain 2020-12 validator, which ignores them, as any consumer's validator would.
ProducerValidator = validators.extend(Draft202012Validator, producer_keywords())
ConsumerValidator = Draft202012Validator


class Vocab:
    """The governed lists: for each list file, its entries keyed by code."""

    def __init__(self) -> None:
        documents = {name: load_json(SCHEMA_DIR / name) for name in GOVERNED_LISTS}
        self.lists = {
            name: {entry["code"]: entry for entry in document["entries"]}
            for name, document in documents.items()
        }
        self.versions = {name: document["version"] for name, document in documents.items()}
        self.facilities = self.lists[FACILITIES]
        self.stored_elsewhere = {
            code for code, entry in self.facilities.items() if "stored_as" in entry
        }


@dataclass(frozen=True)
class Context:
    """What every check needs: the schemas by file name, the registry and the governed lists.

    safety_fields: for each record type, the pointers of its safety facts and facilities,
    read from the x-otwd-safety-fact markers in its full form.
    sites: site types of the sites known to this run, by public ID, for cross-document checks.
    sites_complete: True when every site a document names must be known (the examples).
    """

    registry: Registry
    schemas: dict[str, dict]
    vocab: Vocab
    safety_fields: dict[str, frozenset[str]]
    sites: dict[str, set[str]]
    sites_complete: bool

    @classmethod
    def load(cls) -> Context:
        schemas: dict[str, dict] = {}
        registry = Registry()
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            schema = load_json(path)
            expected_id = BASE + path.name
            if schema.get("$id") != expected_id:
                raise SystemExit(f"{path.name}: $id must be {expected_id}")
            schemas[path.name] = schema
            resource = Resource.from_contents(schema, default_specification=DRAFT202012)
            registry = registry.with_resource(expected_id, resource)
        safety = {
            record_type.code: frozenset(safety_pointers(schemas[record_type.full]))
            for record_type in RECORD_TYPES
        }
        return cls(registry.crawl(), schemas, Vocab(), safety, {}, False)

    def with_sites(self, paths: Iterable[Path], complete: bool) -> Context:
        sites: dict[str, set[str]] = {}
        for path in paths:
            kind = DocumentKind.for_path(path)
            if kind and kind.stem in ("site", "site-compact"):
                document = load_json(path)
                types = site_types_of(document)
                if types is not None:
                    sites[document["id"]] = types
        return Context(self.registry, self.schemas, self.vocab, self.safety_fields, sites, complete)

    def validator(self, schema_name: str, consumer: bool = False) -> Draft202012Validator:
        cls = ConsumerValidator if consumer else ProducerValidator
        return cls(
            self.schemas[schema_name],
            registry=self.registry,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )

    def definition(self, schema_name: str, def_name: str) -> dict:
        """A named entry in a schema's $defs."""
        return self.schemas[schema_name]["$defs"][def_name]


def safety_pointers(full_schema: dict) -> Iterable[str]:
    """The fields a record type's full form marks as safety facts, as JSON Pointers."""
    sections = {"facts": "Facts", "facilities": "FacilityFacts"}
    for section, def_name in sections.items():
        definition = full_schema["$defs"].get(def_name, {})
        for name, fact in definition.get("properties", {}).items():
            if fact.get(SAFETY_MARKER):
                yield f"/{section}/{name}"


def site_types_of(document: dict) -> set[str] | None:
    """The site types of a site in either form, or None for a merged site."""
    value = document.get("site_types") or document.get("facts", {}).get("site_types", {})
    value = value.get("value", value)
    if "primary" not in value:
        return None
    return {value["primary"], *value.get("others", [])}


class SemanticChecker:
    """Rules JSON Schema cannot express. The API applies the same rules."""

    def __init__(self, context: Context, rejects_deprecated: bool) -> None:
        self.context = context
        self.vocab = context.vocab
        self.rejects_deprecated = rejects_deprecated
        self.errors: list[str] = []
        # One table for every record type and for submissions: fact names do not
        # repeat with different meanings across record types.
        self.fact_checks: dict[str, Callable[[Any, str], None]] = {
            "site_types": self.site_types,
            "description": self.description,
            "opening_hours": self.hours,
            "reception_hours": self.hours,
            "operating_hours": self.hours,
            "structure": self.structure,
            "vertical_clearance": self.lowest_figure,
            "width_limit": self.lowest_figure,
            "surface": self.coded(SURFACES),
            "vehicle_access_class": self.coded(ACCESS_CLASSES),
            "accepted_vehicle_classes": self.vehicle_class_list,
            "vehicle_limits": self.vehicle_limits,
            "fares": self.fares,
            "terminals": self.terminals,
        }

    def fail(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def code(self, list_name: str, code: str, where: str) -> None:
        entry = self.vocab.lists[list_name].get(code)
        label = GOVERNED_LISTS[list_name]
        if entry is None:
            self.fail(where, f"unknown {label} code {code!r}")
        elif entry["status"] != "active" and self.rejects_deprecated:
            self.fail(where, f"{label} {code!r} is deprecated")

    def coded(self, list_name: str) -> Callable[[Any, str], None]:
        """A check for a fact whose value is an object with one governed list code in code."""
        return lambda value, where: self.code(list_name, value["code"], f"{where}/code")

    def structure(self, value: dict, where: str) -> None:
        self.code(STRUCTURES, value["code"], f"{where}/code")
        entry = self.vocab.lists[STRUCTURES].get(value["code"])
        if entry and value["passage"] not in entry["passages"]:
            allowed = ", ".join(entry["passages"])
            self.fail(
                f"{where}/passage",
                f"a {value['code']} allows passage {allowed}, not {value['passage']}",
            )

    def lowest_figure(self, value: dict, where: str) -> None:
        """lowest_m is the lowest figure of any basis, and lowest_basis is that figure's basis."""
        figures = value["measurements"]
        lowest = min(item["value_m"] for item in figures)
        bases = {item["basis"] for item in figures if item["value_m"] == lowest}
        if value["lowest_m"] != lowest:
            self.fail(
                f"{where}/lowest_m", f"is {value['lowest_m']} but the lowest figure is {lowest}"
            )
        elif value["lowest_basis"] not in bases:
            self.fail(
                f"{where}/lowest_basis",
                f"is {value['lowest_basis']} but the lowest figure is {', '.join(sorted(bases))}",
            )

    def site_types(self, value: dict, where: str) -> None:
        others = value.get("others", [])
        self.code(SITE_TYPES, value["primary"], f"{where}/primary")
        for index, code in enumerate(others):
            self.code(SITE_TYPES, code, f"{where}/others/{index}")
        if value["primary"] in others:
            self.fail(where, "primary site type repeated in others")

    def description(self, value: list, where: str) -> None:
        languages = [item["lang"].lower() for item in value]
        if len(languages) != len(set(languages)):
            self.fail(where, "more than one description in the same language")

    def hours(self, value: dict, where: str) -> None:
        for index, exception in enumerate(value.get("exceptions", [])):
            if exception["from"] > exception["to"]:
                self.fail(f"{where}/exceptions/{index}", "from is after to")

    def vehicle_class_list(self, value: list, where: str) -> None:
        for index, code in enumerate(value):
            self.code(VEHICLE_CLASSES, code, f"{where}/{index}")

    def vehicle_limits(self, value: dict, where: str) -> None:
        for index, item in enumerate(value.get("by_vehicle_class", [])):
            path = f"{where}/by_vehicle_class/{index}/vehicle_class"
            self.code(VEHICLE_CLASSES, item["vehicle_class"], path)

    def fares(self, value: dict, where: str) -> None:
        for index, item in enumerate(value.get("items", [])):
            self.code(
                VEHICLE_CLASSES, item["vehicle_class"], f"{where}/items/{index}/vehicle_class"
            )

    def terminals(self, value: list, where: str) -> None:
        """A ferry service's terminals are sites whose site types include ferry_terminal."""
        for index, site_id in enumerate(value):
            types = self.context.sites.get(site_id)
            if types is None:
                if self.context.sites_complete:
                    self.fail(f"{where}/{index}", f"{site_id} is not a known site")
            elif "ferry_terminal" not in types:
                self.fail(f"{where}/{index}", f"{site_id} is not a ferry_terminal site")

    def facts(self, values: dict, where: str, suffix: str) -> None:
        """Check plain fact values. suffix is /value when the facts came from the full form."""
        for name, check in self.fact_checks.items():
            if name in values:
                check(values[name], f"{where}/{name}{suffix}")
        self.carried_classes(values, where, suffix)

    def carried_classes(self, values: dict, where: str, suffix: str) -> None:
        """Fares and vehicle limits only name vehicle classes the ferry service carries."""
        accepted = values.get("accepted_vehicle_classes")
        if accepted is None:
            return
        named = [
            (fact, field, item)
            for fact, field in (("fares", "items"), ("vehicle_limits", "by_vehicle_class"))
            for item in values.get(fact, {}).get(field, [])
        ]
        for fact, field, item in named:
            if item["vehicle_class"] not in accepted:
                self.fail(
                    f"{where}/{fact}{suffix}/{field}",
                    f"vehicle class {item['vehicle_class']!r} is not in accepted_vehicle_classes",
                )

    def facilities(self, facilities: dict, where: str) -> None:
        for code in facilities:
            self.code(FACILITIES, code, f"{where}/{code}")

    def derived(self, values: dict, where: str) -> None:
        """Point records hold one country and subdivision, line records lists of them."""
        countries = values.get("country_codes") or [values.get("country_code")]
        subdivisions = values.get("subdivision_codes") or [values.get("subdivision_code")]
        for subdivision in filter(None, subdivisions):
            if not any(
                subdivision.startswith(f"{country}-") for country in filter(None, countries)
            ):
                self.fail(
                    where, f"subdivision {subdivision} is not in country {' or '.join(countries)}"
                )
        time_zone = values.get("time_zone")
        zones = record_zones(values)
        for zone in dict.fromkeys(filter(None, [time_zone, *zones])):
            try:
                zoneinfo.ZoneInfo(zone)
            except (zoneinfo.ZoneInfoNotFoundError, ValueError):
                self.fail(where, f"unknown IANA time zone {zone!r}")
        if zones and time_zone and zones[0] != time_zone:
            self.fail(where, f"time_zones starts with {zones[0]}, not time_zone {time_zone}")
        for index, (zone, following) in enumerate(zip(zones, zones[1:]), start=1):
            if zone == following:
                self.fail(
                    f"{where.rstrip('/')}/time_zones/{index}",
                    f"{zone} is listed twice in a row: list a zone again only after another",
                )

    def schedule_zones(self, values: dict, zones: list[str], where: str, suffix: str) -> None:
        """A schedule's own time_zone is one of the zones the record lies in."""
        for name, fact in values.items():
            zone = fact.get("time_zone") if isinstance(fact, dict) else None
            if zone and zones and zone not in zones:
                self.fail(
                    f"{where}/{name}{suffix}/time_zone",
                    f"{zone} is not one of the record's time zones ({', '.join(zones)})",
                )

    def same_type(self, record_id: str, others: list[str], where: str) -> None:
        """Records merged together, or named as duplicates, share one record type and differ."""
        for index, other in enumerate(others):
            if other == record_id:
                self.fail(f"{where}/{index}", "names the record itself")
            elif record_type_of(other) != record_type_of(record_id):
                self.fail(f"{where}/{index}", f"{other} is not a {record_type_of(record_id).code}")

    def other_type(self, record_id: str, other: str, where: str) -> None:
        """A replacement is a record of another record type."""
        if record_type_of(other) == record_type_of(record_id):
            self.fail(
                where,
                f"{other} is a {record_type_of(record_id).code} too: a replacement is another record type",
            )

    def always_human_reasons(self, kind: str, record_type: str, fields: list[str]) -> list[str]:
        """Why a submission is on the always-human list, from its kind and the schema's markers."""
        reasons = []
        if kind.startswith("new_") or kind in ALWAYS_HUMAN_KINDS:
            reasons.append(f"{kind} is on the always-human list")
        safety = self.context.safety_fields[record_type]
        reasons += [
            f"{field} is a safety fact of a {record_type}" for field in fields if field in safety
        ]
        return reasons


def check_record(document: dict, checker: SemanticChecker, full: bool) -> None:
    """Any record in either form. The full form wraps facts and nests derived values."""
    if full:
        derived, where, suffix = document.get("derived", {}), "/derived", "/value"
        values = {name: fact["value"] for name, fact in document.get("facts", {}).items()}
        facts_where = "/facts"
    else:
        derived, where, suffix, values, facts_where = document, "/", "", document, ""
    checker.derived(derived, where)
    checker.schedule_zones(values, record_zones(derived), facts_where, suffix)
    checker.facts(values, facts_where, suffix)
    checker.facilities(document.get("facilities", {}), "/facilities")
    status = document["status"]["value"] if full else document["status"]
    target = document.get("redirect_to")
    if target == document["id"]:
        checker.fail("/redirect_to", "a record cannot redirect to itself")
    elif target and status == "merged":
        checker.same_type(document["id"], [target], "/redirect_to")
    elif target and status == "replaced":
        checker.other_type(document["id"], target, "/redirect_to")
    if status == "retracted":
        allowed = STUB_FIELDS if full else STUB_FIELDS_COMPACT
        for name in sorted(document.keys() - allowed):
            checker.fail(f"/{name}", "a retracted record keeps only its stub")


def check_submission(document: dict, checker: SemanticChecker) -> None:
    proposed = document["proposed"]
    checker.facts(proposed.get("facts", {}), "/proposed/facts", "")
    checker.facilities(proposed.get("facilities", {}), "/proposed/facilities")
    if document["kind"] == "request_merge":
        duplicates = proposed["duplicate_record_ids"]
        checker.same_type(document["record_id"], duplicates, "/proposed/duplicate_record_ids")
    for index, part in enumerate(proposed.get("parts", [])):
        where = f"/proposed/parts/{index}"
        checker.facts(part["facts"], f"{where}/facts", "")
        checker.facilities(part.get("facilities", {}), f"{where}/facilities")
    if document["kind"] == "request_replacement":
        new_type = proposed["record_type"]
        if new_type == record_type_of(document["record_id"]).code:
            checker.fail("/proposed/record_type", f"is {new_type}, the record's own type")


def check_moderation_decision(document: dict, checker: SemanticChecker) -> None:
    check_decision_results(document, checker)
    if "routing" not in document:
        return
    routing = document["routing"]
    kind, record_type = routing["submission_kind"], routing["record_type"]
    if kind.startswith("new_") and kind != RECORD_TYPE_BY_CODE[record_type].new_kind:
        checker.fail("/routing/record_type", f"{kind} does not create a {record_type}")
    reasons = checker.always_human_reasons(kind, record_type, routing.get("fields", []))
    if reasons and not routing["always_human"]:
        checker.fail("/routing/always_human", f"must be true: {'; '.join(reasons)}")
    if reasons and document["decided_by"]["kind"] == "routing_rule":
        checker.fail("/decided_by", f"a routing rule cannot decide this: {'; '.join(reasons)}")


def check_decision_results(document: dict, checker: SemanticChecker) -> None:
    """Merges, unmerges and splits stay within one record type, and a replacement leaves it."""
    merge = document.get("merge")
    if merge:
        survivor = merge["surviving_record_id"]
        checker.same_type(survivor, merge["merged_record_ids"], "/merge/merged_record_ids")
    unmerge = document.get("unmerge")
    if unmerge:
        checker.same_type(
            unmerge["record_id"], [unmerge["unmerged_from"]], "/unmerge/unmerged_from"
        )
    split = document.get("split")
    if split:
        checker.same_type(split["record_id"], split["new_record_ids"], "/split/new_record_ids")
    replacement = document.get("replacement")
    if replacement:
        checker.other_type(
            replacement["record_id"], replacement["replaced_by"], "/replacement/replaced_by"
        )


def check_change(document: dict, checker: SemanticChecker) -> None:
    record_id = document["record_id"]
    for field in ("merged_into", "unmerged_from", "split_from"):
        if field in document:
            checker.same_type(record_id, [document[field]], f"/{field}")
    if "split_into" in document:
        checker.same_type(record_id, document["split_into"], "/split_into")
    if "replaced_by" in document:
        checker.other_type(record_id, document["replaced_by"], "/replaced_by")
    safety = checker.context.safety_fields[record_type_of(record_id).code]
    changed = [field for field in document["changed_fields"] if field in safety]
    if changed and document.get("safety_fact_changed") is False:
        checker.fail("/safety_fact_changed", f"is false but {', '.join(changed)} changed")


def check_nothing(document: dict, checker: SemanticChecker) -> None:
    pass


def check_translation(document: dict, checker: SemanticChecker) -> None:
    """A translation names only codes and attributes of its reference list, in another language."""
    reference_file = list_file(document["list"])
    reference = checker.vocab.lists[reference_file]
    if canonical_tag(document["language"]) == REFERENCE_LANGUAGE:
        checker.fail(
            "/language", f"{REFERENCE_LANGUAGE} is the reference language, not a translation"
        )
    if version_tuple(document["reference_version"]) > version_tuple(
        checker.vocab.versions[reference_file]
    ):
        checker.fail(
            "/reference_version",
            f"{document['reference_version']} is newer than {reference_file} "
            f"{checker.vocab.versions[reference_file]}",
        )
    for code, entry in document["entries"].items():
        where = f"/entries/{code}"
        if code not in reference:
            checker.fail(where, f"code {code!r} is not in {reference_file}")
            continue
        names = {attribute["name"] for attribute in reference[code].get("attributes", [])}
        for name in entry.get("attributes", {}):
            if name not in names:
                checker.fail(f"{where}/attributes/{name}", f"{code} has no attribute {name!r}")


def is_translation(path: Path) -> bool:
    """Translations sit at i18n/<language>/<list file>."""
    return path.parent.parent.name == I18N


def translation_file(path: Path, document: dict) -> list[str]:
    """The folder names the translation's language, the file name its list, and it is licensed.

    Language tags compare case-insensitively, and the folder is the tag in canonical case.
    """
    problems = []
    folder, expected_file = path.parent.name, list_file(document["list"])
    language = document["language"]
    if canonical_tag(language) != canonical_tag(folder):
        problems.append(f"/language: is {language} but the folder is {folder}")
    elif folder != canonical_tag(folder):
        problems.append(
            f"/language: the folder {folder} must be the tag in canonical case, "
            f"{canonical_tag(folder)} (tags compare case-insensitively)"
        )
    if path.name != expected_file:
        problems.append(f"/list: is {document['list']} but the file is {path.name}")
    if document.get(COMMENT_KEY) != SPDX_COMMENT:
        problems.append(f"/{COMMENT_KEY}: must be {SPDX_COMMENT!r}, like every governed list file")
    return problems


def no_file_rules(path: Path, document: dict) -> list[str]:
    """Documents other than translations have no rules on the file itself."""
    return []


@dataclass(frozen=True)
class DocumentKind:
    """A kind of document: its file suffix and schema follow from stem."""

    stem: str
    semantic_check: Callable[[dict, SemanticChecker], None]
    rejects_deprecated: bool = False
    # Rules on the file itself, given its path and the document with its $comment.
    file_check: Callable[[Path, dict], list[str]] = no_file_rules

    @property
    def suffix(self) -> str:
        return f".{self.stem}.json"

    @property
    def schema(self) -> str:
        return schema_file(self.stem)

    @staticmethod
    def for_path(path: Path) -> DocumentKind | None:
        if is_translation(path):
            return TRANSLATION
        return next((kind for kind in DOCUMENT_KINDS if path.name.endswith(kind.suffix)), None)


def full_record(document: dict, checker: SemanticChecker) -> None:
    check_record(document, checker, full=True)


def compact_record(document: dict, checker: SemanticChecker) -> None:
    check_record(document, checker, full=False)


DOCUMENT_KINDS = tuple(
    kind
    for record_type in RECORD_TYPES
    for kind in (
        DocumentKind(record_type.stem, full_record),
        DocumentKind(f"{record_type.stem}-compact", compact_record),
    )
) + (
    DocumentKind("submission", check_submission, rejects_deprecated=True),
    DocumentKind("verdict", check_nothing),
    DocumentKind("moderation-decision", check_moderation_decision),
    DocumentKind("change", check_change),
)
TRANSLATION = DocumentKind("translation", check_translation, file_check=translation_file)


def check_document(path: Path, context: Context) -> list[str]:
    kind = DocumentKind.for_path(path)
    if kind is None:
        suffixes = ", ".join(kind.suffix for kind in DOCUMENT_KINDS)
        return [
            f"/: cannot tell the schema from the file name (expected one of {suffixes}, "
            f"or a translation at {I18N}/<language>/<list file>)"
        ]
    raw = load_json(path)
    document = without_comment(raw)
    schema_errors = list(context.validator(kind.schema).iter_errors(document))
    if schema_errors:
        return all_errors(schema_errors)
    checker = SemanticChecker(context, kind.rejects_deprecated)
    kind.semantic_check(document, checker)
    return checker.errors + kind.file_check(path, raw)


def check_record_type(context: Context, record_type: RecordType) -> list[str]:
    """The full form, FactValues, the compact form and the submissions agree on one fact table."""
    problems: list[str] = []
    full = record_type.full
    facts = context.definition(full, "Facts")
    values = context.definition(full, "FactValues")["properties"]
    required = context.definition(full, "RequiredFacts")["required"]
    for name in facts["properties"].keys() ^ values.keys():
        problems.append(f"{full}: fact {name} is in only one of Facts and FactValues")
    for name, fact in facts["properties"].items():
        shape = ref_name(fact["properties"]["value"])
        if name in values and shape != ref_name(values[name]):
            problems.append(
                f"{full}: Facts {name} holds {shape}, FactValues {ref_name(values[name])}"
            )
    for name in record_type.computed - values.keys():
        problems.append(f"{full}: computed fact {name} is not a fact")

    shared_required = f"{full}#RequiredFacts"
    uses = {
        f"{full} Facts": [ref_name(item) for item in facts.get("allOf", [])],
        record_type.compact: [
            ref_name(item)
            for branch in context.schemas[record_type.compact]["allOf"]
            for item in branch.get("else", {}).get("allOf", [])
        ],
    }
    submission = context.schemas["submission.schema.json"]["$defs"]
    new = submission[f"New{record_type.camel}Submission"]["properties"]["proposed"]
    uses[f"New{record_type.camel}Submission"] = [
        ref_name(item) for item in new["properties"]["facts"].get("allOf", [])
    ]
    for user, refs in uses.items():
        if shared_required not in refs and "#RequiredFacts" not in refs:
            problems.append(f"{user} does not use {shared_required}")
    compact_refs = [ref_name(item) for item in context.schemas[record_type.compact]["allOf"]]
    if f"{full}#FactValues" not in compact_refs:
        problems.append(f"{record_type.compact} does not use {full}#FactValues")

    submitted = submission[f"{record_type.camel}Facts"]
    if ref_name(submitted) != f"{full}#FactValues":
        problems.append(f"submission.schema.json {record_type.camel}Facts is not {full}#FactValues")
    excluded = {name for name, rule in submitted.get("properties", {}).items() if rule is False}
    if excluded != record_type.computed:
        problems.append(
            f"{record_type.camel}Facts excludes {sorted(excluded)}, not the computed facts"
        )
    update = submission[f"{record_type.camel}FactsUpdate"]["properties"]["proposed"]["properties"]
    forbidden = set(update["remove"]["items"]["not"]["enum"])
    if forbidden != {f"/facts/{name}" for name in required}:
        problems.append(
            f"{record_type.camel}FactsUpdate forbids removing {sorted(forbidden)}, "
            f"but RequiredFacts is {required}"
        )
    kinds = submission_kinds(context)
    if record_type.new_kind not in kinds:
        problems.append(f"submission.schema.json has no kind {record_type.new_kind}")
    return problems


def submission_kinds(context: Context) -> list[str]:
    return context.definition("common.schema.json", "SubmissionKind")[KNOWN_VALUES]


def check_schemas(context: Context) -> list[str]:
    problems: list[str] = []
    for name, schema in context.schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as metaschema_error:  # noqa: BLE001 - report any metaschema failure
            problems.append(f"{name}: not a valid 2020-12 schema: {metaschema_error}")

    vocabulary_validator = context.validator("vocabulary.schema.json")
    for list_file in GOVERNED_LISTS:
        document = load_json(SCHEMA_DIR / list_file)
        errors = sorted(
            vocabulary_validator.iter_errors(document), key=lambda e: list(map(str, e.path))
        )
        problems += [f"{list_file}{describe(error)}" for error in errors]
        codes = [entry["code"] for entry in document["entries"]]
        if len(codes) != len(set(codes)):
            problems.append(f"{list_file}: duplicate codes")
        if document.get("language") != REFERENCE_LANGUAGE:
            problems.append(f"{list_file}: language must be {REFERENCE_LANGUAGE}, the reference")
        for entry in document["entries"]:
            for field in FALLBACK_FIELDS:
                if field in entry:
                    problems.append(f"{list_file} {entry['code']}: {field} is for API responses")
    ranks = [entry.get("rank") or 0 for entry in context.vocab.lists[ACCESS_CLASSES].values()]
    if sorted(ranks) != list(range(1, len(ranks) + 1)):
        problems.append(
            f"{ACCESS_CLASSES}: ranks must run 1, 2, 3 and so on without gaps, got {ranks}"
        )

    for record_type in RECORD_TYPES:
        problems += check_record_type(context, record_type)
    creation = {kind for kind in submission_kinds(context) if kind.startswith("new_")}
    if creation != {record_type.new_kind for record_type in RECORD_TYPES}:
        problems.append(f"creation kinds {sorted(creation)} do not match the record types")
    problems += check_facilities(context)
    problems += check_record_type_registry(context)
    problems += check_open_enumerations(context)
    return problems


def check_record_type_registry(context: Context) -> list[str]:
    """record-types.json is valid, and each entry names its schemas, ID kind and creation kind."""
    problems: list[str] = []
    document = load_json(SCHEMA_DIR / RECORD_TYPE_REGISTRY)
    validator = context.validator("record-types.schema.json")
    problems += [
        f"{RECORD_TYPE_REGISTRY}{describe(error)}" for error in validator.iter_errors(document)
    ]
    reserved = re.compile(context.definition("common.schema.json", "NonRecordId")["pattern"])
    codes = [entry["code"] for entry in document["entries"]]
    if len(codes) != len(set(codes)):
        problems.append(f"{RECORD_TYPE_REGISTRY}: duplicate codes")
    for entry, record_type in zip(document["entries"], RECORD_TYPES):
        where = f"{RECORD_TYPE_REGISTRY} {entry['code']}"
        if reserved.match(f"otwd:{entry['code']}:"):
            problems.append(f"{where}: the ID kind is reserved for another identifier")
        if (entry["full_schema"], entry["compact_schema"]) != (
            record_type.full,
            record_type.compact,
        ):
            problems.append(
                f"{where}: schemas must be {record_type.full} and {record_type.compact}"
            )
        for name in (entry["full_schema"], entry["compact_schema"]):
            if name not in context.schemas:
                problems.append(f"{where}: {name} does not exist")
        if entry["creation_kind"] != record_type.new_kind:
            problems.append(f"{where}: creation_kind must be {record_type.new_kind}")
    return problems


def open_enumerations(node: Any, where: str = "") -> Iterable[tuple[str, list]]:
    """Every x-otwd-known-values list in a schema, with where it is."""
    if isinstance(node, dict):
        if KNOWN_VALUES in node:
            yield where, node[KNOWN_VALUES]
        for key, value in node.items():
            yield from open_enumerations(value, f"{where}/{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from open_enumerations(value, f"{where}/{index}")


def check_open_enumerations(context: Context) -> list[str]:
    """Known values are unique, follow EnumCode, and sit on a schema that only allows EnumCode."""
    problems: list[str] = []
    pattern = re.compile(context.definition("common.schema.json", "EnumCode")["pattern"])
    for name, schema in context.schemas.items():
        for where, known in open_enumerations(schema):
            if len(known) != len(set(known)):
                problems.append(f"{name}{where}: {KNOWN_VALUES} repeats a value")
            for value in known:
                if not pattern.match(value):
                    problems.append(f"{name}{where}: {value!r} does not follow EnumCode")
    return problems


def check_facilities(context: Context) -> list[str]:
    """facilities.json, values.schema.json and the site schema agree on codes and attributes."""
    problems: list[str] = []
    values = "values.schema.json"
    per_code = context.definition(values, "Facilities")["properties"]
    site_facilities = context.definition("site.schema.json", "FacilityFacts")["properties"]
    if site_facilities.keys() != per_code.keys():
        difference = sorted(site_facilities.keys() ^ per_code.keys())
        problems.append(
            f"site.schema.json FacilityFacts and {values} list different codes: {difference}"
        )
    marked = {code for code, fact in site_facilities.items() if fact.get(SAFETY_MARKER)}
    listed_safety = {
        code
        for code, entry in context.vocab.facilities.items()
        if entry.get("safety_fact") and code not in context.vocab.stored_elsewhere
    }
    if marked != listed_safety:
        problems.append(
            f"site.schema.json marks safety facilities {sorted(marked)}, "
            f"but facilities.json marks {sorted(listed_safety)}"
        )
    for code, entry in context.vocab.facilities.items():
        listed = {attribute["name"] for attribute in entry.get("attributes", [])}
        ref = per_code.get(code, {}).get("$ref")
        defined: set[str] = set()
        if ref:
            value_schema = context.definition(values, ref.rsplit("/", 1)[1])
            defined = set(value_schema["properties"]["attributes"]["properties"])
        if listed != defined:
            problems.append(
                f"facilities.json {code}: attributes {sorted(listed)} "
                f"do not match {values} {sorted(defined)}"
            )
    for code in per_code.keys() - context.vocab.facilities.keys():
        problems.append(f"{values} defines facility {code!r} that is not in facilities.json")
    excluded = context.definition(values, "StoredFacilities")["not"]["anyOf"]
    excluded_codes = {item["required"][0] for item in excluded}
    if excluded_codes != context.vocab.stored_elsewhere:
        problems.append(
            f"StoredFacilities excludes {sorted(excluded_codes)} but facilities.json marks "
            f"{sorted(context.vocab.stored_elsewhere)} as stored_as"
        )
    return problems


def report(label: str, name: str, problems: list[str], indent: str) -> None:
    print(f"{indent}{label}  {name}")
    for message in problems:
        print(f"{indent}      {shorten(message)}")


def check_given_files(arguments: list[str], context: Context) -> bool:
    paths = [Path(argument) for argument in arguments]
    context = context.with_sites(paths, complete=False)
    ok = True
    for path in paths:
        problems = check_document(path, context)
        report("PASS" if not problems else "FAIL", str(path), problems, indent="")
        ok &= not problems
    return ok


def documents_in(folder: Path) -> list[Path]:
    """The documents in a folder and the translations in its i18n tree."""
    paths = sorted(path for path in folder.glob("*.json") if path.name != "expected.json")
    return paths + sorted(folder.glob(f"{I18N}/*/*.json"))


def check_passing(title: str, folder: Path, paths: list[Path], context: Context) -> bool:
    print(f"\n{title}")
    ok = True
    for path in paths:
        problems = check_document(path, context)
        name = str(path.relative_to(folder))
        report("pass" if not problems else "FAIL", name, problems, indent="  ")
        ok &= not problems
    if not paths:
        print("  none yet")
    return ok


def check_valid_examples(context: Context) -> tuple[bool, int]:
    folder = EXAMPLES / "valid"
    paths = documents_in(folder)
    return check_passing("Valid examples (must pass)", folder, paths, context), len(paths)


def check_translations(context: Context) -> tuple[bool, int]:
    paths = sorted((SCHEMA_DIR / I18N).glob("*/*.json"))
    title = f"Translations in {I18N}/ (must pass)"
    return check_passing(title, SCHEMA_DIR, paths, context), len(paths)


def check_consumer_examples(context: Context) -> tuple[bool, int]:
    """Documents from a later minor version: a consumer accepts them, a producer may not send them.

    Each must pass the plain 2020-12 validator, which ignores the open enumeration keywords as
    any consumer's validator does, and must fail the producer validator on one of them, so it
    proves an unknown value is accepted rather than passing for some other reason.
    """
    print("\nConsumer examples (a consumer accepts them, a producer may not send them)")
    ok = True
    folder = EXAMPLES / "consumer"
    paths = documents_in(folder)
    for path in paths:
        kind = DocumentKind.for_path(path)
        if kind is None:
            print(f"  FAIL  {path.name}: cannot tell the schema from the file name")
            ok = False
            continue
        document = without_comment(load_json(path))
        consumer = all_errors(context.validator(kind.schema, consumer=True).iter_errors(document))
        producer = all_errors(context.validator(kind.schema).iter_errors(document))
        unknown = [message for message in producer if PRODUCER_ONLY in message]
        if consumer:
            report("FAIL", f"{path.name}: a consumer must accept it", consumer[:8], "  ")
            ok = False
        elif not unknown:
            print(f"  FAIL  {path.name}: it must carry a value only a later version knows")
            ok = False
        else:
            print(f"  pass  {path.name}  ({len(unknown)} unknown to this version)")
    return ok, len(paths)


def check_invalid_examples(context: Context) -> tuple[bool, int]:
    print("\nInvalid examples (must fail with the expected error)")
    ok = True
    folder = EXAMPLES / "invalid"
    expected: dict[str, str] = without_comment(load_json(folder / "expected.json"))
    paths = documents_in(folder)
    names = [str(path.relative_to(folder)) for path in paths]
    for path, name in zip(paths, names):
        problems = check_document(path, context)
        fragment = expected.get(name)
        if fragment is None:
            print(f"  FAIL  {name}: no entry in expected.json")
            ok = False
        elif not problems:
            print(f"  FAIL  {name}: validated, but it must fail")
            ok = False
        elif not any(fragment in message for message in problems):
            report("FAIL", f"{name}: failed, but not with {fragment!r}", problems[:8], "  ")
            ok = False
        else:
            print(f"  fail  {name}  ({fragment})")
    for name in sorted(set(expected) - set(names)):
        print(f"  FAIL  expected.json names {name}, which does not exist")
        ok = False
    return ok, len(paths)


def main(arguments: list[str]) -> int:
    missing = REQUIRED_FORMATS - set(Draft202012Validator.FORMAT_CHECKER.checkers)
    if missing:
        print(f"Format checkers missing: {sorted(missing)}. Install schema/tools/requirements.txt.")
        return 1

    context = Context.load()
    if arguments:
        return 0 if check_given_files(arguments, context) else 1

    print("Schemas and governed lists")
    problems = check_schemas(context)
    for message in problems:
        print(f"  FAIL  {message}")
    if not problems:
        counts = ", ".join(
            f"{len(context.vocab.lists[name])} {label} codes"
            for name, label in GOVERNED_LISTS.items()
        )
        print(f"  ok    {len(context.schemas)} schemas, {len(RECORD_TYPES)} record types, {counts}")

    # Ferry terminals in the examples must be sites among the valid examples.
    context = context.with_sites((EXAMPLES / "valid").glob("*.json"), complete=True)
    valid_ok, valid_count = check_valid_examples(context)
    invalid_ok, invalid_count = check_invalid_examples(context)
    consumer_ok, consumer_count = check_consumer_examples(context)
    translations_ok, translation_count = check_translations(context)
    ok = not problems and valid_ok and invalid_ok and consumer_ok and translations_ok
    verdict = "all expectations met" if ok else "EXPECTATIONS NOT MET"
    counts = (
        f"{valid_count} valid, {invalid_count} invalid, {consumer_count} consumer, "
        f"{translation_count} translations"
    )
    print(f"\n{counts}: {verdict}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

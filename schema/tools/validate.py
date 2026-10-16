#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the OTWD JSON Schema, the governed lists and the examples.

Usage:
    python3 schema/tools/validate.py              # check everything
    python3 schema/tools/validate.py FILE...      # check documents of your own

A document's schema is chosen from its file name suffix:
    *.site.json, *.site-compact.json, *.submission.json, *.verdict.json,
    *.moderation-decision.json, *.change.json

The script runs three stages:

1. Every *.schema.json file is checked against the JSON Schema 2020-12
   metaschema, and the governed lists (site-types.json, facilities.json)
   are checked against vocabulary.schema.json and against the per-facility
   schemas in values.schema.json.
2. Each document is validated against its schema with format checking on
   (date, date-time, uri, email, json-pointer).
3. Rules that JSON Schema cannot express, and that the API also enforces,
   are checked: governed list codes, ISO 3166-2 prefixes, IANA time zones
   and a few cross-field rules.

A top-level "$comment" in a document (the SPDX header of the example files)
is removed before validation.

Files under examples/valid must pass. Files under examples/invalid must fail,
and examples/invalid/expected.json names a fragment of the error each one must
produce, so an invalid example cannot pass by failing for the wrong reason.
The exit status is 0 when every expectation holds and 1 otherwise.
"""

from __future__ import annotations

import json
import sys
import zoneinfo
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SCHEMA_DIR = Path(__file__).resolve().parent.parent
EXAMPLES = SCHEMA_DIR / "examples"
BASE = "https://schema.opentouring.org/otwd/v1/"
COMMENT_KEY = "$comment"

# Formats the schemas rely on. Without the packages in requirements.txt the
# jsonschema library silently skips some of them, so their absence is fatal.
REQUIRED_FORMATS = {"date", "date-time", "uri", "email", "json-pointer"}

VOCABULARY_SCHEMA = "vocabulary.schema.json"
VALUES_SCHEMA = "values.schema.json"
SITE_SCHEMA = "site.schema.json"
GOVERNED_LISTS = ("site-types.json", "facilities.json")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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


def top_level_errors(errors: Iterable[ValidationError]) -> list[str]:
    ordered = sorted(errors, key=lambda error: [str(part) for part in error.absolute_path])
    return [describe(error) for error in ordered]


class Vocab:
    """The governed lists, keyed by code."""

    def __init__(self) -> None:
        site_types = load_json(SCHEMA_DIR / "site-types.json")
        facilities = load_json(SCHEMA_DIR / "facilities.json")
        self.site_types = {entry["code"]: entry for entry in site_types["entries"]}
        self.facilities = {entry["code"]: entry for entry in facilities["entries"]}
        self.stored_elsewhere = {code for code, entry in self.facilities.items() if "stored_as" in entry}


@dataclass(frozen=True)
class Context:
    """Everything a check needs: the schema registry, the schemas by file name and the governed lists."""

    registry: Registry
    schemas: dict[str, dict]
    vocab: Vocab

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
            registry = registry.with_resource(
                expected_id, Resource.from_contents(schema, default_specification=DRAFT202012)
            )
        return cls(registry.crawl(), schemas, Vocab())

    def validator(self, schema_name: str) -> Draft202012Validator:
        return Draft202012Validator(
            self.schemas[schema_name],
            registry=self.registry,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )

    def definition(self, schema_name: str, def_name: str) -> dict:
        """A named entry in a schema's $defs."""
        return self.schemas[schema_name]["$defs"][def_name]


class SemanticChecker:
    """Rules JSON Schema cannot express. The API applies the same rules."""

    def __init__(self, vocab: Vocab, rejects_deprecated: bool) -> None:
        self.vocab = vocab
        self.rejects_deprecated = rejects_deprecated
        self.errors: list[str] = []

    def site_type(self, code: str, where: str) -> None:
        entry = self.vocab.site_types.get(code)
        if entry is None:
            self.errors.append(f"{where}: unknown site type code {code!r}")
        elif entry["status"] != "active" and self.rejects_deprecated:
            self.errors.append(f"{where}: site type {code!r} is deprecated")

    def facilities(self, facilities: dict, where: str) -> None:
        for code in facilities:
            if code not in self.vocab.facilities:
                self.errors.append(f"{where}/{code}: unknown facility code {code!r}")

    def site_types(self, value: dict, where: str) -> None:
        others = value.get("others", [])
        self.site_type(value["primary"], f"{where}/primary")
        for index, code in enumerate(others):
            self.site_type(code, f"{where}/others/{index}")
        if value["primary"] in others:
            self.errors.append(f"{where}: primary site type repeated in others")

    def description(self, value: list, where: str) -> None:
        languages = [item["lang"].lower() for item in value]
        if len(languages) != len(set(languages)):
            self.errors.append(f"{where}: more than one description in the same language")

    def hours(self, value: dict, where: str) -> None:
        for index, exception in enumerate(value.get("exceptions", [])):
            if exception["from"] > exception["to"]:
                self.errors.append(f"{where}/exceptions/{index}: from is after to")

    def facts(self, facts: dict, where: str, wrapped: bool) -> None:
        """Check fact values. wrapped: each fact is a {value, provenance} object (full form)."""
        checks: dict[str, Callable[[Any, str], None]] = {
            "site_types": self.site_types,
            "description": self.description,
            "opening_hours": self.hours,
            "reception_hours": self.hours,
        }
        suffix = "/value" if wrapped else ""
        for name, check in checks.items():
            fact = facts.get(name)
            if fact is not None:
                check(fact["value"] if wrapped else fact, f"{where}/{name}{suffix}")

    def derived(self, country: str | None, subdivision: str | None, time_zone: str | None, where: str) -> None:
        if country and subdivision and not subdivision.startswith(country + "-"):
            self.errors.append(f"{where}: subdivision {subdivision} is not in country {country}")
        if time_zone:
            try:
                zoneinfo.ZoneInfo(time_zone)
            except (zoneinfo.ZoneInfoNotFoundError, ValueError):
                self.errors.append(f"{where}: unknown IANA time zone {time_zone!r}")


def check_site(document: dict, checker: SemanticChecker) -> None:
    derived = document.get("derived", {})
    checker.derived(derived.get("country_code"), derived.get("subdivision_code"), derived.get("time_zone"), "/derived")
    checker.facts(document.get("facts", {}), "/facts", wrapped=True)
    checker.facilities(document.get("facilities", {}), "/facilities")
    if document.get("redirect_to") == document.get("id"):
        checker.errors.append("/redirect_to: a site cannot redirect to itself")


def check_site_compact(document: dict, checker: SemanticChecker) -> None:
    checker.derived(document.get("country_code"), document.get("subdivision_code"), document.get("time_zone"), "/")
    checker.facts(document, "", wrapped=False)
    checker.facilities(document.get("facilities", {}), "/facilities")


def check_submission(document: dict, checker: SemanticChecker) -> None:
    proposed = document.get("proposed", {})
    if not isinstance(proposed, dict):
        return
    checker.facts(proposed.get("facts", {}), "/proposed/facts", wrapped=False)
    checker.facilities(proposed.get("facilities", {}), "/proposed/facilities")
    if document.get("kind") == "request_merge" and document.get("site_id") in proposed.get("duplicate_site_ids", []):
        checker.errors.append("/proposed/duplicate_site_ids: lists the submission's own site_id")


def check_moderation_decision(document: dict, checker: SemanticChecker) -> None:
    merge = document.get("merge")
    if merge and merge["surviving_site_id"] in merge["merged_site_ids"]:
        checker.errors.append("/merge: surviving site is also listed as merged")


def check_change(document: dict, checker: SemanticChecker) -> None:
    if document.get("merged_into") == document.get("site_id"):
        checker.errors.append("/merged_into: a site cannot merge into itself")


def check_nothing(document: dict, checker: SemanticChecker) -> None:
    pass


@dataclass(frozen=True)
class KindSpec:
    suffix: str
    schema: str
    semantic_check: Callable[[dict, SemanticChecker], None]
    rejects_deprecated: bool = False


class DocumentKind(Enum):
    """Every kind of document the validator knows, with its file suffix, schema and extra rules."""

    SITE_COMPACT = KindSpec(".site-compact.json", "site-compact.schema.json", check_site_compact)
    SITE = KindSpec(".site.json", SITE_SCHEMA, check_site)
    SUBMISSION = KindSpec(".submission.json", "submission.schema.json", check_submission, rejects_deprecated=True)
    VERDICT = KindSpec(".verdict.json", "verdict.schema.json", check_nothing)
    MODERATION_DECISION = KindSpec(
        ".moderation-decision.json", "moderation-decision.schema.json", check_moderation_decision
    )
    CHANGE = KindSpec(".change.json", "change.schema.json", check_change)

    @classmethod
    def for_path(cls, path: Path) -> DocumentKind | None:
        return next((kind for kind in cls if path.name.endswith(kind.value.suffix)), None)


def check_document(path: Path, context: Context) -> list[str]:
    kind = DocumentKind.for_path(path)
    if kind is None:
        suffixes = ", ".join(kind.value.suffix for kind in DocumentKind)
        return [f"/: cannot tell the schema from the file name (expected one of {suffixes})"]
    spec = kind.value
    document = without_comment(load_json(path))
    schema_errors = list(context.validator(spec.schema).iter_errors(document))
    if schema_errors:
        return all_errors(schema_errors)
    checker = SemanticChecker(context.vocab, spec.rejects_deprecated)
    spec.semantic_check(document, checker)
    return checker.errors


def check_schemas(context: Context) -> list[str]:
    problems: list[str] = []
    for name, schema in context.schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as metaschema_error:  # noqa: BLE001 - report any metaschema failure
            problems.append(f"{name}: not a valid 2020-12 schema: {metaschema_error}")

    vocabulary_validator = context.validator(VOCABULARY_SCHEMA)
    for list_file in GOVERNED_LISTS:
        document = load_json(SCHEMA_DIR / list_file)
        for message in top_level_errors(vocabulary_validator.iter_errors(document)):
            problems.append(f"{list_file}{message}")
        codes = [entry["code"] for entry in document["entries"]]
        if len(codes) != len(set(codes)):
            problems.append(f"{list_file}: duplicate codes")

    # facilities.json and values.schema.json must agree on attributes, and the
    # site schema must check every facility the values schema checks.
    per_code = context.definition(VALUES_SCHEMA, "Facilities")["properties"]
    site_codes = set(context.definition(SITE_SCHEMA, "FacilityFacts")["properties"])
    if site_codes != set(per_code):
        problems.append(
            "site.schema.json FacilityFacts and values.schema.json Facilities list different codes: "
            f"{sorted(site_codes ^ set(per_code))}"
        )
    for code, entry in context.vocab.facilities.items():
        listed = {attribute["name"] for attribute in entry.get("attributes", [])}
        ref = per_code.get(code, {}).get("$ref")
        defined: set[str] = set()
        if ref:
            value_schema = context.definition(VALUES_SCHEMA, ref.rsplit("/", 1)[1])
            defined = set(value_schema["properties"]["attributes"]["properties"])
        if listed != defined:
            problems.append(
                f"facilities.json {code}: attributes {sorted(listed)} do not match values.schema.json {sorted(defined)}"
            )
    for code in per_code:
        if code not in context.vocab.facilities:
            problems.append(f"values.schema.json defines facility {code!r} that is not in facilities.json")
    excluded = context.definition(VALUES_SCHEMA, "StoredFacilities")["not"]["anyOf"]
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
    ok = True
    for argument in arguments:
        path = Path(argument)
        problems = check_document(path, context)
        report("PASS" if not problems else "FAIL", str(path), problems, indent="")
        ok &= not problems
    return ok


def check_valid_examples(context: Context) -> tuple[bool, int]:
    print("\nValid examples (must pass)")
    ok = True
    paths = sorted((EXAMPLES / "valid").glob("*.json"))
    for path in paths:
        problems = check_document(path, context)
        report("pass" if not problems else "FAIL", path.name, problems, indent="  ")
        ok &= not problems
    return ok, len(paths)


def check_invalid_examples(context: Context) -> tuple[bool, int]:
    print("\nInvalid examples (must fail with the expected error)")
    ok = True
    expected: dict[str, str] = without_comment(load_json(EXAMPLES / "invalid" / "expected.json"))
    paths = sorted(path for path in (EXAMPLES / "invalid").glob("*.json") if path.name != "expected.json")
    for path in paths:
        problems = check_document(path, context)
        fragment = expected.get(path.name)
        if fragment is None:
            print(f"  FAIL  {path.name}: no entry in expected.json")
            ok = False
        elif not problems:
            print(f"  FAIL  {path.name}: validated, but it must fail")
            ok = False
        elif not any(fragment in message for message in problems):
            report("FAIL", f"{path.name}: failed, but not with {fragment!r}", problems[:8], indent="  ")
            ok = False
        else:
            print(f"  fail  {path.name}  ({fragment})")
    for name in sorted(set(expected) - {path.name for path in paths}):
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
        vocab = context.vocab
        print(f"  ok    {len(context.schemas)} schemas, {len(vocab.site_types)} site types, {len(vocab.facilities)} facilities")

    valid_ok, valid_count = check_valid_examples(context)
    invalid_ok, invalid_count = check_invalid_examples(context)
    ok = not problems and valid_ok and invalid_ok
    print(f"\n{valid_count} valid, {invalid_count} invalid: {'all expectations met' if ok else 'EXPECTATIONS NOT MET'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""
Validate Agentic Enterprise Origin Ledger examples.

Dependencies:
    pip install jsonschema pyyaml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT_DIR = Path(__file__).resolve().parents[1]

VALIDATION_TARGETS = [
    (
        ROOT_DIR
        / "schemas"
        / "enterprise-knowledge-origin-record.schema.json",
        ROOT_DIR
        / "examples"
        / "enterprise-knowledge-origin-record.example.yaml",
        "Enterprise Knowledge Origin Record",
    ),
    (
        ROOT_DIR
        / "schemas"
        / "knowledge-to-agent-skill-binding.schema.json",
        ROOT_DIR
        / "examples"
        / "knowledge-to-agent-skill-binding.example.yaml",
        "Knowledge-to-Agent Skill Binding",
    ),
    (
        ROOT_DIR
        / "schemas"
        / "cross-department-execution-trace.schema.json",
        ROOT_DIR
        / "examples"
        / "cross-department-execution-trace.example.yaml",
        "Cross-Department Execution Trace",
    ),
]


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in {path}: "
            f"line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"Expected a JSON object in {path}")

    return data


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from disk."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"YAML file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"Expected a YAML mapping in {path}")

    return data


def format_error_path(error: Any) -> str:
    """Convert a jsonschema error path into dotted notation."""
    if not error.absolute_path:
        return "<root>"

    parts: list[str] = []

    for item in error.absolute_path:
        if isinstance(item, int):
            if parts:
                parts[-1] = f"{parts[-1]}[{item}]"
            else:
                parts.append(f"[{item}]")
        else:
            parts.append(str(item))

    return ".".join(parts)


def validate_document(
    schema_path: Path,
    example_path: Path,
    label: str,
) -> bool:
    """Validate one YAML example against one JSON Schema."""
    print(f"[validate] {label}")
    print(f"  schema : {schema_path.relative_to(ROOT_DIR)}")
    print(f"  example: {example_path.relative_to(ROOT_DIR)}")

    schema = load_json(schema_path)
    example = load_yaml(example_path)

    Draft202012Validator.check_schema(schema)

    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    errors = sorted(
        validator.iter_errors(example),
        key=lambda error: list(error.absolute_path),
    )

    if errors:
        for error in errors:
            print(f"  [error] {format_error_path(error)}: {error.message}")

        print(f"[failed] {label}")
        return False

    print(f"[schema-ok] {label}")
    print(f"[example-ok] {label}")
    return True


def main() -> int:
    """Run every registered validation target."""
    print("=== Agentic Enterprise Origin Ledger Validation ===")
    print()

    all_valid = True

    for schema_path, example_path, label in VALIDATION_TARGETS:
        try:
            valid = validate_document(
                schema_path=schema_path,
                example_path=example_path,
                label=label,
            )
        except RuntimeError as exc:
            print(f"[fatal] {exc}")
            valid = False
        except Exception as exc:
            print(f"[fatal] Unexpected validation error: {exc}")
            valid = False

        all_valid = all_valid and valid
        print()

    if all_valid:
        print("All examples are valid.")
        return 0

    print("Validation failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

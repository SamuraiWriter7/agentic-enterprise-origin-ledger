#!/usr/bin/env python3
"""
Validate Agentic Enterprise Origin Ledger examples.

The script validates every schema/example pair currently present in the
repository. It also applies semantic checks to the v0.4 Human Contribution
Attribution example.

Dependencies:
    pip install jsonschema pyyaml
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT_DIR = Path(__file__).resolve().parents[1]

KNOWN_TARGETS = [
    (
        "schemas/enterprise-knowledge-origin-record.schema.json",
        "examples/enterprise-knowledge-origin-record.example.yaml",
        "Enterprise Knowledge Origin Record",
    ),
    (
        "schemas/knowledge-to-agent-skill-binding.schema.json",
        "examples/knowledge-to-agent-skill-binding.example.yaml",
        "Knowledge-to-Agent Skill Binding",
    ),
    (
        "schemas/cross-department-execution-trace.schema.json",
        "examples/cross-department-execution-trace.example.yaml",
        "Cross-Department Execution Trace",
    ),
    (
        "schemas/human-contribution-attribution.schema.json",
        "examples/human-contribution-attribution.example.yaml",
        "Human Contribution Attribution",
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


def validate_schema_document(
    schema_path: Path,
    example_path: Path,
    label: str,
) -> tuple[bool, dict[str, Any] | None]:
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
        return False, example

    print(f"[schema-ok] {label}")
    print(f"[example-ok] {label}")
    return True, example


def semantic_error(path: str, message: str) -> None:
    """Print one semantic validation error."""
    print(f"  [semantic-error] {path}: {message}")


def validate_v04_semantics(document: dict[str, Any]) -> bool:
    """Apply arithmetic and cross-field checks not expressible in JSON Schema."""
    print("[semantic] Human Contribution Attribution")

    valid = True
    tolerance = 1e-6

    methodology = document["methodology"]
    dimensions = methodology["dimensions"]
    contributors = document["human_contributors"]
    aggregate = document["aggregate_attribution"]

    dimension_ids = [item["dimension_id"] for item in dimensions]
    dimension_weights = {
        item["dimension_id"]: float(item["weight"])
        for item in dimensions
    }

    if len(dimension_ids) != len(set(dimension_ids)):
        semantic_error(
            "methodology.dimensions",
            "dimension_id values must be unique.",
        )
        valid = False

    total_dimension_weight = sum(dimension_weights.values())

    if not math.isclose(
        total_dimension_weight,
        1.0,
        rel_tol=0.0,
        abs_tol=tolerance,
    ):
        semantic_error(
            "methodology.dimensions",
            f"dimension weights sum to {total_dimension_weight}, not 1.0.",
        )
        valid = False

    contribution_ids = [
        item["contribution_id"]
        for item in contributors
    ]

    if len(contribution_ids) != len(set(contribution_ids)):
        semantic_error(
            "human_contributors",
            "contribution_id values must be unique.",
        )
        valid = False

    relative_weight_sum = 0.0

    for index, contributor in enumerate(contributors):
        path = f"human_contributors[{index}]"
        scores = contributor["dimension_scores"]
        score_ids = [item["dimension_id"] for item in scores]

        if len(score_ids) != len(set(score_ids)):
            semantic_error(
                f"{path}.dimension_scores",
                "dimension_id values must be unique.",
            )
            valid = False

        if set(score_ids) != set(dimension_ids):
            missing = sorted(set(dimension_ids) - set(score_ids))
            extra = sorted(set(score_ids) - set(dimension_ids))
            semantic_error(
                f"{path}.dimension_scores",
                f"score dimensions differ from methodology; "
                f"missing={missing}, extra={extra}.",
            )
            valid = False

        score_map = {
            item["dimension_id"]: float(item["raw_score"])
            for item in scores
        }

        calculated_score = sum(
            score_map[dimension_id] * weight
            for dimension_id, weight in dimension_weights.items()
            if dimension_id in score_map
        )

        precision = int(methodology["rounding_precision"])
        calculated_score = round(calculated_score, precision)
        recorded_score = float(
            contributor["computed_attribution"]["weighted_score"]
        )

        score_tolerance = 10 ** (-precision)

        if not math.isclose(
            calculated_score,
            recorded_score,
            rel_tol=0.0,
            abs_tol=score_tolerance,
        ):
            semantic_error(
                f"{path}.computed_attribution.weighted_score",
                f"recorded={recorded_score}, calculated={calculated_score}.",
            )
            valid = False

        computed = contributor["computed_attribution"]

        if computed["weight_status"] != "excluded":
            relative_weight_sum += float(computed["relative_weight"])

        dependencies = contributor["causal_assessment"]["dependency_links"]

        unknown_dependencies = sorted(
            set(dependencies) - set(contribution_ids)
        )

        if unknown_dependencies:
            semantic_error(
                f"{path}.causal_assessment.dependency_links",
                f"unknown contribution references: {unknown_dependencies}.",
            )
            valid = False

        if contributor["contribution_id"] in dependencies:
            semantic_error(
                f"{path}.causal_assessment.dependency_links",
                "a contribution cannot depend on itself.",
            )
            valid = False

    normalized_total = (
        relative_weight_sum
        + float(aggregate["unattributed_weight"])
    )

    if not math.isclose(
        normalized_total,
        float(aggregate["total_relative_weight"]),
        rel_tol=0.0,
        abs_tol=tolerance,
    ):
        semantic_error(
            "aggregate_attribution.total_relative_weight",
            f"human weights + unattributed weight = {normalized_total}, "
            f"recorded total = {aggregate['total_relative_weight']}.",
        )
        valid = False

    if not math.isclose(
        float(aggregate["total_relative_weight"]),
        1.0,
        rel_tol=0.0,
        abs_tol=tolerance,
    ):
        semantic_error(
            "aggregate_attribution.total_relative_weight",
            "normalized attribution total must equal 1.0.",
        )
        valid = False

    open_disputes = [
        contributor["contribution_id"]
        for contributor in contributors
        if contributor["dispute"]["status"] == "open"
    ]

    if open_disputes and aggregate["allocation_readiness"] == "ready":
        semantic_error(
            "aggregate_attribution.allocation_readiness",
            f"cannot be ready while disputes are open: {open_disputes}.",
        )
        valid = False

    if valid:
        print("[semantic-ok] Human Contribution Attribution")

    return valid


def existing_targets() -> list[tuple[Path, Path, str]]:
    """Return schema/example targets present in the current repository."""
    targets: list[tuple[Path, Path, str]] = []

    for schema_rel, example_rel, label in KNOWN_TARGETS:
        schema_path = ROOT_DIR / schema_rel
        example_path = ROOT_DIR / example_rel

        if schema_path.exists() and example_path.exists():
            targets.append((schema_path, example_path, label))

    return targets


def main() -> int:
    """Run every schema and semantic validation target."""
    print("=== Agentic Enterprise Origin Ledger Validation ===")
    print()

    targets = existing_targets()

    if not targets:
        print("[fatal] No known schema/example pairs were found.")
        return 1

    all_valid = True

    for schema_path, example_path, label in targets:
        try:
            valid, example = validate_schema_document(
                schema_path=schema_path,
                example_path=example_path,
                label=label,
            )

            if (
                valid
                and example is not None
                and example.get("record_type")
                == "human_contribution_attribution"
            ):
                valid = validate_v04_semantics(example) and valid

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

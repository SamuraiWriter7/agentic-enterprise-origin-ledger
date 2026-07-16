#!/usr/bin/env python3
"""
Validate Agentic Enterprise Origin Ledger examples.

The script discovers known schema/example pairs that are present in the
repository. It performs JSON Schema validation and semantic arithmetic checks
for v0.4 and v0.5 records.

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
    (
        "schemas/enterprise-value-return-ledger.schema.json",
        "examples/enterprise-value-return-ledger.example.yaml",
        "Enterprise Value Return Ledger",
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
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}"
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


def money_amount(value: dict[str, Any]) -> float:
    """Extract a numeric amount from a money object."""
    return float(value["amount"])


def validate_v04_semantics(document: dict[str, Any]) -> bool:
    """Apply arithmetic and cross-field checks to a v0.4 record."""
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

    if not math.isclose(total_dimension_weight, 1.0, abs_tol=tolerance):
        semantic_error(
            "methodology.dimensions",
            f"dimension weights sum to {total_dimension_weight}, not 1.0.",
        )
        valid = False

    contribution_ids = [item["contribution_id"] for item in contributors]

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

        if set(score_ids) != set(dimension_ids):
            semantic_error(
                f"{path}.dimension_scores",
                "score dimensions must match the methodology dimensions.",
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

        score_tolerance = 10 ** (-precision) if precision > 0 else 1.0

        if not math.isclose(
            calculated_score,
            recorded_score,
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

    normalized_total = (
        relative_weight_sum
        + float(aggregate["unattributed_weight"])
    )

    if not math.isclose(
        normalized_total,
        float(aggregate["total_relative_weight"]),
        abs_tol=tolerance,
    ):
        semantic_error(
            "aggregate_attribution.total_relative_weight",
            "human weights plus unattributed weight do not match the recorded total.",
        )
        valid = False

    if valid:
        print("[semantic-ok] Human Contribution Attribution")

    return valid


def validate_v05_semantics(document: dict[str, Any]) -> bool:
    """Apply currency, allocation, and settlement checks to a v0.5 ledger."""
    print("[semantic] Enterprise Value Return Ledger")

    valid = True
    tolerance = 1e-6

    case_currency = document["value_case"]["currency"]
    verification = document["value_verification"]
    policy = document["return_policy"]
    eligibility = document["eligibility"]
    recipients = document["recipient_allocations"]
    collective = document["collective_allocations"]
    summary = document["settlement_summary"]
    governance = document["governance"]
    lifecycle = document["lifecycle"]

    money_objects: list[tuple[str, dict[str, Any]]] = [
        ("value_verification.gross_verified_value", verification["gross_verified_value"]),
        ("value_verification.excluded_value", verification["excluded_value"]),
        ("return_policy.gross_return_pool", policy["gross_return_pool"]),
    ]

    if policy.get("minimum_pool") is not None:
        money_objects.append(("return_policy.minimum_pool", policy["minimum_pool"]))

    if policy.get("maximum_pool") is not None:
        money_objects.append(("return_policy.maximum_pool", policy["maximum_pool"]))

    for index, component in enumerate(verification["components"]):
        money_objects.append((f"value_verification.components[{index}].value", component["value"]))

    for index, allocation in enumerate(recipients):
        money_objects.extend(
            [
                (f"recipient_allocations[{index}].allocated_value", allocation["allocated_value"]),
                (f"recipient_allocations[{index}].immediate_value", allocation["immediate_value"]),
                (f"recipient_allocations[{index}].held_value", allocation["held_value"]),
            ]
        )

    for index, allocation in enumerate(collective):
        money_objects.extend(
            [
                (f"collective_allocations[{index}].allocated_value", allocation["allocated_value"]),
                (f"collective_allocations[{index}].immediate_value", allocation["immediate_value"]),
                (f"collective_allocations[{index}].held_value", allocation["held_value"]),
            ]
        )

    for path, money in money_objects:
        if money["currency"] != case_currency:
            semantic_error(
                f"{path}.currency",
                f"currency {money['currency']} differs from case currency {case_currency}.",
            )
            valid = False

    if summary["currency"] != case_currency:
        semantic_error(
            "settlement_summary.currency",
            "summary currency differs from the value-case currency.",
        )
        valid = False

    included_total = sum(
        money_amount(component["value"])
        for component in verification["components"]
        if component["inclusion_status"] == "included"
    )
    excluded_total = sum(
        money_amount(component["value"])
        for component in verification["components"]
        if component["inclusion_status"] == "excluded"
    )

    recorded_gross = money_amount(verification["gross_verified_value"])
    recorded_excluded = money_amount(verification["excluded_value"])

    if not math.isclose(included_total, recorded_gross, abs_tol=tolerance):
        semantic_error(
            "value_verification.gross_verified_value",
            f"included components sum to {included_total}, recorded={recorded_gross}.",
        )
        valid = False

    if not math.isclose(excluded_total, recorded_excluded, abs_tol=tolerance):
        semantic_error(
            "value_verification.excluded_value",
            f"excluded components sum to {excluded_total}, recorded={recorded_excluded}.",
        )
        valid = False

    pool = money_amount(policy["gross_return_pool"])
    precision = int(policy["allocation_precision"])
    amount_tolerance = 10 ** (-precision) if precision > 0 else 1.0

    if policy["basis_type"] == "percentage_of_verified_value":
        expected_pool = round(recorded_gross * float(policy["return_rate"]), precision)
        if not math.isclose(pool, expected_pool, abs_tol=amount_tolerance):
            semantic_error(
                "return_policy.gross_return_pool",
                f"recorded={pool}, expected={expected_pool} from verified value and return rate.",
            )
            valid = False

    decisions = eligibility["decisions"]
    decision_ids = [item["contribution_id"] for item in decisions]

    if len(decision_ids) != len(set(decision_ids)):
        semantic_error(
            "eligibility.decisions",
            "contribution_id values must be unique.",
        )
        valid = False

    eligible_ids = {
        item["contribution_id"]
        for item in decisions
        if item["eligible"] is True and item["decision"] == "eligible"
    }

    allocation_ids = [item["allocation_id"] for item in recipients]
    allocation_ids.extend(item["allocation_id"] for item in collective)

    if len(allocation_ids) != len(set(allocation_ids)):
        semantic_error(
            "recipient_allocations / collective_allocations",
            "allocation_id values must be unique across the ledger.",
        )
        valid = False

    total_weight = 0.0
    recipient_allocated = 0.0
    recipient_immediate = 0.0
    recipient_held = 0.0

    for index, allocation in enumerate(recipients):
        path = f"recipient_allocations[{index}]"
        contribution_id = allocation["contribution_id"]

        if contribution_id not in eligible_ids:
            semantic_error(
                f"{path}.contribution_id",
                f"{contribution_id} is not eligible for allocation.",
            )
            valid = False

        weight = float(allocation["allocation_weight"])
        allocated = money_amount(allocation["allocated_value"])
        immediate = money_amount(allocation["immediate_value"])
        held = money_amount(allocation["held_value"])

        expected_allocated = round(pool * weight, precision)
        expected_held = round(allocated * float(policy["holdback_rate"]), precision)

        if not math.isclose(allocated, expected_allocated, abs_tol=amount_tolerance):
            semantic_error(
                f"{path}.allocated_value.amount",
                f"recorded={allocated}, expected={expected_allocated} from allocation weight.",
            )
            valid = False

        if not math.isclose(immediate + held, allocated, abs_tol=amount_tolerance):
            semantic_error(
                path,
                "immediate value plus held value must equal allocated value.",
            )
            valid = False

        if not math.isclose(held, expected_held, abs_tol=amount_tolerance):
            semantic_error(
                f"{path}.held_value.amount",
                f"recorded={held}, expected={expected_held} from holdback rate.",
            )
            valid = False

        total_weight += weight
        recipient_allocated += allocated
        recipient_immediate += immediate
        recipient_held += held

    collective_allocated = 0.0
    collective_immediate = 0.0
    collective_held = 0.0

    for index, allocation in enumerate(collective):
        path = f"collective_allocations[{index}]"
        weight = float(allocation["allocation_weight"])
        allocated = money_amount(allocation["allocated_value"])
        immediate = money_amount(allocation["immediate_value"])
        held = money_amount(allocation["held_value"])
        expected_allocated = round(pool * weight, precision)

        if not math.isclose(allocated, expected_allocated, abs_tol=amount_tolerance):
            semantic_error(
                f"{path}.allocated_value.amount",
                f"recorded={allocated}, expected={expected_allocated} from allocation weight.",
            )
            valid = False

        if not math.isclose(immediate + held, allocated, abs_tol=amount_tolerance):
            semantic_error(
                path,
                "immediate value plus held value must equal allocated value.",
            )
            valid = False

        total_weight += weight
        collective_allocated += allocated
        collective_immediate += immediate
        collective_held += held

    if not math.isclose(total_weight, 1.0, abs_tol=tolerance):
        semantic_error(
            "allocations",
            f"recipient and collective allocation weights sum to {total_weight}, not 1.0.",
        )
        valid = False

    total_allocated = recipient_allocated + collective_allocated
    total_immediate = recipient_immediate + collective_immediate
    total_held = recipient_held + collective_held

    checks = [
        (
            "settlement_summary.total_pool",
            float(summary["total_pool"]),
            pool,
        ),
        (
            "settlement_summary.total_recipient_allocations",
            float(summary["total_recipient_allocations"]),
            recipient_allocated,
        ),
        (
            "settlement_summary.total_collective_allocations",
            float(summary["total_collective_allocations"]),
            collective_allocated,
        ),
        (
            "settlement_summary.total_immediate",
            float(summary["total_immediate"]),
            total_immediate,
        ),
        (
            "settlement_summary.total_held",
            float(summary["total_held"]),
            total_held,
        ),
        (
            "settlement_summary.total_unallocated",
            float(summary["total_unallocated"]),
            pool - total_allocated,
        ),
    ]

    for path, recorded, expected in checks:
        if not math.isclose(recorded, expected, abs_tol=amount_tolerance):
            semantic_error(
                path,
                f"recorded={recorded}, calculated={expected}.",
            )
            valid = False

    if not math.isclose(total_allocated, pool, abs_tol=amount_tolerance):
        semantic_error(
            "allocations",
            f"allocated total {total_allocated} does not equal pool {pool}.",
        )
        valid = False

    open_appeals = [
        item["appeal_id"]
        for item in governance["appeals"]
        if item["status"] in {"open", "under_review"}
    ]

    if open_appeals and summary["settlement_ready"] is True:
        semantic_error(
            "settlement_summary.settlement_ready",
            f"cannot be true while appeals are open: {open_appeals}.",
        )
        valid = False

    if lifecycle["status"] == "settled":
        if not math.isclose(
            float(summary["total_settled"]),
            pool,
            abs_tol=amount_tolerance,
        ):
            semantic_error(
                "settlement_summary.total_settled",
                "a settled ledger must record the entire pool as settled.",
            )
            valid = False

    if verification["double_counting_check"] == "failed":
        semantic_error(
            "value_verification.double_counting_check",
            "a failed double-counting check cannot support a v0.5 ledger.",
        )
        valid = False

    if valid:
        print("[semantic-ok] Enterprise Value Return Ledger")

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

            if valid and example is not None:
                record_type = example.get("record_type")

                if record_type == "human_contribution_attribution":
                    valid = validate_v04_semantics(example) and valid
                elif record_type == "enterprise_value_return_ledger":
                    valid = validate_v05_semantics(example) and valid

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

# Agentic Enterprise Origin Ledger

A protocol for preserving the origin, transformation, execution, attribution, and value return of enterprise knowledge used by AI agents.

## Overview

Enterprise AI agents increasingly rely on:

* employee expertise;
* team practices;
* process documents;
* system records;
* operational observations;
* regulatory requirements;
* customer feedback;
* organizational decision rules.

When this knowledge is converted into prompts, workflows, agent skills, or automated decision logic, its origin can easily disappear.

The **Agentic Enterprise Origin Ledger** provides a structured lineage from human and organizational knowledge to enterprise value:

```text
Enterprise Knowledge Origin
        ↓
Knowledge-to-Agent Skill Binding
        ↓
Cross-Department Execution Trace
        ↓
Human Contribution Attribution
        ↓
Enterprise Value Return Ledger
```

The protocol is designed to answer five questions:

```text
v0.1  Where did the knowledge originate?
v0.2  How was it transformed into an agent skill?
v0.3  What happened when the skill operated?
v0.4  Which human contributions supported the outcome?
v0.5  How is verified value returned?
```

## Core principle

> Enterprise knowledge must not lose its origin merely because it becomes machine-usable.

The protocol preserves:

* knowledge provenance;
* contributor attribution;
* supporting evidence;
* operational limitations;
* inherited permissions;
* human-review requirements;
* agent execution traces;
* decision authority;
* causal contribution;
* verified business effects;
* monetary and non-monetary value return.

## Protocol architecture

### v0.1 — Enterprise Knowledge Origin Record

Records enterprise knowledge before it is transformed into an AI-agent skill.

It captures:

* the knowledge origin;
* human, team, system, or organizational contributors;
* capture methods;
* supporting evidence;
* known limitations;
* confidentiality;
* permissions;
* governance flags;
* human-review requirements;
* lifecycle status.

Core rule:

> Origin must be recorded before automation begins.

### v0.2 — Knowledge-to-Agent Skill Binding

Binds an approved knowledge origin to a specific AI-agent skill.

It records:

* the source origin record;
* the resulting skill;
* inputs and outputs;
* invocation conditions;
* prohibited behavior;
* transformation steps;
* retained knowledge;
* lost or distorted context;
* inherited permissions;
* validation tests;
* deployment and rollback conditions.

Core rule:

> A skill must not outlive or outrun its origin.

### v0.3 — Cross-Department Execution Trace

Records how an agent skill operates across departments.

It captures:

* execution triggers;
* participating departments;
* data access;
* agent decisions;
* human approvals;
* human corrections and overrides;
* policy checks;
* department-to-department handoffs;
* restrictions carried forward;
* operational results;
* business effects;
* trace completeness;
* causal completeness.

Core rule:

> Data, authority, restrictions, and attribution must travel together.

### v0.4 — Human Contribution Attribution

Attributes human contribution across the full lineage.

It distinguishes:

```text
Contribution
    ≠
Decision authority
    ≠
Risk responsibility
    ≠
Monetary allocation
```

It records:

* origin creation;
* evidence provision;
* knowledge capture;
* skill transformation;
* domain review;
* contextual judgment;
* correction;
* authorization;
* outcome validation;
* stewardship;
* counterfactual causal assessment;
* evidence-weighted scores;
* relative attribution weights;
* unattributed collective contribution;
* disputes and appeals;
* non-human agent and system support.

Core rule:

> Visibility is not the same as causality.

### v0.5 — Enterprise Value Return Ledger

Connects verified enterprise value to an approved contribution-attribution record.

It records:

* verified value components;
* excluded or speculative value;
* valuation evidence;
* double-counting checks;
* value-return policy;
* contributor eligibility;
* individual and team allocations;
* collective knowledge-fund allocations;
* immediate and held value;
* settlement routes;
* appeals;
* non-monetary recognition;
* protected time;
* governance participation;
* lifecycle and settlement status.

Core rule:

> Verified value may return only through verified lineage.

## Important distinctions

### Enterprise value is not the return pool

```text
Verified enterprise value
        ≠
Value-return pool
        ≠
Immediate payment
```

An organization may verify a business effect while returning only a policy-defined share.

### Contribution is not responsibility

A knowledge originator may contribute substantially without holding final operational authority.

A final approver may accept operational responsibility without becoming the sole owner of upstream knowledge.

### AI support is not human contribution

Agents and systems are recorded under non-human support.

They remain visible in the causal chain but are not presented as human contributors.

### Unattributed contribution is valid

Where evidence is incomplete, the protocol preserves an unattributed share rather than assigning it arbitrarily.

That share may be returned to:

* shared knowledge funds;
* organizational infrastructure;
* verification reserves;
* contributor-discovery programs;
* collective stewardship.

## Repository structure

```text
agentic-enterprise-origin-ledger/
├─ .github/
│  └─ workflows/
│     └─ validate.yml
├─ schemas/
│  ├─ enterprise-knowledge-origin-record.schema.json
│  ├─ knowledge-to-agent-skill-binding.schema.json
│  ├─ cross-department-execution-trace.schema.json
│  ├─ human-contribution-attribution.schema.json
│  └─ enterprise-value-return-ledger.schema.json
├─ examples/
│  ├─ enterprise-knowledge-origin-record.example.yaml
│  ├─ knowledge-to-agent-skill-binding.example.yaml
│  ├─ cross-department-execution-trace.example.yaml
│  ├─ human-contribution-attribution.example.yaml
│  └─ enterprise-value-return-ledger.example.yaml
├─ docs/
│  ├─ v0.1-enterprise-knowledge-origin-record.md
│  ├─ v0.2-knowledge-to-agent-skill-binding.md
│  ├─ v0.3-cross-department-execution-trace.md
│  ├─ v0.4-human-contribution-attribution.md
│  └─ v0.5-enterprise-value-return-ledger.md
├─ scripts/
│  └─ validate_examples.py
├─ requirements-dev.txt
├─ README.md
├─ CHANGELOG.md
└─ LICENSE
```

## Record lineage

A downstream record should reference upstream records rather than copying their contents without provenance.

```text
ekor_*   Enterprise Knowledge Origin Record
   ↓
kasb_*   Knowledge-to-Agent Skill Binding
   ↓
cdet_*   Cross-Department Execution Trace
   ↓
hca_*    Human Contribution Attribution
   ↓
evrl_*   Enterprise Value Return Ledger
```

Example:

```yaml
origin_record_id: ekor_spindle-vibration-001
skill_binding_id: kasb_spindle-diagnosis-001
execution_trace_ids:
  - cdet_spindle-anomaly-20260716-001
attribution_id: hca_spindle-anomaly-20260716-002
ledger_id: evrl_spindle-anomaly-20260716-001
```

## Validation

The project uses:

* JSON Schema Draft 2020-12;
* YAML examples;
* `jsonschema`;
* `PyYAML`;
* semantic validation for cross-field calculations.

### Install dependencies

Create `requirements-dev.txt` in the repository root:

```text
jsonschema>=4.23,<5
PyYAML>=6.0.2,<7
```

Install:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### Run validation

```bash
python scripts/validate_examples.py
```

Expected result:

```text
=== Agentic Enterprise Origin Ledger Validation ===

[validate] Enterprise Knowledge Origin Record
[schema-ok] Enterprise Knowledge Origin Record
[example-ok] Enterprise Knowledge Origin Record

[validate] Knowledge-to-Agent Skill Binding
[schema-ok] Knowledge-to-Agent Skill Binding
[example-ok] Knowledge-to-Agent Skill Binding

[validate] Cross-Department Execution Trace
[schema-ok] Cross-Department Execution Trace
[example-ok] Cross-Department Execution Trace

[validate] Human Contribution Attribution
[schema-ok] Human Contribution Attribution
[example-ok] Human Contribution Attribution
[semantic-ok] Human Contribution Attribution

[validate] Enterprise Value Return Ledger
[schema-ok] Enterprise Value Return Ledger
[example-ok] Enterprise Value Return Ledger
[semantic-ok] Enterprise Value Return Ledger

All examples are valid.
```

## Semantic validation

Some requirements cannot be expressed reliably through JSON Schema alone.

The validation script additionally checks:

### v0.4 checks

* attribution-dimension weights total `1.0`;
* contributor score dimensions match the methodology;
* weighted scores can be reproduced;
* contribution IDs are unique;
* dependency references exist;
* human relative weights and unattributed weight total `1.0`;
* open disputes block allocation readiness.

### v0.5 checks

* all monetary values use the declared currency;
* included value components equal gross verified value;
* excluded components equal excluded value;
* percentage-based return pools are calculated correctly;
* recipient allocations reference eligible contributors;
* allocation IDs are unique;
* allocation weights total `1.0`;
* immediate and held values equal allocated value;
* holdbacks match the declared policy;
* recipient and collective allocations equal the return pool;
* settlement-summary totals can be reproduced;
* open appeals block settlement readiness;
* failed double-counting checks block the ledger.

## GitHub Actions

The repository includes a validation workflow:

```text
.github/workflows/validate.yml
```

The workflow runs on:

* pushes to `main`;
* pull requests;
* manual dispatch;
* changes to schemas, examples, scripts, dependencies, or the workflow itself.

It validates the repository against multiple supported Python versions.

### Required dependency file

When pip caching is enabled in `actions/setup-python`, the following file must be committed to the repository root:

```text
requirements-dev.txt
```

Without that file, the cache dependency lookup will fail.

### Minimal workflow

```yaml
name: Validate Protocol Examples

on:
  push:
    branches:
      - main
    paths:
      - "schemas/**"
      - "examples/**"
      - "scripts/**"
      - "requirements-dev.txt"
      - ".github/workflows/validate.yml"

  pull_request:
    paths:
      - "schemas/**"
      - "examples/**"
      - "scripts/**"
      - "requirements-dev.txt"
      - ".github/workflows/validate.yml"

  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: validate-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    name: Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    timeout-minutes: 10

    strategy:
      fail-fast: false
      matrix:
        python-version:
          - "3.11"
          - "3.12"
          - "3.13"
          - "3.14"

    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
          cache-dependency-path: requirements-dev.txt

      - name: Install validation dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-dev.txt

      - name: Compile validation scripts
        run: python -m compileall -q scripts

      - name: Validate schemas and examples
        run: python scripts/validate_examples.py
```

## Example enterprise flow

```text
A technician discovers a recurring failure pattern
        ↓
The knowledge is captured with evidence and limitations
        ↓
The knowledge is transformed into an advisory agent skill
        ↓
The agent analyzes an operational event
        ↓
A maintenance engineer corrects the proposed action
        ↓
A quality supervisor authorizes a lot hold
        ↓
The execution and human interventions are traced
        ↓
Human contributions are causally attributed
        ↓
Verified cost avoidance is calculated
        ↓
A policy-defined share enters the return pool
        ↓
Value returns to contributors and a shared knowledge fund
```

## Governance principles

A conforming implementation should preserve the following principles.

### Origin preservation

A downstream skill, execution, attribution, or settlement must not remove its source origin.

### Permission inheritance

Machine transformation must not weaken the permissions or restrictions attached to the original knowledge.

### Human authority

Consequential operational decisions must retain explicit human authority where required.

### Evidence before valuation

Estimated, speculative, disputed, or duplicated effects must not enter the verified return pool.

### Attribution before allocation

Money must not be assigned before contribution evidence, causal assessment, and review are complete.

### Appeal before finality

A material open dispute or appeal must block final allocation or settlement.

### Privacy protection

Pseudonymous or withheld contributor identities must remain protected outside authorized review and settlement processes.

### Compensation boundary

Value return must not be used to reduce ordinary salary, benefits, negotiated compensation, or other established rights.

## Non-goals

The protocol does not:

* determine legal ownership;
* determine legal liability;
* replace employment law;
* replace collective bargaining;
* calculate taxes;
* execute bank or payroll payments;
* issue securities or tokens;
* prove universal correctness of an AI-agent skill;
* authorize unrestricted autonomous operation;
* create a general employee-ranking system;
* treat AI-generated scores as self-validating.

## Status

Experimental specification.

The initial v0.1–v0.5 arc is complete.

The protocol currently provides a full conceptual and machine-readable lineage from enterprise knowledge origin to auditable value return.

## License

Apache License 2.0

# Changelog

All notable changes to the **Agentic Enterprise Origin Ledger** are documented in this file.

The project follows semantic versioning where practical.

## [Unreleased]

### Added

* GitHub Actions validation workflow.
* Push, pull-request, and manual validation triggers.
* Multi-version Python validation matrix.
* Dependency caching through `actions/setup-python`.
* Python script compilation check before validation.
* `requirements-dev.txt` dependency definition.

### Fixed

* Documented that `requirements-dev.txt` must exist in the repository root when `cache-dependency-path` is configured.
* Added a cache-free workflow alternative for repositories that do not yet contain a dependency file.

### Validation

* The workflow validates all available schema and example pairs.
* Semantic checks remain enabled for v0.4 and v0.5.

---

## [0.5.0] - 2026-07-16

### Enterprise Value Return Ledger

Completed the first Origin–Derivative–Trace–Attribution–Return protocol arc.

### Added

* Enterprise Value Return Ledger specification.
* JSON Schema Draft 2020-12 implementation.
* Verified spindle-anomaly value-return example.
* References to v0.1 origin records.
* References to v0.2 skill bindings.
* References to v0.3 execution traces.
* Approved and allocation-ready v0.4 attribution references.
* Attribution-record integrity verification.
* Value-case scope and valuation boundaries.
* Included and excluded value components.
* Valuation methodology and evidence references.
* Verified-value confidence status.
* Double-counting checks.
* Gross verified value.
* Excluded speculative value.
* Percentage-based return policies.
* Fixed-pool return policies.
* Hybrid return policies.
* Minimum and maximum return pools.
* Policy-defined return rates.
* Contributor eligibility decisions.
* Individual recipient allocations.
* Human-team allocations.
* Collective allocations.
* Shared knowledge-fund allocations.
* Unattributed contribution handling.
* Immediate monetary value.
* Held monetary value.
* Settlement routes.
* Settlement schedules and references.
* Settlement-status states.
* Non-monetary recognition.
* Protected knowledge-development time.
* Training credits.
* Governance participation.
* Knowledge-stewardship roles.
* Contributor notice controls.
* Appeal windows.
* Appeal records.
* Privacy and identity protections.
* Payroll, tax, employment, and procurement boundaries.
* Settlement-summary balancing.
* Lifecycle states for authorization, settlement, suspension, voiding, and archival.
* Ledger integrity metadata.
* Semantic validation for valuation, currency, allocation, holdback, appeal, and settlement consistency.

### Defined

* Verified enterprise value is distinct from the return pool.
* The return pool is distinct from immediate settlement.
* Only verified value may enter the return pool.
* Estimated, disputed, speculative, or duplicated effects must remain excluded.
* v0.5 may consume only an approved and allocation-ready v0.4 record.
* Recipient and collective allocation weights must total `1.0`.
* Monetary allocations must equal the gross return pool.
* Immediate and held value must equal allocated value.
* Unattributed value must be sent to a declared collective destination.
* Agents and systems cannot receive from the human-recipient pool.
* Non-monetary return must remain separate from monetary allocation.
* Material appeals block settlement readiness.
* Value return must not replace ordinary salary, benefits, or negotiated compensation.
* Origin attribution must survive settlement.

### Changed

* Expanded the protocol from causal contribution attribution into verified value return.
* Added semantic checks for currency consistency.
* Added semantic checks for verified-value totals.
* Added semantic checks for return-pool calculations.
* Added semantic checks for allocation eligibility.
* Added semantic checks for holdback calculations.
* Added semantic checks for settlement totals.
* Added semantic checks for open appeals.
* Completed the first five-version repository arc.

### Not included

* Automatic payroll execution.
* Automatic bank transfers.
* Blockchain settlement.
* Token issuance.
* Tax calculation or withholding.
* Legal ownership determination.
* Legal liability determination.
* Securities or profit-sharing administration.
* Cross-enterprise clearing.

---

## [0.4.0] - 2026-07-16

### Human Contribution Attribution

Introduced evidence-based attribution across knowledge origin, skill transformation, execution, judgment, and outcome verification.

### Added

* Human Contribution Attribution specification.
* JSON Schema Draft 2020-12 implementation.
* Predictive-maintenance contribution-attribution example.
* v0.1 origin lineage.
* v0.2 skill-binding lineage.
* v0.3 execution-trace lineage.
* Execution-trace integrity references.
* Attribution scope.
* Outcome scope.
* Evidence-weighted causal-attribution methodology.
* Versioned attribution dimensions.
* Dimension weights.
* Human-individual contributor records.
* Human-team contributor records.
* Contribution-event references.
* Origin-creation events.
* Evidence-provision events.
* Knowledge-capture events.
* Skill-transformation events.
* Domain-review events.
* Operational-judgment events.
* Correction events.
* Approval and rejection events.
* Outcome-verification events.
* Stewardship events.
* Causal-role classification.
* Required counterfactual assessments.
* Evidence-quality declarations.
* Weighted contribution scores.
* Relative contribution weights.
* Provisional, confirmed, disputed, and excluded weight states.
* Explicit unattributed contribution.
* Separate decision-authority records.
* Separate risk-responsibility records.
* Non-human agent and system support records.
* Dispute and appeal fields.
* Identity-protection controls.
* Allocation-readiness states.
* Semantic validation for dimension totals.
* Semantic validation for score reproduction.
* Semantic validation for dependency references.
* Semantic validation for normalized relative weights.
* Semantic validation for open disputes.

### Defined

* Visibility is not equivalent to causal contribution.
* Origin creation, transformation, execution, correction, authorization, and validation may all support the same result.
* Final authority does not erase upstream contribution.
* Upstream contribution does not imply later operational authority.
* Contribution, authority, responsibility, and monetary allocation must remain separate.
* Every contributor requires evidence.
* Every contributor requires a counterfactual assessment.
* Methodology dimension weights must total `1.0`.
* Human relative weights and unattributed weight must total `1.0`.
* Shared or undocumented contribution must remain unattributed rather than being assigned arbitrarily.
* Agents and systems must not be represented as human contributors.
* Open disputes block allocation readiness.
* Monetary allocation remains outside v0.4.

### Changed

* Expanded the protocol from runtime Trace and Audit into human contribution attribution.
* Updated the validation script to perform v0.4 semantic checks.

### Not included

* Monetary valuation.
* Currency denomination.
* Bonus or royalty calculation.
* Payment execution.
* Tax treatment.
* Employment compensation determination.
* Legal ownership or liability determination.

---

## [0.3.0] - 2026-07-16

### Cross-Department Execution Trace

Introduced auditable execution traces for enterprise-agent operations spanning multiple departments.

### Added

* Cross-Department Execution Trace specification.
* JSON Schema Draft 2020-12 implementation.
* Cross-department predictive-maintenance example.
* Execution context.
* Trigger records.
* Origin and skill lineage.
* Participating-department records.
* Department authorization boundaries.
* Department-to-department handoffs.
* Restrictions carried forward through handoffs.
* Execution-step records.
* Agent actions.
* Human actions.
* System actions.
* Data-access logs.
* Purpose-bound access records.
* Agent decisions.
* Human authority status.
* Decision evidence.
* Human interventions.
* Corrections and overrides.
* Policy evaluations.
* Policy-gate results.
* Operational outcomes.
* Business-effect records.
* Estimated, observed, verified, and unmeasured effect states.
* Trace-completeness assessment.
* Causal-completeness assessment.
* Attribution-preservation checks.
* Permission-propagation checks.
* Trace integrity metadata.
* Lifecycle and retention states.

### Defined

* A department handoff must carry restrictions as well as data.
* Agent decisions and human decisions must be recorded separately.
* Human correction of an agent output must remain visible.
* Human authorization must not be inferred from agent execution.
* Trace completeness and causal completeness are separate conditions.
* Business effects must declare their measurement status.
* Estimated effects must not be treated as verified value.
* Contributor and origin references must survive department handoffs.
* Consequential actions must preserve declared authority boundaries.

### Changed

* Expanded the protocol from static skill binding into runtime operational tracing.
* Updated the validation script to include the v0.3 schema and example.

### Not included

* Human contribution weighting.
* Monetary valuation.
* Value-return allocation.
* Payroll or settlement.
* General employee performance scoring.

---

## [0.2.0] - 2026-07-16

### Knowledge-to-Agent Skill Binding

Introduced the Derivative layer connecting approved enterprise knowledge to AI-agent skills.

### Added

* Knowledge-to-Agent Skill Binding specification.
* JSON Schema Draft 2020-12 implementation.
* Predictive-maintenance agent-skill example.
* Approved origin-record references.
* Origin-record integrity verification.
* Skill identifiers and semantic versions.
* Skill-type declarations.
* Agent-role declarations.
* Skill input contracts.
* Skill output contracts.
* Invocation conditions.
* Explicit prohibited behaviors.
* Tool dependencies.
* Model requirements.
* Transformation-method records.
* Transformation participants.
* Transformation steps.
* Retained-knowledge records.
* Transformation-loss records.
* Distortion-risk records.
* Mitigation controls.
* Mandatory attribution preservation.
* Origin-permission inheritance.
* Allowed agent actions.
* Prohibited agent actions.
* Human-escalation conditions.
* Data-handling controls.
* Logging requirements.
* Validation test cases.
* Acceptance criteria.
* Validation limitations.
* Controlled deployment states.
* Activation conditions.
* Rollback conditions.
* Operational monitoring requirements.
* Skill lifecycle and governance review.
* Multi-schema validation support.

### Defined

* A skill may bind only to an approved origin.
* Agent-skill transformation must not weaken origin permissions.
* Known information loss must be recorded.
* Known distortion risk must be mitigated.
* Attribution must survive transformation.
* Production deployment does not imply autonomous authority.
* Out-of-scope invocation must be blocked or escalated.
* A skill must be suspended when its origin becomes invalid.
* A downstream skill may be more restrictive than its origin but not less restrictive without separate approval.

### Changed

* Expanded the repository from the Origin layer into the Derivative layer.
* Updated the validation script to validate v0.1 and v0.2 records.

### Not included

* Cross-department runtime execution.
* Runtime decision lineage.
* Human contribution scoring.
* Monetary value calculation.
* Value-return settlement.

---

## [0.1.0] - 2026-07-16

### Enterprise Knowledge Origin Record

Established the foundational Origin layer.

### Added

* Initial repository structure.
* Enterprise Knowledge Origin Record specification.
* JSON Schema Draft 2020-12 implementation.
* Manufacturing knowledge-origin example.
* Enterprise-context fields.
* Organizational and business-unit scope.
* Jurisdiction fields.
* Confidentiality classifications.
* Knowledge-origin identifiers.
* Knowledge-origin types.
* Human contributors.
* Team contributors.
* System contributors.
* Organization contributors.
* Contribution-role records.
* Attribution-mode fields.
* Contributor-consent states.
* Capture-context records.
* Interview capture.
* Direct observation.
* Document extraction.
* System export.
* Agent-assisted capture.
* Knowledge-summary fields.
* Operational scope.
* Decision contexts.
* Known limitations.
* Excluded uses.
* Confidence states.
* Evidence records.
* Evidence-verification states.
* Prior-origin references.
* Integrity metadata.
* Knowledge stewards.
* Usage permissions.
* Attribution requirements.
* Human-review requirements.
* Permitted uses.
* Prohibited uses.
* Retention policies.
* Governance flags.
* Personal-data flags.
* Sensitive-business-information flags.
* Safety-critical flags.
* Regulatory-impact flags.
* Automated-execution permissions.
* Lifecycle states.
* Review states.
* YAML example validation script.
* Initial v0.1–v0.5 roadmap.

### Defined

* Knowledge must be recorded before agent automation begins.
* Contributor attribution must survive downstream transformation.
* Every approved origin must include supporting evidence.
* Operational limitations are part of the knowledge.
* Autonomous-execution permission must be explicit.
* Human-review requirements must be explicit.
* Retired knowledge must remain available for audit and attribution.
* Pseudonymous identity should be used where legal identity is unnecessary.
* Downstream records should reference origin identifiers rather than copying knowledge without provenance.

### Not included

* Agent-skill binding.
* Cross-department execution traces.
* Human contribution scoring.
* Monetary value calculation.
* Value-return allocation.

# Proposed development roadmap

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](docs/INDEX.md). This date identifies the review, not a release or deployment.

The window is **2026-11-19 through 2027-11-18 inclusive** (end-exclusive 2027-11-19): twelve calendar months. Now is the remainder of calendar Q4 2026; Next is Q1 2027; Later is Q2 2027; Horizon spans Q3 and the partial Q4 through November 18. Dates, effort and roles are proposals, not staffing commitments or authorization to change native behavior. The source has no open issues/PRs in the dated complete list observation; these items arise from source findings and evidence gaps.

Categories separate defects, maintenance, documentation, engineering improvements and exploratory research. Dependencies below are within this repository. A shared portfolio documentation checker may be reused after review, but no implemented cross-repository coupling is assumed.

## Now: 2026-11-19 to 2026-12-31

### BT-01 — Close handbook validation coverage

**Documentation; P1.** Proposed owner: Documentation maintainer with CI reviewer. Effort: 1–3 engineer-days. Confidence: High.

**Outcome:** Maintainers detect stale derived content and broken handbook links before merge.

**Proposed change:** Propose a narrow documentation CI gate covering the canonical handbook, generated freshness and citation/schema checks while preserving native tests and required contexts.

**Basis:** [.github/workflows/markdown-maintenance.yml:85–89](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/markdown-maintenance.yml#L85-L89); [.github/workflows/deploy-dashboard.yml:35–54](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/deploy-dashboard.yml#L35-L54).

**Dependencies:** None within this plan.

**Risks:** External link availability can be transient; keep local structural and network failures distinguishable.

**Unresolved assumptions:** Current required check names and branch policies will be inspected before a workflow edit.

**Acceptance criteria:**

- All 24 canonical entry points and their local anchors are checked.
- A deliberately stale handbook and a broken local link each fail the proposed gate.
- Existing model checks, tag coverage and deployment permissions remain intact.

**Verification:** Review the workflow diff and exercise pass/fail fixtures in a task PR; bind results to its exact head.
### BT-02 — Define numerical verification envelopes

**Engineering improvement; P1.** Proposed owner: Thermal modeling reviewer. Effort: 3–6 engineer-days. Confidence: Medium.

**Outcome:** Users can select interval and RK4 steps with declared numerical evidence.

**Proposed change:** Document and test representative stable/unstable affine Euler cases and a nonlinear radiation step-refinement matrix; propose any solver guard separately after compatibility review.

**Basis:** [models/lumped_cell_thermal.py:507–547](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L507-L547); [models/lumped_cell_thermal.py:903–945](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L903-L945); [tests/test_lumped_cell_thermal.py:1619–1697](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L1619-L1697).

**Dependencies:** None within this plan.

**Risks:** A passing example cannot establish an unbounded operating envelope.

**Unresolved assumptions:** Reference cases and acceptable endpoint/event-time errors will be approved before thresholds are called acceptance criteria.

**Acceptance criteria:**

- Record at least three affine feedback/step regimes and three radiation cases with three successively halved internal steps.
- Separate endpoint error, crossing-time error and state-derived bookkeeping residual.
- Publish exact inputs, independent reference construction and the admitted envelope.

**Verification:** Compare affine cases against analytic solutions and nonlinear cases against a reviewed converged reference; preserve failure cases.
### BT-03 — Make lesson provenance maintenance explicit

**Maintenance; P2.** Proposed owner: Documentation maintainer. Effort: 2–4 engineer-days. Confidence: High.

**Outcome:** Readers distinguish historical teaching snapshots from the current source review.

**Proposed change:** Specify a reproducible catalogue/config generation path and an explicit historical/current provenance map without silently changing old source identities.

**Basis:** [docs/native-lessons.json:8–19](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/native-lessons.json#L8-L19); [docs/portfolio/README.md:19–24](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/portfolio/README.md#L19-L24).

**Dependencies:** BT-01.

**Risks:** Blindly refreshing hashes can misattribute historical narratives or examples.

**Unresolved assumptions:** Original generation inputs may need reconstruction; any reconstruction will be labelled.

**Acceptance criteria:**

- Every learning surface exposes its source identity and intended snapshot status.
- A deterministic check detects disagreement between canonical configuration and embedded data.
- All historical badge/workflow markers retain an accountable disposition outside the engineering learning index.

**Verification:** Regenerate twice, compare outputs and source links, and independently inspect representative historical/current passages.

## Next: 2027-01-01 to 2027-03-31

### BT-04 — Establish a measured validation case

**Exploratory research; P1.** Proposed owner: Data/validation steward and thermal reviewer. Effort: 2–6 engineer-weeks. Confidence: Low.

**Outcome:** A specific thermal accuracy claim can be judged against suitable measurements.

**Proposed change:** Select a legally reusable cell dataset or authorized experiment with documented sensor placement, current, ambient/surroundings and parameter sources; separate calibration and validation cases.

**Basis:** [models/README.md:378–403](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L378-L403); [templates/thermal-test-data-quality-checklist.md:1–18](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/templates/thermal-test-data-quality-checklist.md#L1-L18); [references/reading-log-nrel-li-ion-thermal-characterization.md:19–30](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/references/reading-log-nrel-li-ion-thermal-characterization.md#L19-L30).

**Dependencies:** BT-02.

**Risks:** Data access, instrument quality and one-node representativeness may prevent a defensible validation claim.

**Unresolved assumptions:** Dataset license, consent and cell/test conditions are unresolved; no acquisition or experiment is authorized by this proposal alone.

**Acceptance criteria:**

- Publish rights/provenance, units, timestamps, missing-data decisions and sensor uncertainty.
- Declare calibration/held-out cases and error metrics before reporting validation results.
- Report the accepted envelope and mismatches; explicitly defer validation if evidence is unsuitable.

**Verification:** Independent data-quality and method review, then reproducible held-out comparisons under a separately authorized analysis.
### BT-05 — Specify machine-readable threshold assessments

**Engineering improvement; P2.** Proposed owner: Native interface maintainer. Effort: 3–5 engineer-days. Confidence: Medium.

**Outcome:** Automation can interpret upper and lower assessments without confusing process success with a passed threshold.

**Proposed change:** Design a versioned export contract for both assessment types, explicit absent-event semantics and optional exit-policy behavior, preserving existing defaults unless an approved compatibility decision changes them.

**Basis:** [models/lumped_cell_thermal.py:283–394](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L283-L394); [models/lumped_cell_thermal.py:1065–1117](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1065-L1117); [models/lumped_cell_thermal.py:1388–1437](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1388-L1437).

**Dependencies:** BT-02.

**Risks:** Changing exit semantics can break callers; interpolated events can be mistaken for continuous roots.

**Unresolved assumptions:** Consumer requirements and compatibility policy need owner approval.

**Acceptance criteria:**

- Document upper/lower field names, units, strict comparisons and null reasons.
- Include no-violation, initial violation, recovery, repeated-excursion and coarse-sampling examples.
- Record a compatibility decision before adding behavior.

**Verification:** Review the schema/ADR and add contract tests only in a separately scoped implementation PR.
### BT-06 — Map engineering templates to native quantities

**Documentation; P2.** Proposed owner: Thermal documentation reviewer. Effort: 2–4 engineer-days. Confidence: High.

**Outcome:** Template users avoid substituting a surface coefficient or spatial metric into the one-node model.

**Proposed change:** Add an applicability/unit/source map across the broader BTMS templates and a completed synthetic native-case example with explicit N/A spatial outputs.

**Basis:** [templates/thermal-parameter-traceability-matrix.md:5–18](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/templates/thermal-parameter-traceability-matrix.md#L5-L18); [templates/validation-checklist.md:35–41](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/templates/validation-checklist.md#L35-L41); [notes/thermal-assumptions-example-table.md:9–19](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/notes/thermal-assumptions-example-table.md#L9-L19).

**Dependencies:** BT-01.

**Risks:** Over-specializing shared templates could hide their valid broader BTMS purpose.

**Unresolved assumptions:** The broader template scope remains useful and should be preserved.

**Acceptance criteria:**

- Every solver input has a unit, default/override source and project-evidence field.
- W/K and W/(m²·K) mappings require a declared area basis.
- Spatial gradient, conductivity, SOC and electrical capacity are explicitly distinguished from native outputs.

**Verification:** Review a completed example against API declarations and rerun its command with no hidden parameter conversions.

## Later: 2027-04-01 to 2027-06-30

### BT-07 — Correct profile diagnostic line provenance

**Defect; P3.** Proposed owner: Native interface maintainer. Effort: 1–2 engineer-days. Confidence: High.

**Outcome:** CSV timing errors identify the actual source line after comments or blank lines.

**Proposed change:** Add focused failing examples, then propose retaining physical line provenance consistently in timing validation; preserve accepted numeric schedule behavior.

**Basis:** [models/lumped_cell_thermal.py:553–560](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L553-L560); [models/lumped_cell_thermal.py:600–642](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L600-L642); [models/lumped_cell_thermal.py:694–729](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L694-L729).

**Dependencies:** None within this plan.

**Risks:** Changing diagnostic text may affect consumers that parse messages.

**Unresolved assumptions:** Error wording compatibility must be checked; no parser modification is part of this documentation package.

**Acceptance criteria:**

- A gap/overlap and a nonuniform-grid error following comments/blanks report the correct physical line.
- Existing valid profiles and all native regression tests retain their numerical results.

**Verification:** Execute focused diagnostic tests and the full suite in a separately scoped code PR.
### BT-08 — Rehearse recovery and publication

**Maintenance; P2.** Proposed owner: Repository owner and recovery backup. Effort: 1–3 engineer-days. Confidence: Medium.

**Outcome:** An assigned backup can restore the documented model and existing static site with evidence.

**Proposed change:** Assign primary/backup roles and conduct a timed source/docs restore using normal access, current signature/branch rules and the existing Pages route.

**Basis:** [CITATION.cff:5–8](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/CITATION.cff#L5-L8); [.github/workflows/deploy-dashboard.yml:56–82](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/deploy-dashboard.yml#L56-L82); [.gitignore:1–15](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.gitignore#L1-L15).

**Dependencies:** BT-01, BT-03.

**Risks:** Access recovery and protected environments may require platform/account-owner intervention.

**Unresolved assumptions:** No backup assignment or restore target is currently established in source.

**Acceptance criteria:**

- Record assigned roles and an agreed recovery target before the exercise.
- Verify source/tree/fixture hashes, native checks and handbook freshness after restore.
- Tie a permitted publication to its merged revision and inspect live updated content; record elapsed time and failures.

**Verification:** Use a reviewed exercise report with access evidence and deployment lineage; never weaken protection to complete the drill.

## Horizon: 2027-07-01 to 2027-11-18

### BT-09 — Decide the next scientific scope

**Exploratory research; P3.** Proposed owner: Repository owner with thermal/data reviewers. Effort: 1–3 engineer-weeks for decision study. Confidence: Low.

**Outcome:** Future model complexity answers a validated need instead of implying unsupported pack behavior.

**Proposed change:** Evaluate whether a multi-node model, uncertainty propagation or a calibrated parameter map is justified by the measured-case discrepancies; accept, defer or reject each with an ADR.

**Basis:** [models/README.md:378–403](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L378-L403); [notes/thermal-model-limitations.md:7–20](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/notes/thermal-model-limitations.md#L7-L20); [references/research-next-questions-log.md:1–18](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/references/research-next-questions-log.md#L1-L18).

**Dependencies:** BT-04, BT-06.

**Risks:** Added parameters may be unidentifiable; a larger model may obscure rather than reduce uncertainty.

**Unresolved assumptions:** Adequate reusable data and a concrete use case remain unresolved.

**Acceptance criteria:**

- Compare the retained one-node baseline with evidence needs and parameter identifiability.
- Document alternatives, data/license costs, verification strategy and explicit non-goals.
- Record an actual approve/defer/reject decision; implement no expanded model without a separate authorized scope.

**Verification:** Independent review of the decision study, held-out evidence where available and traceable ADR consequences.

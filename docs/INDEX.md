# Documentation index

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](INDEX.md). This date identifies the review, not a release or deployment.

Start with the preserved [native model guide](../models/README.md), then follow the audience routes below. The [static handbook](reference/index.html) is a dated derived view; canonical Markdown/CFF remains authoritative. Existing [interactive thermal lab](index.html), [native catalogue](native-lessons.html), [learning paths](portfolio/index.html) and [animation gallery](animations/index.html) remain available.

- Developers: [setup](developer/SETUP_AND_REPRODUCIBILITY.md) → [interfaces](developer/API_CLI_AND_INTERFACES.md) → [worked examples](developer/WORKED_EXAMPLES_AND_LABS.md).
- Scientific reviewers: [equations](math-and-physics/EQUATIONS_AND_DERIVATIONS.md), [parameters](math-and-physics/PARAMETERS_AND_SYMBOLS.md), [limits](math-and-physics/ASSUMPTIONS_AND_LIMITS.md), and the existing [assumption](../notes/modeling-assumptions.md) / [validation](../templates/validation-checklist.md) materials.
- Maintainers and owners: [evidence](maintainer/VERIFICATION_EVIDENCE_LEDGER.md), [delivery](maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md), [governance](owner/GOVERNANCE_AND_SCOPE.md), [recovery](owner/BUS_FACTOR_RECOVERY_RUNBOOK.md), and [roadmap](../ROADMAP.md).

## Canonical mapping of the 24 required outputs

The existing model guide and substantive notes/templates are preserved. New entry points add current-source contracts and evidence and link to that material; they do not replace it with a second independently maintained feature narrative. CFF is retained verbatim.

| Requested entry point | Canonical purpose |
|---|---|
| [README.md](../README.md) | Existing project narrative plus handbook navigation |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Existing contribution checklist plus documentation maintenance |
| [CHANGELOG.md](../CHANGELOG.md) | Unreleased documentation scope and observed source history |
| [CITATION.cff](../CITATION.cff) | Existing authorship/citation preserved and schema-validated |
| [SECURITY.md](../SECURITY.md) | Observed reporting/access boundaries without invented contacts |
| [ROADMAP.md](../ROADMAP.md) | Nine evidence-backed proposed items over twelve calendar months |
| [docs/INDEX.md](INDEX.md) | Canonical mapping and audience routes |
| [docs/developer/ARCHITECTURE.md](developer/ARCHITECTURE.md) | Native/browser/data/publication boundaries |
| [docs/developer/SETUP_AND_REPRODUCIBILITY.md](developer/SETUP_AND_REPRODUCIBILITY.md) | Source checkout, environment and reproducible commands |
| [docs/developer/API_CLI_AND_INTERFACES.md](developer/API_CLI_AND_INTERFACES.md) | Native entry points, CLI, input/export contracts |
| [docs/developer/WORKED_EXAMPLES_AND_LABS.md](developer/WORKED_EXAMPLES_AND_LABS.md) | Executed source-specific laboratories |
| [docs/developer/TROUBLESHOOTING.md](developer/TROUBLESHOOTING.md) | Source-based symptoms and practical diagnosis |
| [docs/math-and-physics/EQUATIONS_AND_DERIVATIONS.md](math-and-physics/EQUATIONS_AND_DERIVATIONS.md) | Balance, exact/Euler/RK4 and reporting derivations |
| [docs/math-and-physics/PARAMETERS_AND_SYMBOLS.md](math-and-physics/PARAMETERS_AND_SYMBOLS.md) | Defaults, units, signs and template mapping |
| [docs/math-and-physics/ASSUMPTIONS_AND_LIMITS.md](math-and-physics/ASSUMPTIONS_AND_LIMITS.md) | Validity envelope and unestablished claims |
| [docs/maintainer/VERIFICATION_EVIDENCE_LEDGER.md](maintainer/VERIFICATION_EVIDENCE_LEDGER.md) | Observed checks, source criteria and revision limits |
| [docs/maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md](maintainer/CI_CD_AND_RELEASE_PLAYBOOK.md) | Actual workflows and guarded existing publication |
| [docs/maintainer/TOOLCHAIN_AND_DEPENDENCY_MATRIX.md](maintainer/TOOLCHAIN_AND_DEPENDENCY_MATRIX.md) | Declared/tested tools and license/data boundaries |
| [docs/maintainer/FAILURE_MODES_AND_TECH_DEBT.md](maintainer/FAILURE_MODES_AND_TECH_DEBT.md) | Evidence-backed discrepancies and proposals |
| [docs/maintainer/DOCS_MAINTENANCE_RUNBOOK.md](maintainer/DOCS_MAINTENANCE_RUNBOOK.md) | Canonical updates, reproducible renderer and drift checks |
| [docs/owner/ADR/ADR-0000-INDEX.md](owner/ADR/ADR-0000-INDEX.md) | Reconstructed observations, not historical approvals |
| [docs/owner/GOVERNANCE_AND_SCOPE.md](owner/GOVERNANCE_AND_SCOPE.md) | Documented author and proposed responsibilities |
| [docs/owner/BUS_FACTOR_RECOVERY_RUNBOOK.md](owner/BUS_FACTOR_RECOVERY_RUNBOOK.md) | Concrete source/docs/access restoration |
| [docs/owner/PORTFOLIO_INTEGRATION.md](owner/PORTFOLIO_INTEGRATION.md) | Public interface boundaries and qualified future connections |

## Supporting reference material

- [Native API reference](developer/API_REFERENCE.md): every public declaration, annotated dataclass field and constant.
- [Browser model/control inventory](developer/BROWSER_MODEL_CATALOG.md): active thermal model, all bundled kinds and UI/storage/export boundaries.
- [Source evidence and coverage](SOURCE_EVIDENCE.md): pinned locators, complete tree accounting and explicit indexed-only limits.
- Existing [heat-source selection](../notes/heat-generation-model-selection.md), [thermal limitations](../notes/thermal-model-limitations.md), [parameter traceability](../templates/thermal-parameter-traceability-matrix.md), [source checklist](../templates/btms-source-checklist.md) and [NREL reading log](../references/reading-log-nrel-li-ion-thermal-characterization.md).

The review distinguishes software verification, synthetic teaching results, measured validation and live publication. The source contains no measured-cell validation package, and an exceeded teaching threshold is not a safety recommendation.

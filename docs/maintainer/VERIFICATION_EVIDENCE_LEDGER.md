# Verification evidence ledger

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

**Review identity:** native source `37cb3c16069b21c373efc17ed202352ab69224dd`, observed 2026-11-19 on Python 3.12.14/Linux. Native checks ran in an isolated copy with unchanged source bytes. Documentation checks bind to a separately recorded candidate tree fingerprint. Final documentation commit, PR checks, merge SHA and deployment identity belong in the external delivery record; none is implied by this source review.

## Observed local executions

| Evidence | Command / criterion | Result and limit |
|---|---|---|
| Native regression suite | `python -m unittest discover -s tests -v` | 85 tests passed; synthetic/analytic software verification |
| CLI registration | `python models/lumped_cell_thermal.py --help` | Successful; 23 explicit long options plus automatic help |
| Constant reference | 75 A, 600 s, Euler 1 s versus exact-linear 600 s | 34.309 versus 34.305 °C rounded final output |
| Seven committed input CSVs | Methods/settings in [worked examples](../developer/WORKED_EXAMPLES_AND_LABS.md) | All seven CLI runs succeeded and exported interval records |
| Upper/lower assessment | Upper 30/35 °C, lower 20 °C on default run | 30 exceeded; 35 and lower 20 passed; process exit 0 |
| Source-linked guide | `python scripts/portfolio/validate_guide.py` | Four paths validated; validates structure/source links, not native execution |
| Active browser equations | Evaluate exact inline UMD and declared module presets/checkpoints | All eight thermal checkpoints passed; no DOM/visual claim |

Input and implementation references: [models/lumped_cell_thermal.py:1120–1437](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1120-L1437); [scripts/portfolio/validate_guide.py:1–33](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/scripts/portfolio/validate_guide.py#L1-L33); [docs/index.html:147–335](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L147-L335). Full commands, timestamps, environment, input/output/log hashes and exact fingerprints are retained with the review handoff.

## What the source tests actually assert

| Claim | Existing test locations | Criterion |
|---|---|---|
| Equilibrium and Euler recurrence | [tests/test_lumped_cell_thermal.py:289–317](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L289-L317) | Exact zero-current equilibrium; final recurrence agreement to 10 decimal places |
| Affine analytic solution | [tests/test_lumped_cell_thermal.py:319–398](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L319-L398) | Analytic endpoint comparisons to 12 decimal places, including zero feedback slope |
| Bookkeeping is not accuracy | [tests/test_lumped_cell_thermal.py:400–441](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L400-L441) | Two Euler resolutions both have zero bookkeeping residual despite different nonzero analytic errors |
| External/reversible heat and cooling | [tests/test_lumped_cell_thermal.py:459–613](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L459-L613) | Closed forms, sign reversal and interval override checks |
| Step sensitivity | [tests/test_lumped_cell_thermal.py:667–674](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L667-L674) | Default 1 s and 0.5 s Euler finals differ by <0.01 °C; one scenario only |
| CSV/boundary contracts | [tests/test_lumped_cell_thermal.py:721–1119](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L721-L1119) | Uniform/variable timing, comments/BOM/header rules, boundaries, validation and export values |
| CLI and conflict resolution | [tests/test_lumped_cell_thermal.py:1122–1535](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L1122-L1535) | Output records, advertised methods and conflicting constant/profile inputs |
| Radiation / RK4 | [tests/test_lumped_cell_thermal.py:1537–1764](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L1537-L1764) | Radiation sign and components; radiation-disabled RK4/exact endpoint agreement to 11 decimal places |
| Upper and lower exposure | [tests/test_lumped_cell_thermal.py:27–287](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L27-L287) | Hand-constructed crossing/exposure values, equality semantics, reports and CLI |

Decimal-place comparisons are the unittest criteria used by these examples, not universal engineering tolerances. The nonlinear radiation tests exercise signs and bookkeeping; they do not provide a measured-data comparison or exhaustive error-convergence proof.

## Documentation and delivery checks

The author checks the complete pinned tree and blob hashes, authorized diff, all 24 entry points, CFF against its declared official 1.2.0 schema, local Markdown/HTML links and anchors, source-locator bounds, JSON schemas, SVG XML, CSV structure, roadmap fields/dependencies, public interface accounting and deterministic handbook freshness. Those checks cannot replace independent scientific/content review. External URLs are indexed; universal network reachability is not claimed.

At source-head observation, GitHub checks `deploy`, `validate` and `human-authorship-policy` were successful for the source SHA. The two Pages jobs belong to workflow run [43747906426](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/actions/runs/43747906426); the metadata policy belongs to [43747906359](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/actions/runs/43747906359). These historical checks do not establish candidate native CI, approval, merge or updated Pages content.

Measured-cell validation, full GUI/accessibility/browser inspection and publication verification are **not established by the author-side local checks**. The existing page/config snapshots remain historical; current live delivery must be tied to the merged revision and inspected separately.

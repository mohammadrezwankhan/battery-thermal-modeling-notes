# Source evidence and coverage boundaries

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](INDEX.md). This date identifies the review, not a release or deployment.

The immutable input is source `37cb3c16069b21c373efc17ed202352ab69224dd`, Git tree `127037ea757181c6baa8db8290d2f978838dd636`. The complete recursive tree contains **751 entries: 718 blobs and 33 directories**. All 718 payloads are available, UTF-8 text and verified against their pinned Git blob identities. Full accounting is not full semantic or visual certification.

Review dispositions are **69 analyzed** and **682 indexed only**. The complete native engine, native tests, substantive model guide/notes/templates/references, workflow contracts, relevant browser logic and primary configuration were inspected. The 598 historical badge/workflow markers (573 TXT and 25 Markdown) were payload-read and classified through six normalized forms, but remain indexed historical evidence rather than engineering content or a current-achievement claim. SVG/CSS presentation assets and generated catalogues retain bounded structural/provenance inspection.

There are **four Python files**, 121 AST definitions across native code/tests, **30 public native declarations**, **70 dataclass fields**, **two constants**, **23 explicitly registered CLI options**, seven illustrative CSVs, 43 SVGs, eight JSON files and five HTML pages. No notebooks, binary payloads, symlinks, submodules or LFS pointers were found in this canonical tree. Public API coverage is separately recorded from file coverage.

## Claim-to-source map

| Claim / object | Immutable source locator |
|---|---|
| Parameter defaults/validation | [models/lumped_cell_thermal.py:17–119](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L17-L119) |
| Heat signs and radiation | [models/lumped_cell_thermal.py:130–185](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L130-L185) |
| State-derived energy | [models/lumped_cell_thermal.py:247–277](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L247-L277) |
| Upper/lower assessments | [models/lumped_cell_thermal.py:283–394](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L283-L394) |
| RK4 integration | [models/lumped_cell_thermal.py:507–547](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L507-L547) |
| Strict profile contract | [models/lumped_cell_thermal.py:550–747](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L550-L747) |
| Scheduled inputs / integrators | [models/lumped_cell_thermal.py:750–993](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L750-L993) |
| CSV exports | [models/lumped_cell_thermal.py:996–1117](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L996-L1117) |
| CLI registration / dispatch | [models/lumped_cell_thermal.py:1120–1437](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1120-L1437) |
| Native tests | [tests/test_lumped_cell_thermal.py:1–1768](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L1-L1768) |
| Preserved model narrative | [models/README.md:1–403](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L1-L403) |
| Active thermal browser model | [docs/index.html:167–172](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L167-L172) |
| Pure browser API implementation | [docs/index.html:231–335](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L231-L335) |
| Native catalogue provenance | [docs/native-lessons.json:8–19](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/native-lessons.json#L8-L19) |
| Model and Markdown CI | [.github/workflows/markdown-maintenance.yml:1–89](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/markdown-maintenance.yml#L1-L89) |
| Existing Pages route | [.github/workflows/deploy-dashboard.yml:1–82](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/deploy-dashboard.yml#L1-L82) |
| Template applicability | [templates/thermal-parameter-traceability-matrix.md:1–18](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/templates/thermal-parameter-traceability-matrix.md#L1-L18) |

## Input fixtures

| File | Rows / elapsed seconds | Source |
|---|---:|---|
| `ambient_step_current_profile.csv` | 6 / 360 | [models/data/ambient_step_current_profile.csv:1–7](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/ambient_step_current_profile.csv#L1-L7) |
| `external_heat_profile.csv` | 3 / 300 | [models/data/external_heat_profile.csv:1–4](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/external_heat_profile.csv#L1-L4) |
| `irregular_current_profile.csv` | 4 / 180 | [models/data/irregular_current_profile.csv:1–5](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/irregular_current_profile.csv#L1-L5) |
| `pulse_current_profile.csv` | 10 / 600 | [models/data/pulse_current_profile.csv:1–11](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/pulse_current_profile.csv#L1-L11) |
| `radiative_cooling_profile.csv` | 4 / 1800 | [models/data/radiative_cooling_profile.csv:1–5](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/radiative_cooling_profile.csv#L1-L5) |
| `reversible_heat_current_profile.csv` | 4 / 360 | [models/data/reversible_heat_current_profile.csv:1–5](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/reversible_heat_current_profile.csv#L1-L5) |
| `variable_cooling_profile.csv` | 5 / 1800 | [models/data/variable_cooling_profile.csv:1–6](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/data/variable_cooling_profile.csv#L1-L6) |

All 36 fixture data rows were read and run using the documented methods. They prescribe currents and boundaries; no measured provenance is inferred. No simulation result bundle is committed at this source; local run outputs and hashes remain in the external review record.

## Metadata and evidence limits

On 2026-11-19, read-only GitHub observations found main at the reviewed source, three completed successful source-head check runs, and empty release, tag-ref, open-PR, open-issue and legacy-status lists. Paginated list requests used 100 entries per page and returned short/empty complete first pages; the checks total was three and all three were returned. The rulesets list contained one active ruleset, whose detail required signatures on all branches without bypass actors. Classic branch-protection read access returned an integration permission error; current delivery must resolve that gate through an authorized supported route.

The public repository metadata declares GitHub Pages and its homepage, and the tracked workflow supplies a publication route. Neither observation proves delivery of this new documentation. The author performed no remote mutation and does not claim live publication, full GUI verification, measurement validation or present-day badge status.

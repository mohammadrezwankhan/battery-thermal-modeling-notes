# Battery Thermal Modeling Notes

[![Model and Markdown validation](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/actions/workflows/markdown-maintenance.yml/badge.svg)](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/actions/workflows/markdown-maintenance.yml)

Research-backed notes and reproducible examples for battery thermal behavior,
BTMS design thinking, and validation assumptions.

## Focus Areas

- Battery heat generation and thermal pathways.
- BTMS architecture comparison.
- Model assumptions and boundary conditions.
- Validation checklists for simulation claims.
- Reading notes from public literature.

## Starter Notes

- [Executable lumped cell thermal reference](models/README.md)

- [Battery thermal modeling assumptions](notes/modeling-assumptions.md)
- [BTMS architecture comparison](notes/btms-architecture-comparison.md)
- [Heat-generation model selection](notes/heat-generation-model-selection.md)
- [Thermal model limitations](notes/thermal-model-limitations.md)
- [Thermal source confidence guide](notes/thermal-source-confidence-guide.md)
- [Thermal assumptions example table](notes/thermal-assumptions-example-table.md)
- [Thermal validation example result summary](notes/thermal-validation-example-result-summary.md)
- [Battery thermal validation checklist](templates/validation-checklist.md)
- [BTMS source checklist](templates/btms-source-checklist.md)
- [Thermal validation decision log](templates/thermal-validation-decision-log.md)
- [Thermal parameter traceability matrix](templates/thermal-parameter-traceability-matrix.md)
- [Reading log template](references/reading-log-template.md)
- [Reading log: NREL Li-ion thermal characterization](references/reading-log-nrel-li-ion-thermal-characterization.md)

- [Cooling Loop Assumption Register](templates/cooling-loop-assumption-register.md)

- [Thermal Test Data Quality Checklist](templates/thermal-test-data-quality-checklist.md)

- [Cell To Pack Scaling Note](notes/cell-to-pack-scaling-note.md)

- [Ambient Boundary Condition Log](templates/ambient-boundary-condition-log.md)

- [Sensor Placement Review Template](templates/sensor-placement-review-template.md)

- [Thermal Runaway Scope Boundary](notes/thermal-runaway-scope-boundary.md)

- [BTMS Control Assumption Table](templates/btms-control-assumption-table.md)

- [Heat Rejection Pathway Map](notes/heat-rejection-pathway-map.md)

- [Validation Metric Selection Guide](notes/validation-metric-selection-guide.md)

- [Uncertainty Review Checklist](templates/uncertainty-review-checklist.md)

- [Literature Claim Extraction Template](references/literature-claim-extraction-template.md)

- [Experimental Condition Comparison](templates/experimental-condition-comparison.md)

- [Thermal Model Change Log](templates/thermal-model-change-log.md)

- [Material Property Source Register](templates/material-property-source-register.md)

- [Transient Vs Steady State Guide](notes/transient-vs-steady-state-guide.md)

- [Cooling Strategy Trade Study](notes/cooling-strategy-trade-study.md)

- [Temperature Limit Rationale Note](notes/temperature-limit-rationale-note.md)

- [Data Gap Triage Checklist](templates/data-gap-triage-checklist.md)

- [Validation Readiness Review](templates/validation-readiness-review.md)

- [Research Next Questions Log](references/research-next-questions-log.md)

## Repository Topics

```text
battery thermal-management btms bms electric-vehicles matlab simulink
research-notes battery-modeling
```

## Suggested Structure

```text
notes/
models/
figures/
references/
README.md
CONTRIBUTING.md
LICENSE
```

## Run The Executable Reference

The dependency-free lumped model implements irreversible `I^2 R` heating,
linear heat rejection, and a discrete energy-balance diagnostic:

```powershell
python models/lumped_cell_thermal.py --current-a 75 --duration-s 600
python models/lumped_cell_thermal.py `
  --profile-csv models/data/pulse_current_profile.csv `
  --output-csv results/pulse_thermal_intervals.csv
python models/lumped_cell_thermal.py `
  --profile-csv models/data/ambient_step_current_profile.csv `
  --output-csv results/ambient_step_thermal_intervals.csv
python -m unittest discover -s tests -v
```

See the [model assumptions and limitations](models/README.md) before adapting
the parameters or using the output in an engineering review. The profile path
supports traceable charge/discharge duty cycles, optional interval ambient
temperature, and interval-level CSV results.

## Contribution Entry Points

- Add a public reading-log entry.
- Extend the BTMS architecture comparison with source-backed examples.
- Add source-backed examples to the heat-generation model selection note.
- Add mitigation examples to the thermal model limitations note.
- Add source ranking examples to the thermal source confidence guide.
- Adapt the thermal assumptions example table for a sourced case study.
- Replace the thermal validation example summary with a sourced case study.
- Add source-backed BTMS claim examples to the BTMS source checklist.
- Improve validation checklist wording with units and boundary conditions.
- Add real project decisions to the thermal validation decision log.
- Add project-specific examples to the thermal parameter traceability matrix.
- Add project-specific examples to the cooling loop assumption register.
- Add project-specific examples to the thermal test data quality checklist.
- Add project-specific examples to the cell to pack scaling note.
- Add project-specific examples to the ambient boundary condition log.
- Add project-specific examples to the sensor placement review template.
- Add project-specific examples to the thermal runaway scope boundary.
- Add project-specific examples to the btms control assumption table.
- Add project-specific examples to the heat rejection pathway map.
- Add project-specific examples to the validation metric selection guide.
- Add project-specific examples to the uncertainty review checklist.
- Add project-specific examples to the literature claim extraction template.
- Add project-specific examples to the experimental condition comparison.
- Add project-specific examples to the thermal model change log.
- Add project-specific examples to the material property source register.
- Add project-specific examples to the transient vs steady state guide.
- Add project-specific examples to the cooling strategy trade study.
- Add project-specific examples to the temperature limit rationale note.
- Add project-specific examples to the data gap triage checklist.
- Add project-specific examples to the validation readiness review.
- Add project-specific examples to the research next questions log.

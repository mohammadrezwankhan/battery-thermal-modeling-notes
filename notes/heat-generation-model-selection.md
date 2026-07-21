# Heat-Generation Model Selection

Battery thermal models should use the simplest heat-generation representation that can answer the engineering question without hiding important operating-condition effects.

## Comparison

| Approach | Typical Form | Best Use | Limits To Document |
|---|---|---|---|
| Simple ohmic loss | `Q_dot = I^2 * R` | Early sizing, quick sensitivity checks, education examples. | Resistance value, temperature range, SOC range, pulse duration, and whether charge/discharge asymmetry is ignored. |
| OCV / entropy-aware heat | Combines irreversible loss with reversible heat such as `-I * T * dU_oc/dT` for the stated positive-discharge convention. | Studies where SOC, temperature, or charge/discharge direction changes the thermal response. | Source of OCV curve, source of entropy coefficient, interpolation method, current direction, and sign convention. |
| Measured or calorimetry-informed heat | Heat map or fitted model from measured cell behavior. | Design reviews, validation packs, high-power duty cycles, and thermal-management decisions. | Test conditions, cell age, C-rate range, temperature range, measurement uncertainty, and scaling from cell to module or pack. |

## Selection Guide

| Project Question | Suggested Starting Point | Upgrade Trigger |
|---|---|---|
| Rough pack heat-rejection estimate | Simple ohmic loss | Temperature rise or duty cycle is close to design limit. |
| Compare charge and discharge pulses | OCV / entropy-aware heat | Reversible heat changes the predicted temperature trend. |
| Validate BTMS architecture | Measured or calorimetry-informed heat | Model output supports hardware selection, warranty claims, or safety evidence. |
| Communicate assumptions to non-specialists | Simple table plus sensitivity range | Reviewers ask whether the assumed heat source is measured, fitted, or guessed. |

## Project Review Checklist

- What current profile is being converted into heat: continuous, pulse, drive cycle, grid-support event, or abuse case?
- Is resistance treated as constant, SOC-dependent, temperature-dependent, or age-dependent?
- Does the model include reversible heat, and is the sign convention stated?
- Are interconnect, busbar, contactor, coolant pump, or auxiliary heat sources included or intentionally excluded?
- Does the validation dataset cover the same C-rate, SOC, temperature, and cooling boundary condition used in the model?
- Is the heat-generation assumption traceable to a datasheet, public source, lab measurement, or clearly marked placeholder?

## Practical Rule

Use a simple model for learning and quick screening. Move to condition-dependent or measured heat-generation inputs when the result affects BTMS architecture, safety margin, warranty discussion, or commissioning evidence.

The executable reference demonstrates the reversible term with a constant or
piecewise-constant coefficient. The underlying equation is documented in the
[NREL Li-Ion Battery Thermal Characterization paper](https://www.osti.gov/biblio/2349292).
Use measured coefficients over the applicable SOC and temperature range before
interpreting the term as cell-specific behavior.

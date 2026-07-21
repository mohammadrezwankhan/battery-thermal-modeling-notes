# Thermal Model Limitations

Early-stage battery thermal models are useful for learning, screening, and review conversations, but their limits should be stated before results are used for design decisions.

| Limitation | Potential Impact | Mitigation |
|---|---|---|
| Placeholder heat source | A simple `I^2 * R` estimate can miss reversible heat, temperature dependence, and operating-condition effects. | Mark the heat source as placeholder and replace with measured, fitted, or literature-backed inputs when results drive design. |
| Contact resistance omitted | Cell-to-module, module-to-plate, or interface gaps can create gradients that the model does not predict. | Add contact assumptions or sensitivity cases when gradients matter. |
| Aging not represented | Resistance, capacity, and heat generation may shift as the cell ages. | State age/SOH assumptions and avoid using fresh-cell values for lifetime claims. |
| Thermal boundary assumptions too narrow | A single convection ambient or radiative-surroundings value can hide hot-day, cold-start, enclosure, or ventilation limits. | Run independent ambient and radiative-surroundings sensitivity cases or define the approved operating ranges. |
| Cooling boundary simplified | Prescribed convection and diffuse-gray surface radiation can overstate thermal performance and miss actuator, fluid, enclosure, or view-factor effects. | Document airflow, coolant, inlet and radiative-surroundings temperatures, heat-transfer coefficient, emissivity, area, and evidence sources; run bounded schedules when staged cooling matters. |
| Module/pack scaling simplified | Cell-level heat results may not capture interconnects, busbars, spacing, or enclosure behavior. | State scaling assumptions and add module or pack evidence before design review. |
| Validation gap | A visually plausible plot may not match measured pulse, calorimetry, or datasheet behavior. | Include validation reference, confidence level, and known mismatch. |
| Solver/time-step sensitivity | Coarse time steps can hide transient peaks or numerical instability. | Report solver, time step, and convergence or sensitivity checks. |

## Review Rule

Use early-stage models to explain assumptions and compare trends. Use validated, condition-aware models before making claims about BTMS sizing, safety margin, warranty behavior, or operating limits.

## Documentation Prompt

```text
This result is an early-stage estimate using [heat source], [cooling boundary], and [validation reference]. Known limitations are [limitations], so conclusions are limited to [screening/design/review purpose].
```

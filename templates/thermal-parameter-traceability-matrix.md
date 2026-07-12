# Thermal Parameter Traceability Matrix

Use this matrix to track where thermal parameters came from and how they affect validation confidence.

| Parameter | Unit | Source | Reference Condition | Validation Impact | Owner |
|---|---|---|---|---|---|
| Cell heat capacity | J/K or J/kg-K | Test data, supplier data, or literature | Temperature range and SOC window | High if transient temperature rise is compared | Modeling owner |
| Thermal conductivity | W/m-K | Material datasheet or measured estimate | Direction and compression state | Medium to high for spatial gradients | Thermal lead |
| Convective coefficient | W/m2-K | Test correlation, CFD, or estimate | Air or coolant flow condition | High for cooling-system comparisons | Reviewer |
| Internal resistance | ohm | Pulse test, datasheet, or model fit | SOC, temperature, and C-rate | High for heat-generation estimates | Battery engineer |
| Ambient temperature | degC | Test log or scenario assumption | Test chamber, room, or field condition | Medium for boundary sensitivity | Validation owner |

## Review Prompts

- Which parameter has the weakest source but the largest effect on the result?
- Are units and reference conditions written close enough to prevent reuse mistakes?
- Which values are educational placeholders rather than validated project values?
- Who can approve changing the parameter after a validation result is published?

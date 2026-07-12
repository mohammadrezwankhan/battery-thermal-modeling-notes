# Battery Thermal Modeling Assumptions

This note captures assumptions that should be stated before presenting battery thermal simulation results.

## Cell-Level Assumptions

| Assumption | Why It Matters | Example Evidence |
|---|---|---|
| Cell format | Geometry affects surface area, heat path, and thermal gradients | Datasheet or measured dimensions |
| Heat generation model | Determines thermal source term and transient behavior | Joule heat, entropic heat, or empirical fit |
| Internal resistance | Strongly affects heat at high current | Datasheet curve or test-derived value |
| Initial temperature | Changes transient response and safety interpretation | Test condition or ambient measurement |
| State of charge window | Resistance and thermal behavior vary by SOC | SOC range and estimation method |

## Pack/System Assumptions

| Assumption | Why It Matters | Example Evidence |
|---|---|---|
| Cooling strategy | Air/liquid/passive cooling changes boundary conditions | BTMS architecture description |
| Contact resistance | Interface quality affects thermal spreading | Material stack-up or test correlation |
| Ambient condition | Temperature and airflow drive heat rejection | Environmental test condition |
| Duty cycle | Load profile determines heat generation over time | Drive cycle, grid dispatch, or test pulse |

## Reporting Standard

Every model result should report:

- Units.
- Initial conditions.
- Boundary conditions.
- Heat generation method.
- Solver/settings if relevant.
- Validation data or limits of confidence.

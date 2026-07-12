# Thermal Assumptions Example Table

Use this table as a compact example for documenting battery thermal model assumptions before sharing plots, simulation results, or design claims.

## Example Assumptions

| Category | Assumption | Placeholder Value | Unit | Why It Matters |
|---|---|---|---|---|
| Cell format | Prismatic Li-ion cell | 50 Ah nominal | Ah | Capacity affects C-rate conversion and heat scaling. |
| Initial SOC | Starting state of charge | 80 | % | SOC can affect open-circuit voltage, resistance, and reversible heat. |
| Ambient condition | Initial ambient temperature | 25 | degC | Defines starting point for thermal rise and cooling calculations. |
| Module layout | Cells per module | 12 | cells | Scaling from cell heat to module heat depends on layout. |
| Cooling mode | Forced air across module face | 2.0 | m/s | Cooling assumption drives surface heat transfer and temperature spread. |
| Heat source | Lumped ohmic heat estimate | `I^2 * R` | W | Simple placeholder until measured or condition-dependent heat data is available. |
| Thermal boundary | Convection coefficient | 15 | W/m^2-K | Strongly influences predicted steady-state temperature. |
| Contact assumption | Cell-to-frame contact resistance | Not modeled | - | Contact assumptions should be stated when gradients matter. |
| Validation reference | Pulse test or literature benchmark | TBD | - | Results should be tied to test data, datasheet behavior, or public literature. |

## Review Prompts

- Are units stated for every value that enters a calculation?
- Are SOC, C-rate, and ambient ranges aligned with the intended duty cycle?
- Is the heat source measured, fitted, estimated from resistance, or marked as a placeholder?
- Does the cooling boundary reflect the actual module or pack arrangement?
- Are excluded effects documented, such as interconnect heat, contact resistance, or aging?

## Reuse Note

Treat the placeholder values as examples only. Replace them with project, datasheet, lab, or literature-backed assumptions before using the table in a design review.

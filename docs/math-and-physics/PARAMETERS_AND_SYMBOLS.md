# Parameters, symbols and units

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

All native defaults below are educational placeholders, except mathematical/unit constants. There is no named-cell calibration dataset in the reviewed source. Use the existing [thermal parameter traceability matrix](../../templates/thermal-parameter-traceability-matrix.md) and [material property register](../../templates/material-property-source-register.md) to record a replacement's source, condition, uncertainty and owner. [models/README.md:378–403](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L378-L403).

| Native field / symbol here | Default | Unit | Admitted meaning |
|---|---:|---|---|
| `mass_kg`, $m$ | 1.05 | kg | Positive lumped mass |
| `specific_heat_j_per_kg_k`, $c_p$ | 1000 | J/(kg·K) | Positive constant specific heat |
| `thermal_capacity_j_per_k`, $C=mc_p$ | 1050 derived | J/K | Effective node heat capacity |
| `resistance_ohm`, $R_0$ | 0.004 | Ω | Nonnegative reference resistance |
| `resistance_temperature_coefficient_per_k`, $\alpha_R$ | 0 | K⁻¹ | Finite linear coefficient; evaluated resistance must stay nonnegative |
| `resistance_reference_temperature_c`, $T_{ref}$ | 25 | °C | Reference for the linear correction |
| `entropic_coefficient_v_per_k`, $\beta$ | 0 | V/K | Signed prescribed entropy coefficient |
| `external_heat_w`, $Q_{ext}$ | 0 | W | Signed prescribed heat into the node |
| `heat_transfer_w_per_k`, $G$ | 1.2 | W/K | Nonnegative effective convection conductance |
| `emissivity`, $\epsilon$ | 0 | dimensionless | 0–1; paired with area |
| `radiating_area_m2`, $A$ | 0 | m² | Nonnegative radiating area |
| `ambient_temperature_c`, $T_a$ | 25 | °C | Convection boundary |
| `radiative_surroundings_temperature_c`, $T_s$ | `None` → ambient | °C | Independent radiative boundary when supplied |
| `initial_temperature_c`, $T_0$ | 25 | °C | Single initial state |
| `time_step_s`, $\Delta t$ | 1 | s | Positive default outer interval duration |
| `rk4_max_step_s`, $\Delta t_{max}$ | 1 | s | Positive maximum internal RK4 step |
| `integration_method` | `explicit-euler` | enum/string | `explicit-euler`, `exact-linear`, `rk4` |

Declarations and validation: [models/lumped_cell_thermal.py:17–119](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L17-L119). Schedule arrays can override ambient, surroundings, interval duration, entropy coefficient, external heat and conductance. Currents are finite signed amperes; all supplied temperatures must exceed absolute zero. [models/lumped_cell_thermal.py:750–861](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L750-L861).

## Avoid unit collisions

The native name “heat transfer” denotes **conductance G in W/K**. Some existing templates discuss a surface convection coefficient in W/(m²·K); a justified area relation such as $G=hA$ is required before substitution. `radiating_area_m2` belongs only to the radiation term and is not silently multiplied into native convection. Thermal conductivity in W/(m·K), C-rate, cell capacity in Ah and spatial gradients appear in broader templates but are not native solver inputs/outputs. [templates/thermal-parameter-traceability-matrix.md:5–11](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/templates/thermal-parameter-traceability-matrix.md#L5-L11); [notes/thermal-assumptions-example-table.md:9–19](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/notes/thermal-assumptions-example-table.md#L9-L19); [models/lumped_cell_thermal.py:486–503](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L486-L503).

Temperature differences in °C equal differences in K, but reversible heat and fourth-power radiation use absolute kelvin. `ABSOLUTE_ZERO_C=-273.15`; `STEFAN_BOLTZMANN_W_PER_M2_K4=5.670374419e-8` W/(m²·K⁴). Current is positive discharge and negative charge; `external_heat_w<0` removes heat. Resistance is evaluated at every derivative/endpoint used by the solver. [models/lumped_cell_thermal.py:13–14](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L13-L14); [models/lumped_cell_thermal.py:130–185](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L130-L185); [models/lumped_cell_thermal.py:460–504](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L460-L504); [models/lumped_cell_thermal.py:947–951](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L947-L951).

## Output and browser conventions

Native energies are J, rates W, time seconds, temperatures °C, exposure fractions dimensionless 0–1, and margins °C. The CLI formats exposure as a percentage. `ThermalSimulation.time_step_s` may be `None` for a variable grid. A reported peak/minimum uses the stored state tuple, not unreported RK4 stages. The API catalogue lists every result field. [models/lumped_cell_thermal.py:188–457](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L188-L457); [models/lumped_cell_thermal.py:1405–1431](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1405-L1431).

Browser controls are Q=1200 W (100–3000), G=40 W/K (10–120), C=18000 J/K (3000–60000) and ambient=25 °C (0–45). It displays time in minutes and energy above ambient in kJ; its parameters are not the native default cell. Its `residualW` is net heat rate, not a numerical residual or native energy bookkeeping error. [docs/index.html:167–172](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L167-L172); [docs/index.html:257–259](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L257-L259).

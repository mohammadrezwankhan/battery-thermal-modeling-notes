# Native API reference

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

Import these names from `models.lumped_cell_thermal`. This catalogue is generated from the reviewed Python AST and checked against the source; it accounts for all 30 public class/function/property declarations and 70 annotated dataclass fields. Arguments are positional-or-keyword; listed defaults make them optional. Read-only `@property` entries are accessed as attributes. Six dataclasses are frozen. Direct construction of result records is possible but does not validate array lengths; use the loader/simulator for consistent records. See [API/CLI contracts](API_CLI_AND_INTERFACES.md) for units, shapes, exceptions and file semantics.

## Constants

- `ABSOLUTE_ZERO_C = -273.15` — [models/lumped_cell_thermal.py:13–13](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L13-L13).
- `STEFAN_BOLTZMANN_W_PER_M2_K4 = 5.670374419e-08` — [models/lumped_cell_thermal.py:14–14](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L14-L14).

## `IntegrationMethod`

Three supported method values: explicit Euler, affine exact-linear and bounded-step RK4.

[models/lumped_cell_thermal.py:17–20](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L17-L20).

Declaration / dataclass field signature:

```python
IntegrationMethod
```

| Member | Value |
|---|---|
| `EXPLICIT_EULER` | `'explicit-euler'` |
| `EXACT_LINEAR` | `'exact-linear'` |
| `RK4` | `'rk4'` |

## `LumpedThermalSpec`

Frozen parameter record. Construction stores values; call validate or run the simulator to enforce parameter constraints.

[models/lumped_cell_thermal.py:23–185](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L23-L185).

Declaration / dataclass field signature:

```python
LumpedThermalSpec(mass_kg: float = 1.05, specific_heat_j_per_kg_k: float = 1000.0, resistance_ohm: float = 0.004, resistance_temperature_coefficient_per_k: float = 0.0, resistance_reference_temperature_c: float = 25.0, entropic_coefficient_v_per_k: float = 0.0, external_heat_w: float = 0.0, heat_transfer_w_per_k: float = 1.2, emissivity: float = 0.0, radiating_area_m2: float = 0.0, ambient_temperature_c: float = 25.0, radiative_surroundings_temperature_c: float | None = None, initial_temperature_c: float = 25.0, time_step_s: float = 1.0, rk4_max_step_s: float = 1.0, integration_method: IntegrationMethod | str = IntegrationMethod.EXPLICIT_EULER)
```

| Field | Annotation | Default |
|---|---|---|
| `mass_kg` | `float` | `1.05` |
| `specific_heat_j_per_kg_k` | `float` | `1000.0` |
| `resistance_ohm` | `float` | `0.004` |
| `resistance_temperature_coefficient_per_k` | `float` | `0.0` |
| `resistance_reference_temperature_c` | `float` | `25.0` |
| `entropic_coefficient_v_per_k` | `float` | `0.0` |
| `external_heat_w` | `float` | `0.0` |
| `heat_transfer_w_per_k` | `float` | `1.2` |
| `emissivity` | `float` | `0.0` |
| `radiating_area_m2` | `float` | `0.0` |
| `ambient_temperature_c` | `float` | `25.0` |
| `radiative_surroundings_temperature_c` | `float \| None` | `None` |
| `initial_temperature_c` | `float` | `25.0` |
| `time_step_s` | `float` | `1.0` |
| `rk4_max_step_s` | `float` | `1.0` |
| `integration_method` | `IntegrationMethod \| str` | `IntegrationMethod.EXPLICIT_EULER` |

## `LumpedThermalSpec.thermal_capacity_j_per_k`

Read-only product of mass and specific heat.

[models/lumped_cell_thermal.py:44–46](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L44-L46).

Property declaration:

```python
thermal_capacity_j_per_k(self) -> float
```

## `LumpedThermalSpec.radiation_coefficient_w_per_k4`

Read-only product of emissivity, the implemented Stefan–Boltzmann constant and radiating area.

[models/lumped_cell_thermal.py:48–52](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L48-L52).

Property declaration:

```python
radiation_coefficient_w_per_k4(self) -> float
```

## `LumpedThermalSpec.validate`

Validate finite parameters, positive capacities/timesteps, nonnegative resistance/conductance, temperature domain, paired radiation values and solver compatibility. Raises ValueError.

[models/lumped_cell_thermal.py:54–119](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L54-L119).

Declaration / dataclass field signature:

```python
validate(self) -> None
```

## `LumpedThermalSpec.resolved_integration_method`

Resolve a string/enum to IntegrationMethod; invalid values raise ValueError.

[models/lumped_cell_thermal.py:121–128](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L121-L128).

Declaration / dataclass field signature:

```python
resolved_integration_method(self) -> IntegrationMethod
```

## `LumpedThermalSpec.resistance_at_temperature`

Evaluate the linear resistance relation; rejects temperatures outside the admitted domain and negative evaluated resistance.

[models/lumped_cell_thermal.py:130–141](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L130-L141).

Declaration / dataclass field signature:

```python
resistance_at_temperature(self, temperature_c: float) -> float
```

## `LumpedThermalSpec.reversible_heat_w`

Return signed −I·T_K·β in W for positive-discharge current; an explicit coefficient overrides the stored default.

[models/lumped_cell_thermal.py:143–161](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L143-L161).

Declaration / dataclass field signature:

```python
reversible_heat_w(self, current_a: float, temperature_c: float, entropic_coefficient_v_per_k: float | None=None) -> float
```

## `LumpedThermalSpec.radiative_heat_rejection_w`

Return signed diffuse-gray rejection to the supplied surroundings in W; negative means heat into the node.

[models/lumped_cell_thermal.py:163–185](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L163-L185).

Declaration / dataclass field signature:

```python
radiative_heat_rejection_w(self, temperature_c: float, surroundings_temperature_c: float) -> float
```

## `TemperatureLimitAssessment`

Frozen upper-limit postprocessing record. Crossing/recovery can be absent; margin is limit minus reported peak.

[models/lumped_cell_thermal.py:188–199](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L188-L199).

Declaration / dataclass field signature:

```python
TemperatureLimitAssessment(limit_temperature_c: float, exceeded: bool, first_exceedance_time_s: float | None, final_recovery_time_s: float | None, time_above_limit_s: float, exposure_fraction: float, peak_temperature_c: float, margin_to_limit_c: float)
```

| Field | Annotation | Default |
|---|---|---|
| `limit_temperature_c` | `float` | Required |
| `exceeded` | `bool` | Required |
| `first_exceedance_time_s` | `float \| None` | Required |
| `final_recovery_time_s` | `float \| None` | Required |
| `time_above_limit_s` | `float` | Required |
| `exposure_fraction` | `float` | Required |
| `peak_temperature_c` | `float` | Required |
| `margin_to_limit_c` | `float` | Required |

## `MinimumTemperatureAssessment`

Frozen lower-limit postprocessing record. Margin is reported minimum minus the requested minimum.

[models/lumped_cell_thermal.py:202–212](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L202-L212).

Declaration / dataclass field signature:

```python
MinimumTemperatureAssessment(minimum_temperature_c: float, violated: bool, first_violation_time_s: float | None, time_below_minimum_s: float, exposure_fraction: float, lowest_temperature_c: float, margin_to_minimum_c: float)
```

| Field | Annotation | Default |
|---|---|---|
| `minimum_temperature_c` | `float` | Required |
| `violated` | `bool` | Required |
| `first_violation_time_s` | `float \| None` | Required |
| `time_below_minimum_s` | `float` | Required |
| `exposure_fraction` | `float` | Required |
| `lowest_temperature_c` | `float` | Required |
| `margin_to_minimum_c` | `float` | Required |

## `ThermalSimulation`

Frozen result record. N+1 state/time values and N interval entries; obtain it from the simulator to preserve invariants.

[models/lumped_cell_thermal.py:215–411](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L215-L411).

Declaration / dataclass field signature:

```python
ThermalSimulation(time_s: tuple[float, ...], temperature_c: tuple[float, ...], current_a: tuple[float, ...], ambient_temperature_c: tuple[float, ...], radiative_surroundings_temperature_c: tuple[float, ...], heat_transfer_w_per_k: tuple[float, ...], resistance_ohm: tuple[float, ...], entropic_coefficient_v_per_k: tuple[float, ...], external_heat_w: tuple[float, ...], irreversible_heat_w: tuple[float, ...], reversible_heat_w: tuple[float, ...], heat_generation_w: tuple[float, ...], convective_heat_rejection_w: tuple[float, ...], radiative_heat_rejection_w: tuple[float, ...], heat_rejection_w: tuple[float, ...], interval_net_heat_j: tuple[float, ...], interval_duration_s: tuple[float, ...], thermal_capacity_j_per_k: float, emissivity: float, radiating_area_m2: float, rk4_max_step_s: float, integration_method: IntegrationMethod)
```

| Field | Annotation | Default |
|---|---|---|
| `time_s` | `tuple[float, ...]` | Required |
| `temperature_c` | `tuple[float, ...]` | Required |
| `current_a` | `tuple[float, ...]` | Required |
| `ambient_temperature_c` | `tuple[float, ...]` | Required |
| `radiative_surroundings_temperature_c` | `tuple[float, ...]` | Required |
| `heat_transfer_w_per_k` | `tuple[float, ...]` | Required |
| `resistance_ohm` | `tuple[float, ...]` | Required |
| `entropic_coefficient_v_per_k` | `tuple[float, ...]` | Required |
| `external_heat_w` | `tuple[float, ...]` | Required |
| `irreversible_heat_w` | `tuple[float, ...]` | Required |
| `reversible_heat_w` | `tuple[float, ...]` | Required |
| `heat_generation_w` | `tuple[float, ...]` | Required |
| `convective_heat_rejection_w` | `tuple[float, ...]` | Required |
| `radiative_heat_rejection_w` | `tuple[float, ...]` | Required |
| `heat_rejection_w` | `tuple[float, ...]` | Required |
| `interval_net_heat_j` | `tuple[float, ...]` | Required |
| `interval_duration_s` | `tuple[float, ...]` | Required |
| `thermal_capacity_j_per_k` | `float` | Required |
| `emissivity` | `float` | Required |
| `radiating_area_m2` | `float` | Required |
| `rk4_max_step_s` | `float` | Required |
| `integration_method` | `IntegrationMethod` | Required |

## `ThermalSimulation.peak_temperature_c`

Maximum of returned boundary temperatures, including the initial state.

[models/lumped_cell_thermal.py:242–244](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L242-L244).

Property declaration:

```python
peak_temperature_c(self) -> float
```

## `ThermalSimulation.stored_energy_change_j`

C times final-minus-initial temperature.

[models/lumped_cell_thermal.py:246–250](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L246-L250).

Property declaration:

```python
stored_energy_change_j(self) -> float
```

## `ThermalSimulation.integrated_net_heat_j`

Sum of state-derived interval energy changes; not independent heat-rate quadrature.

[models/lumped_cell_thermal.py:252–256](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L252-L256).

Property declaration:

```python
integrated_net_heat_j(self) -> float
```

## `ThermalSimulation.energy_bookkeeping_residual_j`

Absolute discrepancy between total state-derived energy and summed interval changes; not a temperature error estimate.

[models/lumped_cell_thermal.py:258–268](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L258-L268).

Property declaration:

```python
energy_bookkeeping_residual_j(self) -> float
```

## `ThermalSimulation.energy_balance_error_j`

Compatibility alias for energy_bookkeeping_residual_j with identical semantics.

[models/lumped_cell_thermal.py:270–277](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L270-L277).

Property declaration:

```python
energy_balance_error_j(self) -> float
```

## `ThermalSimulation.duration_s`

Sum of interval durations.

[models/lumped_cell_thermal.py:279–281](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L279-L281).

Property declaration:

```python
duration_s(self) -> float
```

## `ThermalSimulation.assess_temperature_limit`

Return strict above-limit exposure from piecewise-linear interpolation. Equality passes; final recovery is absent if never exceeded or if still above at the end.

[models/lumped_cell_thermal.py:283–342](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L283-L342).

Declaration / dataclass field signature:

```python
assess_temperature_limit(self, limit_temperature_c: float) -> TemperatureLimitAssessment
```

## `ThermalSimulation.assess_minimum_temperature`

Return strict below-minimum exposure using reported-state interpolation. Equality passes.

[models/lumped_cell_thermal.py:344–394](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L344-L394).

Declaration / dataclass field signature:

```python
assess_minimum_temperature(self, minimum_temperature_c: float) -> MinimumTemperatureAssessment
```

## `ThermalSimulation.time_step_s`

Return the common duration within relative and absolute 1e-12 tolerance, or None for a variable grid.

[models/lumped_cell_thermal.py:396–411](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L396-L411).

Property declaration:

```python
time_step_s(self) -> float | None
```

## `CurrentProfile`

Frozen loader record with interval starts, current and optional schedules; final duration is explicit or inferred from a uniform time grid.

[models/lumped_cell_thermal.py:414–442](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L414-L442).

Declaration / dataclass field signature:

```python
CurrentProfile(time_s: tuple[float, ...], current_a: tuple[float, ...], ambient_temperature_c: tuple[float, ...] | None, radiative_surroundings_temperature_c: tuple[float, ...] | None, entropic_coefficient_v_per_k: tuple[float, ...] | None, external_heat_w: tuple[float, ...] | None, heat_transfer_w_per_k: tuple[float, ...] | None, interval_duration_s: tuple[float, ...])
```

| Field | Annotation | Default |
|---|---|---|
| `time_s` | `tuple[float, ...]` | Required |
| `current_a` | `tuple[float, ...]` | Required |
| `ambient_temperature_c` | `tuple[float, ...] \| None` | Required |
| `radiative_surroundings_temperature_c` | `tuple[float, ...] \| None` | Required |
| `entropic_coefficient_v_per_k` | `tuple[float, ...] \| None` | Required |
| `external_heat_w` | `tuple[float, ...] \| None` | Required |
| `heat_transfer_w_per_k` | `tuple[float, ...] \| None` | Required |
| `interval_duration_s` | `tuple[float, ...]` | Required |

## `CurrentProfile.time_step_s`

Return the common duration within relative and absolute 1e-12 tolerance, or None.

[models/lumped_cell_thermal.py:427–442](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L427-L442).

Property declaration:

```python
time_step_s(self) -> float | None
```

## `HeatRates`

Frozen start-state heat-rate record used internally by the integrators; fields remain publicly accessible though the rate-evaluation helper is private.

[models/lumped_cell_thermal.py:445–457](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L445-L457).

Declaration / dataclass field signature:

```python
HeatRates(resistance_ohm: float, irreversible_w: float, reversible_w: float, external_w: float, generation_w: float, convective_rejection_w: float, radiative_rejection_w: float, total_rejection_w: float, net_w: float)
```

| Field | Annotation | Default |
|---|---|---|
| `resistance_ohm` | `float` | Required |
| `irreversible_w` | `float` | Required |
| `reversible_w` | `float` | Required |
| `external_w` | `float` | Required |
| `generation_w` | `float` | Required |
| `convective_rejection_w` | `float` | Required |
| `radiative_rejection_w` | `float` | Required |
| `total_rejection_w` | `float` | Required |
| `net_w` | `float` | Required |

## `load_current_profile`

Read a strict UTF-8 CSV Path into CurrentProfile; no interpolation. File errors propagate; invalid profile structure/data raise ValueError.

[models/lumped_cell_thermal.py:550–747](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L550-L747).

Declaration / dataclass field signature:

```python
load_current_profile(path: Path) -> CurrentProfile
```

## `simulate_lumped_temperature`

Validate the specification and schedules, advance the one-node model and return ThermalSimulation. Optional Python schedules override specification constants.

[models/lumped_cell_thermal.py:750–993](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L750-L993).

Declaration / dataclass field signature:

```python
simulate_lumped_temperature(currents_a: Sequence[float], spec: LumpedThermalSpec=LumpedThermalSpec(), ambient_temperatures_c: Sequence[float] | None=None, radiative_surroundings_temperatures_c: Sequence[float] | None=None, interval_durations_s: Sequence[float] | None=None, entropic_coefficients_v_per_k: Sequence[float] | None=None, external_heats_w: Sequence[float] | None=None, heat_transfers_w_per_k: Sequence[float] | None=None) -> ThermalSimulation
```

## `write_simulation_csv`

Create output parents and overwrite the chosen CSV with one .12g-formatted numeric row per interval; returns None.

[models/lumped_cell_thermal.py:996–1062](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L996-L1062).

Declaration / dataclass field signature:

```python
write_simulation_csv(path: Path, result: ThermalSimulation) -> None
```

## `write_temperature_limit_csv`

Require at least one upper-limit assessment; create parents and overwrite an eight-column summary CSV. No corresponding lower-limit writer exists.

[models/lumped_cell_thermal.py:1065–1117](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1065-L1117).

Declaration / dataclass field signature:

```python
write_temperature_limit_csv(path: Path, assessments: Sequence[TemperatureLimitAssessment]) -> None
```

## `parse_args`

Parse the 23 explicit long options plus automatic help; returns argparse.Namespace. CLI resolved defaults and mutual exclusions are completed in main.

[models/lumped_cell_thermal.py:1120–1169](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1120-L1169).

Declaration / dataclass field signature:

```python
parse_args(argv: Sequence[str] | None=None) -> argparse.Namespace
```

## `main`

Run the CLI, optionally write files and print summaries. Returns 0 for a valid calculation even when a threshold is exceeded; validation exceptions propagate.

[models/lumped_cell_thermal.py:1172–1437](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1172-L1437).

Declaration / dataclass field signature:

```python
main(argv: Sequence[str] | None=None) -> int
```

## Internal implementation and test accounting

The three underscored native helpers and nested RK4 derivative are implementation details, not public API. The complete AST inventory separately accounts for 121 Python definitions across the model and tests, including private/nested/test definitions. The source guide validator is a top-level script. No dynamic native plugin registration was found; dataclass constructors derive from the explicit fields above.

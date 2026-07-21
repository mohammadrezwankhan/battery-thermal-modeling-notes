# Lumped Cell Thermal Reference

This dependency-free Python model turns the repository's simplest documented
thermal assumptions into an executable calculation. It is intended for
education, early screening, and validation-workflow examples, not cell design
or safety qualification.

## Governing Balance

For each time interval, the model evaluates:

```text
Q_irreversible = I^2 R
Q_reversible = -I T_kelvin dU_oc/dT
Q_generation = Q_irreversible + Q_reversible
R(T) = R_ref [1 + alpha (T_cell - T_ref)]
Q_rejection = h(t) (T_cell - T_ambient)
C_thermal dT/dt = Q_generation - Q_rejection
C_thermal = mass * specific_heat
```

The default method advances temperature with an explicit Euler step. The
optional exact linear method solves each interval analytically when current,
ambient, entropic coefficient, and heat-transfer coefficient are piecewise
constant. The returned result includes stored thermal energy, integrated net
heat, and their absolute difference so discretization and implementation
changes can be audited.

## Run The Reference Case

From the repository root with Python 3.12 or later:

```powershell
python models/lumped_cell_thermal.py `
  --current-a 75 `
  --duration-s 600 `
  --time-step-s 1
```

The default case represents a 75 A constant-current interval applied to a
1.05 kg lumped cell with 1000 J/(kg K) specific heat, 4 mOhm resistance,
zero resistance temperature coefficient, zero entropic coefficient, 1.2 W/K
heat transfer, and 25 degC initial and ambient temperature.

Run the regression checks with:

```powershell
python -m unittest discover -s tests -v
```

## Exact Linear Integration

Use `--integration-method exact-linear` when a coarse interval would make an
explicit Euler approximation unnecessarily sensitive to time-step size:

```powershell
python models/lumped_cell_thermal.py `
  --current-a 75 --duration-s 600 --time-step-s 600 `
  --integration-method exact-linear
```

With constant current, ambient, and entropic coefficient over an interval,
linear heat rejection, reversible heat, and the configured linear
resistance-temperature relation produce a linear ODE. An interval-specific
heat-transfer coefficient is included in that interval's exact feedback slope.
The exact method evaluates its exponential solution with `expm1` for numerical
stability. It also stores the exact net interval heat as thermal capacity times
the temperature change. CSV heat rates, `resistance_ohm`, and
`entropic_coefficient_v_per_k` remain start-of-interval values; `net_heat_j` is
the integrated interval quantity.

The exact method removes integration error for this model equation, but it does
not make piecewise-constant current, ambient, parameter, or one-node
assumptions more accurate. Keep explicit Euler for educational recurrence
comparisons or backward-compatible result reproduction.

## Run A Current And Ambient Profile

The CLI accepts a strict CSV containing interval-start timestamps and current
commands, with optional interval duration, ambient temperature, entropic
coefficient, and heat-transfer coefficient columns.
Without a `duration_s` column, timestamps must start at zero and use one
uniform step; positive and negative currents both produce irreversible `I^2 R`
heat.

```csv
time_s,current_a
0,0
60,75
120,-50
```

Run the committed pulse example and export one auditable row per interval:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/pulse_current_profile.csv `
  --output-csv results/pulse_thermal_intervals.csv
```

The output records interval boundaries and duration, current, start/end
temperature, ambient temperature, heat-transfer coefficient, evaluated
resistance, entropic coefficient, irreversible, reversible, total generated
and rejected heat rates, and net interval heat.
Profile mode derives the time step from the CSV and rejects `--current-a`,
`--duration-s`, or `--time-step-s` overrides.

Run the ambient-step example to make the thermal boundary condition traceable
in both the input and exported interval records:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/ambient_step_current_profile.csv `
  --output-csv results/ambient_step_thermal_intervals.csv
```

A profile without an ambient column uses `--ambient-temperature-c` or its
25 degC default. A profile containing `ambient_temperature_c` cannot be
combined with that option because the interval values are authoritative.

For measurements or dispatch commands with irregular operating windows, add a
positive `duration_s` value to every row. Each `time_s` must equal the previous
interval's end, which rejects gaps and overlaps while making the final
interval's duration explicit:

```csv
time_s,current_a,duration_s,ambient_temperature_c
0,0,30,25
30,75,90,30
120,-50,15,35
```

Run the committed irregular profile with exact within-interval integration:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/irregular_current_profile.csv `
  --integration-method exact-linear `
  --output-csv results/irregular_thermal_intervals.csv
```

The Python API accepts the same schedule through `interval_durations_s`. The
simulation exposes every interval duration, cumulative time boundaries, and
the total elapsed duration. Its `time_step_s` compatibility property returns
the common duration for a uniform grid and `None` for a variable grid.

## Variable Cooling Boundary

Add `heat_transfer_w_per_k` to a profile to represent a supplied sequence of
effective cooling conditions such as staged airflow, coolant-flow operating
points, or conservative sensitivity cases:

```csv
time_s,current_a,duration_s,ambient_temperature_c,heat_transfer_w_per_k
0,100,300,35,0.6
300,100,300,35,1.2
600,100,300,35,4.0
900,50,300,30,6.0
1200,0,600,25,6.0
```

Run the committed staged-cooling example with exact integration:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/variable_cooling_profile.csv `
  --integration-method exact-linear `
  --output-csv results/variable_cooling_intervals.csv
```

The Python API accepts the same values through `heat_transfers_w_per_k`. Values
must be finite and nonnegative. A profile column takes precedence over the
constant boundary, so combining it with `--heat-transfer-w-per-k` is rejected
instead of silently choosing one source. Every interval result and exported row
preserves the applied value.

This input is an effective conductance boundary, not a fan, pump, coolant-loop,
or feedback-controller model. Step changes occur only at supplied interval
boundaries; derive values from measurements, correlations, or a separately
validated cooling model before drawing design conclusions.

## Reversible Entropic Heat

Use `--entropic-coefficient-v-per-k` to add the reversible Bernardi heat term.
This model defines positive current as discharge and evaluates
`Q_reversible = -I * T_kelvin * dU_oc/dT`; therefore reversing current reverses
the reversible term while `I^2 R` remains nonnegative. A positive coefficient
produces reversible cooling during positive-current discharge and heating
during negative-current charge under this convention.

The equation and interpretation follow the electrode-sandwich heat balance in
the [NREL Li-Ion Battery Thermal Characterization paper](https://www.osti.gov/biblio/2349292),
which separates irreversible overpotential heat from reversible entropic heat.
Coefficient sign and magnitude vary with chemistry, SOC, and test method, so
replace the illustrative values with cell-specific measurements.

Run the committed charge/discharge example with an interval-varying coefficient:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/reversible_heat_current_profile.csv `
  --integration-method exact-linear `
  --output-csv results/reversible-heat-intervals.csv
```

The Python API accepts `entropic_coefficients_v_per_k` with one value per
current interval. A profile may add `entropic_coefficient_v_per_k` after the
optional duration and ambient columns, allowing an externally prepared
SOC-dependent coefficient schedule without claiming an electrical SOC model.
Every result preserves the coefficient and separate irreversible, reversible,
and total heat-source traces. For exact-linear integration, all reported heat
rates are start-of-interval values while `net_heat_j` remains the exact
integrated thermal-energy change.

## Temperature-Dependent Resistance

Set `--resistance-temperature-coefficient-per-k` to evaluate a linear
temperature correction around `--resistance-reference-temperature-c`. A
positive coefficient increases irreversible heat as the cell warms, making the
electrical-to-thermal feedback visible while preserving a one-node model:

```powershell
python models/lumped_cell_thermal.py `
  --current-a 100 --duration-s 600 `
  --resistance-temperature-coefficient-per-k 0.01 `
  --resistance-reference-temperature-c 25
```

Expected key values for that illustrative case:

```text
Final temperature: 43.351 degC
Peak temperature: 43.351 degC
Resistance range: 0.004000 to 0.004733 ohm
```

The coefficient defaults to zero, so all existing reference cases retain their
constant-resistance behavior. Every interval records the evaluated resistance,
and a configuration that produces negative resistance at an evaluated
temperature is rejected. Replace the reference resistance, coefficient, and
temperature with values fitted or measured for the target cell and operating
window before engineering use.

## Explicit Limitations

- Resistance may use an optional linear temperature coefficient, but it does
  not vary with SOC or age and does not represent a nonlinear measured map.
- Reversible heat uses a supplied constant or piecewise-constant entropic
  coefficient; the model does not derive its SOC or chemistry dependence.
- Mixing, phase-change, side-reaction, and interconnect heat are excluded.
- The cell is represented by one uniform temperature state.
- Heat transfer is linear; ambient and the effective heat-transfer coefficient
  may vary by interval, but fluid dynamics, coolant thermal mass, actuator
  dynamics, and feedback control are not represented.
- Electrical SOC and voltage dynamics are outside this reference model.
- Parameters are educational placeholders and require sourced replacement for
  engineering decisions.
- Current-profile timestamps are treated as interval starts with piecewise
  constant current, ambient temperature, coefficients, and heat transfer over
  each interval. Explicit durations may vary, but the model does not interpolate
  within an interval.
- Exact integration applies only to the model's linear within-interval
  equation; nonlinear resistance maps or radiation would require a different
  solver.

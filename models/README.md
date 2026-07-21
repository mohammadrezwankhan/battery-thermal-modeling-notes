# Lumped Cell Thermal Reference

This dependency-free Python model turns the repository's simplest documented
thermal assumptions into an executable calculation. It is intended for
education, early screening, and validation-workflow examples, not cell design
or safety qualification.

## Governing Balance

For each time interval, the model evaluates:

```text
Q_generation = I^2 R
R(T) = R_ref [1 + alpha (T_cell - T_ref)]
Q_rejection = h (T_cell - T_ambient)
C_thermal dT/dt = Q_generation - Q_rejection
C_thermal = mass * specific_heat
```

The default method advances temperature with an explicit Euler step. The
optional exact linear method solves each piecewise-constant interval
analytically. The returned result includes stored thermal energy, integrated
net heat, and their absolute difference so discretization and implementation
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
zero resistance temperature coefficient, 1.2 W/K heat transfer, and 25 degC
initial and ambient temperature.

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

With constant current and ambient over an interval, linear heat rejection and
the configured linear resistance-temperature relation produce a linear ODE.
The exact method evaluates its exponential solution with `expm1` for numerical
stability. It also stores the exact net interval heat as thermal capacity times
the temperature change. CSV `heat_generation_w`, `heat_rejection_w`, and
`resistance_ohm` remain start-of-interval values; `net_heat_j` is the integrated
interval quantity.

The exact method removes integration error for this model equation, but it does
not make piecewise-constant current, ambient, parameter, or one-node
assumptions more accurate. Keep explicit Euler for educational recurrence
comparisons or backward-compatible result reproduction.

## Run A Current And Ambient Profile

The CLI accepts a strict CSV containing interval-start timestamps and current
commands, with optional interval duration and ambient-temperature columns.
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
temperature, ambient temperature, evaluated resistance, generated and rejected
heat rates, and net interval heat.
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
- Heat generation contains irreversible ohmic loss only.
- Reversible entropic heat is excluded.
- The cell is represented by one uniform temperature state.
- Heat transfer is linear; ambient may vary by interval, but the heat-transfer
  coefficient remains fixed.
- Electrical SOC and voltage dynamics are outside this reference model.
- Parameters are educational placeholders and require sourced replacement for
  engineering decisions.
- Current-profile timestamps are treated as interval starts with piecewise
  constant current and ambient temperature over each interval. Explicit
  durations may vary, but the model does not interpolate within an interval.
- Exact integration applies only to the model's linear within-interval
  equation; nonlinear resistance maps or radiation would require a different
  solver.

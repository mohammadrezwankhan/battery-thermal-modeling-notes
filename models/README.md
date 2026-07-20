# Lumped Cell Thermal Reference

This dependency-free Python model turns the repository's simplest documented
thermal assumptions into an executable calculation. It is intended for
education, early screening, and validation-workflow examples, not cell design
or safety qualification.

## Governing Balance

For each time interval, the model evaluates:

```text
Q_generation = I^2 R
Q_rejection = h (T_cell - T_ambient)
C_thermal dT/dt = Q_generation - Q_rejection
C_thermal = mass * specific_heat
```

The temperature state is advanced with an explicit Euler step. The returned
result includes stored thermal energy, integrated net heat, and their absolute
difference so discretization and implementation changes can be audited.

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
1.2 W/K heat transfer, and 25 degC initial and ambient temperature.

Run the regression checks with:

```powershell
python -m unittest discover -s tests -v
```

## Run A Current Profile

The CLI accepts a strict two-column CSV containing interval-start timestamps
and current commands. Timestamps must start at zero and use one uniform step;
positive and negative currents both produce irreversible `I^2 R` heat.

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

The output records interval boundaries, current, start/end temperature,
generated and rejected heat rates, and net interval heat. Profile mode derives
the time step from the CSV and rejects `--current-a`, `--duration-s`, or
`--time-step-s` overrides.

## Explicit Limitations

- Resistance is constant and does not vary with SOC, temperature, or age.
- Heat generation contains irreversible ohmic loss only.
- Reversible entropic heat is excluded.
- The cell is represented by one uniform temperature state.
- Heat transfer is linear and ambient temperature is fixed.
- Electrical SOC and voltage dynamics are outside this reference model.
- Parameters are educational placeholders and require sourced replacement for
  engineering decisions.
- Current-profile timestamps are treated as interval starts with piecewise
  constant current over each interval.

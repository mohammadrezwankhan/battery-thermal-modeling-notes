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
Q_generation = Q_irreversible + Q_reversible + Q_external
R(T) = R_ref [1 + alpha (T_cell - T_ref)]
Q_convection = h(t) (T_cell - T_ambient)
Q_radiation = epsilon sigma A (T_cell_kelvin^4 - T_surroundings_kelvin^4)
Q_rejection = Q_convection + Q_radiation
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
heat transfer, zero surface radiation, and 25 degC initial and ambient
temperature.

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

## Nonlinear Surface Radiation

Set both `--emissivity` and `--radiating-area-m2` to add net diffuse-gray
surface radiation. The implementation uses the exact NIST CODATA
Stefan-Boltzmann constant, `5.670374419e-8 W/(m^2 K^4)`, from the
[2022 CODATA recommended values](https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf).
The supplied ambient temperature is also the effective radiative-surroundings
temperature for each interval unless a separate boundary is supplied. Use
`--radiative-surroundings-temperature-c` for a constant enclosure temperature,
or add `radiative_surroundings_temperature_c` to a profile for an independent
piecewise-constant schedule.

Radiation makes the temperature balance nonlinear, so it requires the
fourth-order Runge-Kutta method. `--rk4-max-step-s` bounds the internal solver
step independently of the profile interval width:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/radiative_cooling_profile.csv `
  --emissivity 0.85 --radiating-area-m2 0.03 `
  --integration-method rk4 --rk4-max-step-s 0.5 `
  --output-csv results/radiative_cooling_intervals.csv
```

The committed illustrative case separates a `25` to `35 degC` convection
boundary from a `10` to `50 degC` radiative-surroundings schedule. It reports a
final temperature of `33.323 degC`, a peak of `55.433 degC`, and
start-of-interval radiative heat rejection from `-4.342 W` to `6.200 W`.
Negative rejection means the cooler cell receives net radiative heat from
warmer surroundings. The result and CSV keep both boundary temperatures,
convection, radiation, and total heat rejection separate; integrated net heat
remains the thermal-capacity change over each RK4 interval.

The default emissivity and area are both zero, preserving every existing
linear case. The two parameters must either both be zero or both be positive,
emissivity is constrained to `[0, 1]`, and area must be nonnegative. The
`exact-linear` method rejects enabled radiation rather than silently dropping
the nonlinear term. This is a screening boundary: surface emissivity and area
are constant, each interval has one effective radiative-surroundings
temperature, and view factors, reflections, enclosure exchange, and wavelength
dependence are excluded.

## Run A Current And Ambient Profile

The CLI accepts a strict CSV containing interval-start timestamps and current
commands, with optional interval duration, ambient temperature, entropic
coefficient, radiative-surroundings temperature, and heat-transfer coefficient
columns.
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
temperature, ambient and radiative-surroundings temperatures, heat-transfer
coefficient, radiation parameters, evaluated resistance, entropic coefficient,
irreversible, reversible, total generated, convective, radiative, and total
rejected heat rates, and net interval heat.
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
Likewise, a profile without a radiative-surroundings column uses
`--radiative-surroundings-temperature-c`; when neither source is supplied,
radiation follows ambient for backward compatibility. A profile containing
`radiative_surroundings_temperature_c` cannot be combined with the constant
option. All supplied temperatures must be finite and above absolute zero.

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

## External Heat-Source Profile

Use `--external-heat-w` for a constant signed heat flow into the lumped node,
or add `external_heat_w` to a current-profile CSV for a piecewise-constant
schedule. Positive values add heat; negative values represent an independently
specified heat sink. This can represent a controlled heater, neighboring
component, interconnect estimate, or calibrated parasitic source without
folding that term into electrical resistance.

Run the committed profile through the exact linear integrator:

```powershell
python models/lumped_cell_thermal.py `
  --profile-csv models/data/external_heat_profile.csv `
  --integration-method exact-linear `
  --output-csv results/external_heat_intervals.csv
```

The exported `external_heat_w` column remains separate from irreversible and
reversible heat. `heat_generation_w` is their signed sum, and `net_heat_j`
continues to close the stored thermal-energy balance for explicit Euler, exact
linear, and RK4 integration. A profile source takes precedence over the default
zero source; combining a profile column with `--external-heat-w` is rejected so
the boundary condition remains unambiguous.

This input is a prescribed source, not a conduction network or a solved heater
controller. Its sign, location, time alignment, and physical basis must be
documented before engineering use. A negative source can remove more heat than
the electrical terms generate, but it does not enforce coolant, surface, or
absolute-temperature constraints beyond the model's existing validation.

## Temperature-Limit Exposure

Assess one or more project-defined temperature limits after a simulation and
write one summary row per limit:

```powershell
python models/lumped_cell_thermal.py `
  --current-a 75 --duration-s 600 `
  --temperature-limit-c 30 `
  --temperature-limit-c 35 `
  --limit-report-csv results/temperature-limits.csv
```

Each assessment reports whether the limit was exceeded, the first-crossing
time, final recovery time when the trace ends at or below the limit, total
time above the limit, exposure fraction, peak temperature, and
signed margin from the peak to the limit. A negative margin means the simulated
peak exceeded the limit. The limit itself is not counted as an exceedance.

Crossing times and exposure duration use piecewise-linear interpolation between
the reported temperature states. This makes the calculation deterministic for
uniform and variable-duration profiles, but it does not reconstruct motion
inside an integration interval. Use a reviewed time-step sensitivity study when
a short excursion or precise threshold timing matters. Temperature limits are
project inputs, not safety recommendations from this educational model.

## Explicit Limitations

- Resistance may use an optional linear temperature coefficient, but it does
  not vary with SOC or age and does not represent a nonlinear measured map.
- Reversible heat uses a supplied constant or piecewise-constant entropic
  coefficient; the model does not derive its SOC or chemistry dependence.
- External heat is prescribed rather than derived from a neighboring thermal
  node, heater controller, or interconnect model.
- Mixing, phase-change, and side-reaction heat are excluded.
- The cell is represented by one uniform temperature state.
- Convection is linear; optional diffuse-gray radiation uses constant surface
  emissivity and area with ambient as the radiative-surroundings temperature.
  Fluid dynamics, coolant thermal mass, view factors, reflections, actuator
  dynamics, and feedback control are not represented.
- Electrical SOC and voltage dynamics are outside this reference model.
- Parameters are educational placeholders and require sourced replacement for
  engineering decisions.
- Current-profile timestamps are treated as interval starts with piecewise
  constant current, ambient temperature, coefficients, and heat transfer over
  each interval. Explicit durations may vary, but the model does not interpolate
  within an interval.
- Temperature-limit exposure is linearly interpolated between reported states;
  an unreported within-step excursion can be missed.
- Exact integration applies only to the model's linear within-interval
  equation. Surface radiation uses bounded-step RK4; nonlinear resistance
  maps would require a separately validated extension.

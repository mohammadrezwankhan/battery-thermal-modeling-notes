# APIs, CLI and data interfaces

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

Import from `models.lumped_cell_thermal`. [API_REFERENCE.md](API_REFERENCE.md) enumerates all 30 public class/function/property declarations, 70 annotated dataclass fields, three integration enum values and two constants. Ordinary function and dataclass constructor parameters are positional-or-keyword; defaults make values optional without changing that calling convention. Properties are attributes, not methods to call. Frozen dataclasses prevent normal attribute reassignment but direct construction of result records does not validate array consistency. Prefer records returned by the simulator/loader. [models/lumped_cell_thermal.py:17–457](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L17-L457); [models/lumped_cell_thermal.py:750–759](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L750-L759).

## Main native flow

`load_current_profile(Path(...))` returns a `CurrentProfile`. Pass its current tuple and optional boundary/parameter schedules to `simulate_lumped_temperature`, which returns a `ThermalSimulation`. Explicit Python schedules override the corresponding specification value; unlike CLI conflicts, that override is intentional. Input arrays need one value per current interval. `time_s` and `temperature_c` contain N+1 states; current, heat, resistance, coefficients and durations contain N interval values. `time_step_s` returns the common duration under `rel_tol=abs_tol=1e-12`, or `None`. [models/lumped_cell_thermal.py:396–442](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L396-L442); [models/lumped_cell_thermal.py:750–861](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L750-L861); [models/lumped_cell_thermal.py:953–993](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L953-L993).

## CLI options and resolved defaults

The parser registers 23 explicit long options plus automatic `-h/--help`. Source registration and resolution: [models/lumped_cell_thermal.py:1120–1302](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1120-L1302).

| Options | Effective default / rule |
|---|---|
| `--profile-csv PATH`, `--output-csv PATH` | No profile/output file unless supplied |
| `--current-a`, `--duration-s`, `--time-step-s` | Constant mode: 75 A, 600 s, 1 s; duration must be an integer multiple of the step within 1e-9 s absolute tolerance |
| `--mass-kg`, `--specific-heat-j-per-kg-k` | 1.05 kg; 1000 J/(kg·K) |
| `--resistance-ohm` | 0.004 Ω |
| `--resistance-temperature-coefficient-per-k`, `--resistance-reference-temperature-c` | 0 K⁻¹; 25 °C |
| `--entropic-coefficient-v-per-k`, `--external-heat-w` | 0 V/K; 0 W |
| `--heat-transfer-w-per-k` | 1.2 W/K effective conductance |
| `--emissivity`, `--radiating-area-m2` | Both 0; otherwise both positive, emissivity ≤1, and RK4 required |
| `--ambient-temperature-c`, `--initial-temperature-c` | Both 25 °C |
| `--radiative-surroundings-temperature-c` | Unset means follow the applied interval ambient |
| `--integration-method` | `explicit-euler`; alternatives `exact-linear`, `rk4` |
| `--rk4-max-step-s` | 1 s; internal RK4 cap independent of output interval width |
| `--temperature-limit-c` | Repeatable unique upper limits; equality passes |
| `--minimum-temperature-c` | Repeatable unique lower limits; equality passes |
| `--limit-report-csv PATH` | Upper-limit CSV only; requires at least one `--temperature-limit-c` |

Profile mode rejects explicit current, duration or time-step options. A CSV column for ambient, surroundings, entropic coefficient, external heat or conductance conflicts with the corresponding constant CLI option; omitting the column enables its constant/default value. `main` returns 0 after a valid run even when a limit is reported `EXCEEDED` or `VIOLATED`. Runtime validation raises `ValueError`; argparse handles malformed options. Do not interpret exit 0 as a safe-temperature decision. [models/lumped_cell_thermal.py:1172–1252](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1172-L1252); [models/lumped_cell_thermal.py:1388–1437](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1388-L1437).

## Strict input CSV

The first two headers must be `time_s,current_a`. Select any subset of the following optional headers **in this order**: `duration_s`, `ambient_temperature_c`, `radiative_surroundings_temperature_c`, `entropic_coefficient_v_per_k`, `external_heat_w`, `heat_transfer_w_per_k`. Header whitespace/BOM is normalized; blank lines and lines whose first nonspace character is `#` are skipped. All data must be numeric and finite; no unknown/duplicate/reordered columns are accepted. [models/lumped_cell_thermal.py:550–666](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L550-L666).

Time starts at zero within 1e-12 s. With `duration_s`, at least one row is allowed, durations are positive, and each next start equals the previous end within relative 1e-9 / absolute 1e-12 tolerance. Without it, at least two rows establish a strictly positive uniform step, which is also assigned to the final row. Thus `0,60,120` represents three intervals and 180 s total. Optional temperature values must exceed −273.15 °C and conductance must be nonnegative. [models/lumped_cell_thermal.py:603–747](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L603-L747).

## Exports and browser interfaces

The interval CSV has 21 columns: interval start/end/duration; current; ambient/surroundings; conductance; emissivity/area; resistance/entropic coefficient/external heat; start/end temperature; irreversible/reversible/total generation; convection/radiation/total rejection; and `net_heat_j`. All numeric values use `.12g`. Heat rates and resistance are sampled at the interval start, while net heat is the state-derived interval energy change. The eight-column upper-limit CSV uses lowercase booleans and empty fields for absent crossing/recovery times. There is no lower-limit CSV writer. [models/lumped_cell_thermal.py:996–1117](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L996-L1117).

The browser's five-member `LabSimulation` export, read-only dashboard hook, bounded controls, eight checkpoint definitions and catalogue/storage/export behavior are inventoried in [BROWSER_MODEL_CATALOG.md](BROWSER_MODEL_CATALOG.md). These JavaScript interfaces do not invoke the Python model.

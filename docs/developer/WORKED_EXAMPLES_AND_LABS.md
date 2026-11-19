# Worked examples and laboratories

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

These are local executions observed on 2026-11-19 with Python 3.12.14 against the reviewed source. They verify reproducible illustrative calculations. Use [models/README.md](../../models/README.md) for the preserved feature walkthrough and [setup](SETUP_AND_REPRODUCIBILITY.md) for the checkout. All CSV inputs are committed educational profiles; no measurement record, cell identifier or calibration accompanies them. [models/README.md:32–53](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L32-L53); [models/README.md:378–403](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L378-L403).

## 1. Separate solver error from bookkeeping

```bash
python models/lumped_cell_thermal.py --current-a 75 --duration-s 600
python models/lumped_cell_thermal.py --current-a 75 --duration-s 600 --time-step-s 600 --integration-method exact-linear
```

Defaults give thermal capacity 1050 J/K, Joule heat 22.5 W, steady temperature 43.75 °C and time constant 875 s. The 600-step Euler run reports **34.309 °C**; one exact-linear interval reports **34.305 °C**. These rounded values come from execution, with exact-linear behavior independently covered by the source analytic test. [models/lumped_cell_thermal.py:27–46](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L27-L46); [tests/test_lumped_cell_thermal.py:295–340](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L295-L340).

For a clearer numerical lesson, use the existing test's C=10 J/K, external heat=10 W, conductance=1 W/K, T₀=Tₐ=20 °C case. Its analytic value at 10 s is 26.3212056 °C. One 10 s Euler step gives 30 °C; two 5 s steps give 27.5 °C. Both have zero state-derived bookkeeping residual. The residual therefore cannot rank solver accuracy. This is an explanatory reproduction of the existing test, not a new physical benchmark. [tests/test_lumped_cell_thermal.py:406–441](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L406-L441).

```python
from models.lumped_cell_thermal import LumpedThermalSpec, simulate_lumped_temperature
for step, count in [(10.0, 1), (5.0, 2)]:
    result = simulate_lumped_temperature(
        [0.0] * count,
        LumpedThermalSpec(mass_kg=1.0, specific_heat_j_per_kg_k=10.0,
            resistance_ohm=0.0, external_heat_w=10.0,
            heat_transfer_w_per_k=1.0, ambient_temperature_c=20.0,
            initial_temperature_c=20.0, time_step_s=step),
    )
    print(result.temperature_c[-1], result.energy_bookkeeping_residual_j)
```

## 2. Reproduce the seven input profiles

For a row below, substitute its filename and method:

```bash
python models/lumped_cell_thermal.py --profile-csv models/data/irregular_current_profile.csv --integration-method exact-linear --output-csv results/irregular_thermal_intervals.csv
```

| Input filename | Method and additional settings | Intervals / elapsed seconds | Observed final / reported peak °C |
|---|---|---:|---:|
| `pulse_current_profile.csv` | explicit-euler | 10 / 600 | 30.563 / 31.569 |
| `ambient_step_current_profile.csv` | explicit-euler | 6 / 360 | 29.964 / 29.964 |
| `irregular_current_profile.csv` | exact-linear | 4 / 180 | 27.714 / 27.714 |
| `reversible_heat_current_profile.csv` | exact-linear | 4 / 360 | 29.811 / 30.153 |
| `variable_cooling_profile.csv` | exact-linear | 5 / 1800 | 25.296 / 46.150 |
| `external_heat_profile.csv` | exact-linear | 3 / 300 | 26.919 / 26.919 |
| `radiative_cooling_profile.csv` | rk4; emissivity 0.85, area 0.03 m², maximum internal step 0.5 s | 4 / 1800 | 33.323 / 55.433 |

The complete input rows are linked in [source evidence](../SOURCE_EVIDENCE.md); prescribed schedules are not actuator or coolant-loop dynamics. Reported peaks use stored boundary states. Radiation command:

```bash
python models/lumped_cell_thermal.py --profile-csv models/data/radiative_cooling_profile.csv --emissivity 0.85 --radiating-area-m2 0.03 --integration-method rk4 --rk4-max-step-s 0.5 --output-csv results/radiative_thermal_intervals.csv
```

## 3. Inspect upper and lower limits

```bash
python models/lumped_cell_thermal.py --current-a 75 --duration-s 600 --temperature-limit-c 30 --temperature-limit-c 35 --minimum-temperature-c 20 --limit-report-csv results/temperature-limits.csv
```

The observed default run exceeds 30 °C, passes 35 °C and stays above the 20 °C minimum; the process returns 0. Inspect the report instead of using that exit code as a threshold gate. For a transparent hand calculation, the source test warms linearly from 20 to 40 °C over 20 s: a 25 °C limit first crosses at 5 s, has 15 s exposure, fraction 0.75 and margin −15 °C. Limits here are teaching inputs, not recommended operating values. [tests/test_lumped_cell_thermal.py:27–56](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/tests/test_lumped_cell_thermal.py#L27-L56); [models/lumped_cell_thermal.py:1388–1437](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1388-L1437).

## 4. Browser-to-native comparison

The first browser module uses Q=1200 W, G=40 W/K, C=18000 J/K and ambient 25 °C. At 10 min the actual embedded model gives **47.0920858565 °C** and **397.657545418 kJ** above ambient; all eight declared checkpoints passed in a pure JavaScript evaluation. This evaluates the model and checkpoint functions, not DOM interactions. Reproduce the same physical equation natively with I=0, R=0, external heat=1200 W, mass=1 kg, specific heat=18000 J/(kg·K), G=40 W/K and one 600 s exact-linear interval. Keep the browser's minutes versus native seconds explicit. [docs/index.html:167–172](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L167-L172); [docs/index.html:257–259](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L257-L259); [models/lumped_cell_thermal.py:903–929](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L903-L929).

## 5. Verify the source suite

```bash
python -m unittest discover -s tests -v
python scripts/portfolio/validate_guide.py
```

Observed: **85 tests passed** and **four source-linked learning paths validated**. The [verification ledger](../maintainer/VERIFICATION_EVIDENCE_LEDGER.md) explains each criterion and its limits. Neither command establishes measured-cell accuracy, browser visual quality or current publication.

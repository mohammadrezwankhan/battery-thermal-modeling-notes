# Browser model and control inventory

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

The active configuration selects `thermal`. The exact embedded UMD exposes `MODEL_SPECS`, `getModelSpec(kind)`, `resolveParameters(kind, provided)`, `evaluateModel(kind, provided, time)` and `checkCheckpoint(checkpoint, metrics)` as `LabSimulation` in a browser or `module.exports` in a CommonJS context. Unknown kinds throw; finite numeric inputs are clamped to per-model bounds, missing/nonfinite inputs fall back to defaults, and time is clamped to the model horizon. No numeric-string coercion is performed for parameter values. [docs/index.html:150–159](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L150-L159); [docs/index.html:231–246](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L231-L246); [docs/index.html:320–335](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L320-L335).

## Active thermal surface

Four sliders control heat input, effective conductance, thermal capacity and ambient. Time is 0–60 minutes. The four metrics are temperature °C, heat removed W, stored heat kJ and net heating W. The model starts at ambient and evaluates a closed form; no native input profile, entropic heat, resistance feedback or radiation is active. [docs/index.html:167–172](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L167-L172); [docs/index.html:257–259](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L257-L259).

| Parameter | Default | Range | Step | Unit |
|---|---:|---:|---:|---|
| `heatW` | 1200 | 100–3000 | 100 | W |
| `coolingWK` | 40 | 10–120 | 5 | W/K |
| `capacityJPerK` | 18000 | 3000–60000 | 1000 | J/K |
| `ambientC` | 25 | 0–45 | 1 | °C |

The UI can override parameter labels/units/defaults and metric labels/units/precision, but model bounds, time unit and horizon come from the bundled spec. It builds 241 samples over the horizon; CSV export includes model time, all metrics and current inputs at 12 significant digits. A preset moves to the first fixed checkpoint time. Strict `<`/`>` checkpoints ignore tolerance; equality uses absolute tolerance. A previously verified module is labelled as a prior experiment after settings change. [docs/index.html:357–398](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L357-L398); [docs/index.html:448–470](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L448-L470).

The read-only `LabDashboard` hook exposes `getState()` (kind, copied parameters, time, playing state, active metric/module), `evaluateModel` and `getModelSpec`. It does not expose mutation controls. [docs/index.html:469–470](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L469-L470).

## Observed numerical checkpoints

All eight declared thermal checkpoints passed by evaluating the source UMD in Node, without running the DOM layer. This is not browser UI, screen-reader, screenshot or physical validation.

| Module | Metric / time (min) | Declared target | Observed |
|---|---|---|---:|
| module-1 | `temperatureC` / 10 | == 47.092086 ± 0.02 | 47.0920858565 |
| module-1 | `storedEnergyKJ` / 10 | == 397.657545 ± 0.02 | 397.657545418 |
| module-2 | `temperatureC` / 10 | == 39.597486 ± 0.02 | 39.597486429 |
| module-2 | `residualW` / 10 | == 616.100543 ± 0.02 | 616.100542839 |
| module-3 | `temperatureC` / 10 | == 62.092086 ± 0.02 | 62.0920858565 |
| module-3 | `storedEnergyKJ` / 10 | == 397.657545 ± 0.02 | 397.657545418 |
| module-4 | `temperatureC` / 30 | == 39.994968 ± 0.02 | 39.9949680606 |
| module-4 | `residualW` / 30 | < 1 (strict) | 0.402555153483 |

## All bundled model kinds

All ten dispatch branches are structurally enumerated below. Only `thermal` is selected by this repository configuration and numerically checked in this review. The other nine are dormant generic teaching formulas; they do not establish native application features or portfolio integrations. [docs/index.html:159–230](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L159-L230); [docs/index.html:243–318](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L243-L318).

| Kind | Model time / horizon | Parameter keys | Metric keys |
|---|---|---|---|
| `battery` | 6 h | `capacityAh`, `currentA`, `resistanceOhm`, `ambientC`, `initialSoc` | `socPct`, `voltageV`, `temperatureC`, `powerKW` |
| `thermal` | 60 min | `heatW`, `coolingWK`, `capacityJPerK`, `ambientC` | `temperatureC`, `heatRemovedW`, `storedEnergyKJ`, `residualW` |
| `degradation` | 1000 cycles | `fadePer1000Pct`, `temperatureC`, `cRate`, `initialCapacityAh` | `retentionPct`, `capacityAh`, `resistanceGrowthPct`, `throughputKWh` |
| `grid` | 24 h | `demandKW`, `solarKW`, `batteryKW`, `carbonGPerKWh` | `gridImportKW`, `solarOutputKW`, `renewablePct`, `emissionsKgPerH` |
| `cooling` | 60 min | `serverCount`, `utilizationPct`, `ambientC`, `coolingEfficiency` | `itKW`, `coolingKW`, `pue`, `inletC` |
| `agents` | 30 min | `arrivalRate`, `agentCount`, `serviceRate`, `coordinationPct` | `backlog`, `throughput`, `utilizationPct`, `waitMinutes` |
| `markets` | 24 h | `baseSpreadBps`, `feeBps`, `slippageBps`, `notionalUSD` | `spreadBps`, `netEdgeBps`, `netPnlUSD`, `costUSD` |
| `control` | 20 s | `setpoint`, `damping`, `naturalFrequency`, `gain` | `output`, `error`, `velocity`, `overshootPct` |
| `security` | 60 min | `alertRate`, `analystCount`, `reviewRate`, `automationPct` | `backlog`, `coveragePct`, `reviewedAlerts`, `workloadPct` |
| `charging` | 120 min | `capacityKWh`, `chargerKW`, `initialSoc`, `efficiencyPct` | `socPct`, `chargingKW`, `energyAddedKWh`, `lossKW` |

## Catalogue, portfolio and historic animation

The native catalogue supports text/tag filters and copies displayed commands; it does not execute Python. The portfolio guide supports text/topic/level filters, a dialog, personal review state/notes, motion preference and a study-plan JSON export. Storage key is `portfolio-learning:<repository>:<source_revision>`; unavailable storage is explicitly reported. Exported plans state `not_executed_by_this_guide`. [docs/native-lessons.html:166–216](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/native-lessons.html#L166-L216); [docs/portfolio/index.html:265–294](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/portfolio/index.html#L265-L294).

The previous-animation gallery loads media on an explicit click. Its preserved waveform uses decorative sine/cosine curves controlled by rate/temperature/damping sliders; it is not a thermal solver or measured telemetry. No source application or animation behavior is changed by the handbook. [docs/animations/gallery.js:1–20](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/animations/gallery.js#L1-L20); [docs/animations/waveform.html:148–209](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/animations/waveform.html#L148-L209).

Lesson/config snapshots retain `573e04d53ee0cc06f17d9984c432daad2e7bf5e6`; native catalogue provenance additionally records `b76ca31619dd2b2c8fe2e15b9bb1a53453aa3fa1`. Their historical identities are distinct from the new review source. [docs/native-lessons.json:8–19](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/native-lessons.json#L8-L19); [docs/portfolio/README.md:19–24](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/portfolio/README.md#L19-L24).

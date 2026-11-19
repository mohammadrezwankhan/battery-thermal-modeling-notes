# Setup and reproducibility

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

The native guide declares **Python 3.12 or later** and no third-party runtime packages. The review executed Python **3.12.14 on Linux**. That observed run is not a compatibility matrix for every later Python or other OS. CI selects Python `3.12`. [models/README.md:32–53](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L32-L53); [models/lumped_cell_thermal.py:1–10](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1-L10); [.github/workflows/markdown-maintenance.yml:37–43](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/markdown-maintenance.yml#L37-L43).

## Obtain the reviewed source

```bash
git clone https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes.git
cd battery-thermal-modeling-notes
git checkout --detach 37cb3c16069b21c373efc17ed202352ab69224dd
python --version
python -m unittest discover -s tests -v
python models/lumped_cell_thermal.py --help
python models/lumped_cell_thermal.py --current-a 75 --duration-s 600 --time-step-s 600 --integration-method exact-linear
```

Use that checkout for the reviewed native behavior. The new handbook files are introduced by a later documentation commit; obtain that commit separately when checking the renderer. No dependency installation is needed for native execution. Commands run from the repository root so `models` imports and relative fixture paths resolve. The [worked examples](WORKED_EXAMPLES_AND_LABS.md) record actual outputs and solver settings.

## Keep a reproducible result record

Record the source commit, Python version, operating system, exact argument vector, solver, profile SHA-256, all overridden parameters and output hashes. For a profile, retain its column order, units, sign convention, interval durations and whether each input is illustrative, measured or fitted. Use the existing [traceability matrix](../../templates/thermal-parameter-traceability-matrix.md) and [experimental-condition comparison](../../templates/experimental-condition-comparison.md). The source CLI does not itself write a full software/environment manifest. [models/lumped_cell_thermal.py:996–1117](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L996-L1117); [templates/thermal-parameter-traceability-matrix.md:1–18](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/templates/thermal-parameter-traceability-matrix.md#L1-L18).

```bash
python models/lumped_cell_thermal.py --profile-csv models/data/irregular_current_profile.csv --integration-method exact-linear --output-csv results/irregular_thermal_intervals.csv
python models/lumped_cell_thermal.py --profile-csv models/data/radiative_cooling_profile.csv --emissivity 0.85 --radiating-area-m2 0.03 --integration-method rk4 --rk4-max-step-s 0.5 --output-csv results/radiative_thermal_intervals.csv
python scripts/portfolio/validate_guide.py
```

Writers create parent directories and overwrite the chosen output file. Give distinct filenames to distinct runs. `results/` is ignored by Git; preserve useful experiment evidence deliberately outside a disposable checkout. [models/lumped_cell_thermal.py:996–1025](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L996-L1025); [models/lumped_cell_thermal.py:1065–1086](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/lumped_cell_thermal.py#L1065-L1086); [.gitignore:1–3](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.gitignore#L1-L3).

## Documentation and offline browser use

Open `docs/index.html`, `docs/native-lessons.html`, or `docs/portfolio/index.html` locally. The active browser model is self-contained; following external source links requires network access. Portfolio notes are stored in the browser's local storage when available and can be exported as a study-plan JSON. Storage is not a repository backup. [docs/index.html:147–154](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/index.html#L147-L154); [docs/portfolio/index.html:269–291](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/portfolio/index.html#L269-L291).

The new static handbook requires **Pandoc 3.1.11.1** for the byte-identical reviewed rendering and Python's standard library for its renderer. This is a documentation authoring tool, not a native-model dependency. With the documentation commit checked out:

```bash
pandoc --version
python docs/reference/build_reference.py
python docs/reference/build_reference.py --check
git diff --check
```

No authentication, external service, hardware connection or credential is required by these examples. Model and browser runs use synthetic/illustrative inputs; no measured-cell validation was performed in this review.

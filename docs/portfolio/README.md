# Battery Thermal Modeling — learning map

Battery thermal models, assumption registers and reproducible learning paths with explicit validation boundaries.

This companion organises 4 selected source-backed paths. It complements the repository's full documentation and native lessons. It does not execute its scientific or operational models.

Open `index.html` locally for search, topic filters, source/configuration inspection, personal notes and study-plan export. The guide has no network or build dependency.

Open the [offline interactive lesson lab](../index.html) and inspect its [lesson configuration](../lesson-config.json).

| Path | Learning objective | Level | First source |
| --- | --- | --- | --- |
| path-01 | Establish thermal assumptions and provenance | Foundation | [notes/modeling-assumptions.md](../../notes/modeling-assumptions.md) |
| path-02 | Inspect the constant-current reference | Foundation | [models/README.md](../../models/README.md) |
| path-03 | Inspect interval profiles and thermal boundaries | Applied | [models/data/irregular_current_profile.csv](../../models/data/irregular_current_profile.csv) |
| path-04 | Review limits and validation evidence | Applied | [tests/test_lumped_cell_thermal.py](../../tests/test_lumped_cell_thermal.py) |

## Provenance

Repository: <https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes>

Pinned source: 573e04d53ee0cc06f17d9984c432daad2e7bf5e6

Native commands and expected outputs are guidance unless accompanied by a separate execution record. Reviewed-path progress is a personal learning record.

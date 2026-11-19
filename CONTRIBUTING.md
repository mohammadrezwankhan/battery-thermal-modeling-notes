# Contributing

Contributions should make battery thermal modeling clearer, more reproducible,
or easier to validate.

## Good Contributions

- Clarify assumptions.
- Add citations to public sources.
- Improve model setup notes.
- Add validation checklists.

## Pull Request Checklist

- [ ] Claims are evidence-backed.
- [ ] Units are explicit.
- [ ] Assumptions are stated.
- [ ] No copyrighted paper text is copied.
- [ ] `python -m unittest discover -s tests -v` passes for model changes.

## Maintain the documentation package

Start at [docs/INDEX.md](docs/INDEX.md). Keep the substantive [model guide](models/README.md), notes and templates canonical for their existing subjects. Update the handbook's source locators, API/CLI inventory and worked outputs when their source changes; label proposed work separately from implemented behavior.

Use a small PR with a claim-to-source/test map, explicit units, input provenance and a reproducible command. Preserve the distinction between state-derived energy bookkeeping and independent numerical verification. A literature citation does not turn the seven example CSVs into measured validation data. Record any numerical defect for a separately scoped change.

For this static reading view, edit Markdown or CFF first, then run `python docs/reference/build_reference.py` and `python docs/reference/build_reference.py --check` with Pandoc installed. Run `python -m unittest discover -s tests -v`, `python scripts/portfolio/validate_guide.py`, local Markdown/link checks and `git diff --check`. The existing CI link command does not cover the new `docs/**` handbook; keep a separate local check until that gap is reviewed. See the [maintenance runbook](docs/maintainer/DOCS_MAINTENANCE_RUNBOOK.md).

Follow [AGENTS.md](AGENTS.md) for CI changes and preserve required contexts. Repository policy checks author/committer/co-author metadata; use the authenticated contributor's legitimate identity and obey current signature and branch rules. Source: [.github/workflows/no-codex-attribution.yml:17–99](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/no-codex-attribution.yml#L17-L99).

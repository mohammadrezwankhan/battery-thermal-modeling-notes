# Documentation maintenance runbook

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

## Canonical sources

Keep `models/README.md`, substantive `notes/`, `templates/` and `references/` as their established canonical material. Requested handbook entry points map to them and add source-specific API, derivation, verification and owner context. The source SHA in page banners describes the analyzed code, not the commit that introduces those pages. Existing native/portfolio lesson snapshots retain their separate provenance. [docs/portfolio/README.md:1–24](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/portfolio/README.md#L1-L24).

## Change checklist

1. Pin the source tree and account for every tracked entry. Separate semantic review, structural parsing, indexed historical/generated content and unsupported payloads.
2. Inspect changed functions, dataclass fields, constants, CLI registrations, input/output schemas, tests, workflows and source evidence. Update the API catalogue and unit/assumption pages together.
3. Run the native suite and affected examples. Record actual interpreter, argument vector, fixtures, output/log hashes and revision identity; do not refresh a date while retaining stale results.
4. Check local Markdown paths/anchors, pinned source line ranges, CFF declared schema and duplicate keys, lesson JSON schema, SVG XML, HTML navigation and `git diff --check`.
5. Regenerate the static reading view and compare it. Review the complete diff independently, then use ordinary guarded delivery and the existing Pages route.

Native commands and CI evidence: [CONTRIBUTING.md:13–19](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/CONTRIBUTING.md#L13-L19); [.github/workflows/markdown-maintenance.yml:42–89](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/markdown-maintenance.yml#L42-L89); [scripts/portfolio/validate_guide.py:1–33](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/scripts/portfolio/validate_guide.py#L1-L33).

## Rebuild the reading view

`docs/reference/chapters.json` fixes chapter paths, groups, labels, review date and reviewed source identity. `build_reference.py` reads only those Markdown/CFF inputs, uses Pandoc to produce HTML/MathML, rewrites local links to chapter or source targets, rejects active HTML/event attributes, and writes only `docs/reference/index.html`. `reference.css` owns presentation. Input hashes and the observed Pandoc version are embedded in the generated page.

```bash
pandoc --version
python docs/reference/build_reference.py
python docs/reference/build_reference.py --check
python -m unittest discover -s tests -v
python scripts/portfolio/validate_guide.py
git diff --check
```

The reviewed renderer uses Pandoc 3.1.11.1. A changed renderer/tool version can legitimately alter HTML; inspect the semantic and visual delta, then update the dated build record. Never edit generated HTML independently. The page has no scripts, uses native MathML and links back to existing learning surfaces. Source Markdown remains usable in GitHub without this view.

## Presentation and publication

Preserve the existing purple/cream/orange style, typography hierarchy, keyboard focus, skip navigation and reduced-motion behavior. Keep source identity and synthetic-data qualifications close to outputs. Check narrow and wide screens, table scrolling, chapter anchors, math, keyboard navigation and print output through the supported browser before claiming visual verification. Static parsing is insufficient for those claims.

The source Pages workflow publishes `docs` directly; it does not execute this renderer. Commit the reviewed generated view with its inputs. After a policy-compliant merge, tie deployment to the merged revision and inspect the actual new handbook. Preserve prior evidence and record rollback/recovery as a new reviewed change. [.github/workflows/deploy-dashboard.yml:56–82](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/deploy-dashboard.yml#L56-L82); [AGENTS.md:1–3](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/AGENTS.md#L1-L3).

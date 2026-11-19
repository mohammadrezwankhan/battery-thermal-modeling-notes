# Recovery and continuity runbook

> Reviewed 2026-11-19 against source `37cb3c16069b21c373efc17ed202352ab69224dd`. [Documentation index](../INDEX.md). This date identifies the review, not a release or deployment.

## Preserve what is needed

Retain an authorized Git mirror/export, branch/tag/rules metadata, reviewed source/candidate/merged identities, required CI and deployment receipts, canonical documentation and handbook inputs. Keep environment versions, exact commands, fixture hashes and any measured-data permission/provenance records with reproducibility evidence. `results/` is ignored and portfolio personal notes live in browser storage; neither is guaranteed by a source clone. [.gitignore:1–15](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.gitignore#L1-L15); [docs/portfolio/index.html:269–291](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/docs/portfolio/index.html#L269-L291).

## Restore and verify

1. Obtain an authorized checkout, verify its commit and tree, and preserve any existing uncommitted work. For this snapshot, the reviewed source is `37cb3c16069b21c373efc17ed202352ab69224dd`, tree `127037ea757181c6baa8db8290d2f978838dd636`.
2. Restore Python 3.12 or the specifically recorded compatible environment; run the 85-test source suite and the exact-linear reference. Compare retained fixture/output evidence, not just a plausible plot.
3. Restore the documentation commit and Pandoc 3.1.11.1 for the reviewed handbook bytes; run renderer freshness, local links, citation/schema checks and the source guide validator.
4. Confirm current GitHub account/repository access through approved mechanisms. Inspect branch protection, the actual signature ruleset, required checks/reviews and Pages environment restrictions. Do not copy old policy assumptions or disable a gate to recover.
5. Use a normal reviewed change and legitimate signing route. After merge, map the existing Pages deployment to that merged revision and inspect handbook navigation and updated content.

Source execution and publication contracts: [models/README.md:32–53](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/models/README.md#L32-L53); [.github/workflows/markdown-maintenance.yml:42–89](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/markdown-maintenance.yml#L42-L89); [.github/workflows/deploy-dashboard.yml:56–82](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/deploy-dashboard.yml#L56-L82).

## Access and fallback

Native calculations and the static local learning pages work without production accounts. The source Pages deployment uses `pages: write` and `id-token: write`; no named long-lived deployment secret is declared. Repository administrator and Pages access recovery use the platform's normal authorized account process. Do not collect, embed or manufacture credentials. [.github/workflows/deploy-dashboard.yml:61–82](https://github.com/mohammadrezwankhan/battery-thermal-modeling-notes/blob/37cb3c16069b21c373efc17ed202352ab69224dd/.github/workflows/deploy-dashboard.yml#L61-L82).

If publication access is unavailable, preserve the exact candidate, review evidence and local/GitHub-rendered Markdown while recording the unresolved deployment gate. Do not announce recovery complete until the intended publication outcome is observed. No restore drill or backup-person assignment was established by this documentation review; [BT-08](../../ROADMAP.md#bt-08--rehearse-recovery-and-publication) proposes a measured exercise.

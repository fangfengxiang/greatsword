# Greatsword website and CI reports

Website target: https://fangfengxiang.github.io/greatsword/

## One-time GitHub Pages setting

Repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
The workflow cannot reliably switch this repository setting using the currently connected GitHub integration. Until the owner enables Pages, the deployment step may fail and the website URL may return 404.

## Workflow: Greatsword Quality

Every push to `main`:

1. Static Skill package gate and benchmark dataset gate. Archive `quality-report.json`, `dataset-report.json`, package manifest and installable tarball.
2. Docker smoke and real OpenCode CLI baseline/Greatsword attempts. Each candidate uses the **same model for both conditions**. Fallback stops at first complete pair, subject to a 20-minute evaluation budget and maximum six attempted models. Archive all raw case records, model selection, combined JSON and standalone HTML.
3. Generate the public homepage and per-run evidence page; restore earlier report directories from `gh-pages`; publish the archive branch and deploy via official GitHub Pages Actions.

Report URL: `https://fangfengxiang.github.io/greatsword/reports/<run-id>/`.
Reports index: `https://fangfengxiang.github.io/greatsword/reports/`.

## What each result means

- **Static pass:** packaging and static rules passed, not behavioral improvement.
- **Dataset pass:** dataset shape validated, not case quality.
- **Docker smoke pass:** evaluation environment is runnable, not a successful model call.
- **A/B completed_ungraded:** the same model completed both CLI conditions. This is not proof Greatsword improves decisions.
- **Behavior score not_graded:** automated engineering judgment scoring has not been implemented. Never present CLI exit code as a quality score.
- **Model NONE:** no same-model A/B pair completed. See `model-selection.json` for attempted candidates.

The site is static, with no external frontend build system. The reports index reads the public GitHub Actions API to list run IDs; rate limits or unavailable API may affect the listing. Earlier runs before website publishing may not have archived report pages.

Security: publish only test prompts and outputs from the public evaluation dataset. Do not add secrets or private research material to Pages artifacts. GitHub Actions artifacts have 90-day retention; the `gh-pages` branch retains previously published static report files until explicitly cleaned.

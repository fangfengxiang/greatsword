# OpenCode A/B CLI runner

The runner executes **real OpenCode CLI commands** in a fresh temporary directory per case. Candidate runs copy only `skills/greatsword/` to `.agents/skills/greatsword/`; baseline runs have no Skill. No repository-root `AGENTS.md` or answer keys are copied.

## Local

```bash
npm install -g @opencode/cli
opencode --version
opencode models
python evals/opencode/run.py --model YOUR_AVAILABLE_MODEL --condition baseline --limit 3
python evals/opencode/run.py --model YOUR_AVAILABLE_MODEL --condition greatsword --limit 3
```

For a free model, choose an actual enabled ID from your OpenCode catalog; free access and rate limits may change. CI can optionally receive `OPENCODE_API_KEY` via GitHub Actions Secrets if your account/provider requires it.

## CI

GitHub Actions → **OpenCode A-B Evaluation** → Run workflow → supply model and number of scenarios. It installs OpenCode v2 and archives `summary.json`, per-case JSON, and standalone `report.html` for both conditions. The report is a **run/transcript report, not a correctness score**.

## Limits

- This is **OpenCode directly**, not Inspect AI; Inspect remains available for separate model-graded evaluation.
- The cases are decision prompts, not repository code-edit fixtures. Agent instruction is to avoid modifying files.
- No automated rubric scorer, token accounting, or held-out results yet.
- A zero exit code only means CLI completed, not that the engineering decision was good.
- CLI version, model availability, authentication and Skill discovery must be validated on an actual runner; do not infer skill loading merely from copying files.
- No Docker sandbox yet. Each run uses a separate temporary working directory but shares the host's OpenCode configuration; for stronger isolation use a pinned container and separate home/config directories.

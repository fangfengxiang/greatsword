# Evaluation engine selection: Inspect AI

Status: selected for integration; **not yet executed with a model**.

## Why

Greatsword tests coding-agent *behavior*, not just response similarity. [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) supports CLI evaluations, Docker sandboxes, structured `.eval` logs, and a local log viewer. [Inspect SWE](https://inspect.aisi.org.uk/tutorial.html) supports real Codex CLI / Claude Code agents. [Promptfoo](https://github.com/promptfoo/promptfoo) is a strong fallback for cheap prompt/answer checks, but not the primary executor.

## Two stages

1. **Smoke evaluation**: Inspect AI `generate()` solver with the development scenarios, no-skill vs a Greatsword system-message condition. This is a **prompt injection proxy**, not proof the actual SKILL.md loader works.
2. **Real skill evaluation**: Inspect SWE `codex_cli()` in a Docker sandbox; install `skills/greatsword/` only in candidate containers; baseline containers contain no skill. Keep the evaluator's answer keys outside both sandboxes. Use identical model, source fixture, task, tools and budget.

The development dataset is **not held out**. Reserve fresh tasks for independent validation; keep scorer criteria out of the agent context.

## CLI target

```bash
python -m pip install inspect-ai
inspect eval evals/inspect/greatsword.py --model <provider/model> -T condition=baseline --log-dir build/inspect/baseline
inspect eval evals/inspect/greatsword.py --model <provider/model> -T condition=greatsword --log-dir build/inspect/greatsword
inspect view --log-dir build/inspect
```

For the full coding-agent stage, install `inspect-swe` and run with Docker available. Do not confuse Dockerizing the Inspect CLI itself with Docker *sandboxing the agent*; Docker-in-Docker may require host socket access and security review.

## CI policy

- Static quality runs on every commit without secrets.
- Behavioral runs are manually triggered or scheduled only when model credentials and an explicit cost budget exist.
- Archive `.eval` logs and machine-readable summaries as Actions Artifacts; do not publish credentials or sensitive prompts.
- A run without model execution must be marked `not_run`; a model-graded score is not a functional correctness proof.
- Later: report baseline/candidate delta, negative-control regression, token/tool/time cost, and repeated-run variance.

References: https://inspect.aisi.org.uk/ , https://inspect.aisi.org.uk/tutorial.html , https://inspect.aisi.org.uk/log-viewer.html

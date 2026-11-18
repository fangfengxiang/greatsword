# Inspect AI development evaluation

This is the first runnable **model-response evaluation adapter**, not a Codex CLI coding-agent E2E benchmark.

## Run

```bash
python -m pip install -r evals/inspect/requirements.txt
python scripts/check_dataset.py
inspect eval evals/inspect/greatsword.py --model openai/gpt-4o-mini -T condition=baseline --log-dir build/inspect
inspect eval evals/inspect/greatsword.py --model openai/gpt-4o-mini -T condition=greatsword --log-dir build/inspect
inspect view --log-dir build/inspect
```

Provide the model provider's API key using its standard environment variable. The GitHub Actions `Greatsword Agent Evaluation (manual)` workflow requires the `OPENAI_API_KEY` repository secret and runs only when manually dispatched.

## Boundaries

- The baseline receives the scenario prompt alone; candidate receives the same prompt plus text extracted from SKILL.md via `system_message`. **This does not test real skill discovery, progressive reference loading, tool use, or repository modifications.**
- `model_graded_qa` uses the evaluator's target criteria. Its scores are subjective, can vary by grader/model, and are not equivalent to functional correctness.
- The 12 public development cases are visible and therefore not held out.
- Run both conditions with the same model, settings, budget, and preferably multiple seeds/repetitions; compare negative controls separately.
- The CI workflow produces raw Inspect `.eval` logs as artifacts. No automatic performance claims are made.
- A future second stage should use Inspect SWE/Codex CLI in Docker with real source fixtures, isolated Skill installation, executable tests, and functional scorers.

References: https://inspect.aisi.org.uk/ , https://github.com/UKGovernmentBEIS/inspect_ai

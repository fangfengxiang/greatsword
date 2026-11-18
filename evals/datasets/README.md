# Greatsword Engineering Decision Benchmark

This is a **scenario dataset**, not a training corpus or a collection of answer templates.

- `development.jsonl`: public, inspectable development scenarios. Useful for improving prompts and checking rubric feasibility; **not** an unbiased estimate of generalization.
- `holdout/`: reserved for future blind evaluations; do not add answer keys or private cases to public CI.
- `rubric.md`: stable scoring contract.
- `schema.json`: deterministic structural checks.
- `results/`: aggregate scores with reproducibility metadata, not private transcripts.

Each scenario specifies an observable engineering decision and a risk-proportionate verification boundary. These scenarios are **inspired by** reviewed open-source code, but the cases are simplified; do not claim they reproduce bugs or that their expected answers were experimentally established.

## Evaluation protocol

1. Freeze the same model, agent harness, tool permissions, source context, and budget.
2. Run without Greatsword and with Greatsword in separate clean contexts.
3. Do not expose `rubric.md`, scenario expected checks, or private holdout answers to the agent being evaluated. The evaluator may read them.
4. Grade task correctness first, then decision quality, complexity, and cost.
5. Save the skill commit/hash, scenario ID, evaluator version, and failure evidence.
6. Include low-risk negative controls to detect unnecessary process overhead.

Public development scenarios are not held-out benchmarks. The dataset is versioned with the repository; changes to prompts or rubrics should be reviewed as benchmark changes.

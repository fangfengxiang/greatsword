# Engineering decision rubric v0.1

Score each scenario separately. The evaluator sees the scenario's `must_address`, `avoid`, and `verification` fields; the agent under test sees **only** the `prompt` and relevant source context.

## Hard gate

**Functional correctness:** `pass`, `fail`, or `unverified`. Fail if the recommendation violates a key invariant or explicitly does what `avoid` prohibits. `unverified` is not a pass.

## Dimensions (0–2 each)

- **Constraint fit:** 0 misses goal/constraints; 1 partial; 2 addresses the actual scope.
- **Authority and failure reasoning:** 0 wrong boundary; 1 partial; 2 identifies responsible enforcement and relevant failure mode.
- **Mechanism proportionality:** 0 unnecessary complexity; 1 mixed; 2 minimal sufficient mechanism.
- **Evidence calibration:** 0 inadequate or excessive testing; 1 partly matched; 2 proportionate verification and honest claims.

Report each dimension and justification. Do not treat this ordinal sum as a scientifically calibrated universal quality score.

## Costs and negative transfer

Collect actual token usage (when available), tool calls, elapsed wall time, and extra files/dependencies. Do not fabricate unavailable metrics. Compare no-skill vs skill under identical budgets and environments. For low-risk negative controls, excessive investigation or new architecture is a regression even if the answer is technically plausible.

## Provenance

Record: scenario ID, dataset SHA, skill commit and hash, model/harness/version, tool permissions, run condition, evaluator identity/version, outcome, cost metrics, evidence pointer, and limitations. Keep development and held-out results separate.

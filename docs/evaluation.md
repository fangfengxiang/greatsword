# Evaluation policy

## Two distinct gates

**Static gate (automated on every push/PR):** metadata, local reference paths, expected package contents, forbidden root documents, file limits, and scenario schema. Passing this gate means *well-formed package*, not *effective skill*.

**Behavior gate (not yet implemented):** compare a fixed agent/model/harness on no-skill and Greatsword conditions. Evaluate task correctness, architecture judgment, added complexity, tool/tokens/time costs, and harm on simple tasks. Use independent held-out tasks and preserve failure traces.

## Initial task families

- Architecture: ownership, DI boundaries, cache authority.
- Correctness: concurrency, lifecycle, distributed uniqueness.
- Compatibility: protocols, temporal boundaries, security backports.
- Negative controls: simple renaming, pure-function fixes, small tests.

Do not publish scores until the actual runs are reproducible. Do not fail ordinary CI because an external model key is absent. When no behavior run occurred, report `not_run`, never `pass`.

## Reporting contract

For each behavioral run: commit SHA, skill version/hash, model, harness, task ID, baseline/candidate condition, environment, rubric version, observed outcomes, costs, and evidence locations.

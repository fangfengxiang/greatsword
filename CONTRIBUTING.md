# Contributing

1. Identify the concrete failure mode or decision-quality gap.
2. Modify the smallest relevant section of `skills/greatsword/`; do not add generic maxims.
3. Include applicability, counterexamples, and proportional verification.
4. Run `python3 scripts/check_skill.py`.
5. Describe which behavioral evaluations were run; if none, explicitly say **not run**.
6. Keep authoring docs and evaluation materials outside the installable directory.

Static checks validate packaging, not the usefulness of the Skill. Avoid introducing new tooling until justified by an actual need.

# Instructions for agents developing Greatsword

This file governs **development of this repository**. It must not be copied into the installable skill.

## Mission

Build a concise, language-neutral Agent Skill for software architecture, system design, and technical decisions. Prefer evidence-grounded decision procedures over slogans. The public positioning is: *Engineering wisdom for software architecture, system design, and technical decisions. Guided by first principles and engineering cybernetics.*

## Boundaries

- The only installable package is `skills/greatsword/`.
- Never include `AGENTS.md`, `docs/`, `evals/`, `scripts/`, or `.github/` in the package.
- Avoid project-specific assumptions, framework mandates, and universal prohibitions.
- Avoid exposing private research, credentials, confidential conversations, or unreviewed artifacts.
- Keep `SKILL.md` short. Load references only when the task warrants them.
- A simple, low-risk change should remain simple. Do not force a six-section report or full E2E testing.

## Evidence and claims

Distinguish hypotheses, documented claims, inspected code/tests, executed checks, and independently reproduced results. A test file's existence is not proof it ran. Link source evidence when material; describe its limits. Do not claim measured skill improvements without controlled agent runs.

## Change procedure

For each meaningful skill edit: state the failure mode or improvement target, make the smallest edit, run `python3 scripts/check_skill.py`, record whether behavior evaluation was actually run, and inspect for negative transfer or unnecessary work. Never represent static checks as quality benchmark results.

See `docs/skill-design.md` and `docs/evaluation.md`.

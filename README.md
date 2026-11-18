# Greatsword

**Engineering wisdom for software architecture, system design, and technical decisions. Guided by first principles and engineering cybernetics.**

Greatsword is an Agent Skill for making proportionate, evidence-grounded engineering decisions. It is not a mandatory architecture review for every code change.

## Install

Install **only** the `skills/greatsword/` directory using an Agent Skills-compatible installer that supports subdirectory selection. For manual installation, copy that directory to your agent's skills directory, retaining `SKILL.md` and `references/`.

Do **not** install the repository root: `AGENTS.md`, `docs/`, `evals/`, `scripts/`, and `.github/` are authoring and validation materials, not part of the skill.

## Development

- [Authoring instructions](AGENTS.md)
- [Design requirements](docs/skill-design.md)
- [Evaluation plan](docs/evaluation.md)
- [Installable skill](skills/greatsword/SKILL.md)

## Quality

`python3 scripts/check_skill.py` validates the skill structure, links, and package isolation. GitHub Actions runs it on pushes and pull requests. This is **static validation**, not proof that the skill improves agent behavior. Real-agent evaluations require controlled no-skill comparisons and are tracked separately.

## Status

Early public draft (v0.1). Evidence-based principles and the evaluation harness are being developed iteratively. Research notes are kept separately; the published skill contains only reviewed, generalizable guidance.

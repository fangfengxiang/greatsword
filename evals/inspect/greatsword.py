"""Inspect AI development-set evaluation (answer-quality proxy, not coding-agent E2E).

Run:
  inspect eval evals/inspect/greatsword.py --model openai/gpt-4o-mini -T condition=baseline
  inspect eval evals/inspect/greatsword.py --model openai/gpt-4o-mini -T condition=greatsword

Requires inspect-ai and model credentials. This module does NOT run Codex CLI.
"""
import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import generate, system_message

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "evals" / "datasets" / "development.jsonl"
SKILL = ROOT / "skills" / "greatsword" / "SKILL.md"


def scenarios():
    result = []
    for line in DATA.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        # Only the prompt is visible to the solver. Criteria remain evaluator-side.
        target = (
            "A good answer must address: " + "; ".join(row["must_address"])
            + ". Avoid: " + "; ".join(row["avoid"])
            + ". Verification should be proportional: " + row["verification"]
        )
        result.append(Sample(id=row["id"], input=row["prompt"], target=target))
    return result


def skill_guidance():
    text = SKILL.read_text(encoding="utf-8")
    # This is a proxy: injects the SKILL.md instructions, not an actual skill loader.
    return text.split("---", 2)[-1].strip()


@task
def greatsword(condition: str = "baseline"):
    if condition not in {"baseline", "greatsword"}:
        raise ValueError("condition must be baseline or greatsword")
    solver = [generate()]
    if condition == "greatsword":
        solver = [system_message(skill_guidance()), generate()]
    return Task(
        dataset=scenarios(),
        solver=solver,
        scorer=model_graded_qa(),
        name=f"greatsword-{condition}",
    )

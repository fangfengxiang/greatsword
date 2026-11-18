#!/usr/bin/env python3
"""Dependency-free validation of the installable Greatsword package."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "greatsword"
ALLOWED = {
    "SKILL.md",
    "references/responsibility-boundary.md",
    "references/invariant-lifecycle.md",
    "references/contract-compatibility.md",
    "references/controlled-change.md",
    "references/technology-selection.md",
}
errors = []
def check(ok, msg):
    if not ok:
        errors.append(msg)

actual = {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob("*") if p.is_file()}
check(actual == ALLOWED, f"Package allowlist mismatch: missing={sorted(ALLOWED-actual)} unexpected={sorted(actual-ALLOWED)}")
entry = PACKAGE / "SKILL.md"
if entry.exists():
    body = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", body, re.S)
    check(bool(match), "SKILL.md must start with YAML frontmatter")
    if match:
        fields = dict(re.findall(r"^([a-z][a-z0-9_-]*):\s*(.+)$", match.group(1), re.M))
        check(fields.get("name") == "greatsword", "Skill name must be greatsword")
        check(bool(fields.get("description")), "Skill description is required")
    for target in re.findall(r"\]\(([^)]+)\)", body):
        if "://" not in target and not target.startswith("#"):
            check((entry.parent / target.split("#")[0]).is_file(), f"Broken local reference: {target}")
    check(len(body.splitlines()) <= 120, "SKILL.md exceeds 120 lines")
for rel in sorted(actual):
    path = PACKAGE / rel
    check(path.stat().st_size <= 25000, f"Reference too large: {rel}")
    text = path.read_text(encoding="utf-8")
    check("BEGIN PRIVATE KEY" not in text, f"Possible private key in {rel}")
    check(not re.search(r"(?i)(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}", text), f"Possible GitHub token in {rel}")
for forbidden in ("AGENTS.md", "docs", "evals", "scripts", ".github"):
    check(not (PACKAGE / forbidden).exists(), f"Authoring content inside package: {forbidden}")
report = {
    "schema_version": 1,
    "gate": "static",
    "status": "fail" if errors else "pass",
    "behavior_evaluation": "not_run",
    "package_root": "skills/greatsword",
    "files": sorted(actual),
    "errors": errors,
}
out = ROOT / "build"
out.mkdir(exist_ok=True)
(out / "quality-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(bool(errors))

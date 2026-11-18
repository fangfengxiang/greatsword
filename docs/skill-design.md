# Greatsword design requirements

## Purpose

Teach a coding agent *when and how to make an engineering judgment*, not a catalog of every engineering technique.

## Research-informed requirements

- **Resource2Skill:** transform source material into retrievable, executable decision procedures with traceable evidence; avoid dumping raw notes into the skill.
- **SkillOpt:** prefer small, reviewable edits; compare candidate to baseline on held-out tasks; record rejected changes.
- **Agent Skills Can Be Harmful:** include anti-triggers and stop conditions; minimize verification overhead and negative transfer.
- **Agent Skills format:** use a concise `SKILL.md` entry and optional on-demand `references/`.

These are design inspirations, not proof that Greatsword improves outcomes.

## Every decision reference should answer

1. Trigger: when is this relevant?
2. Anti-trigger: when is it unnecessary?
3. Questions: what facts must be established?
4. Procedure: what is the minimum useful decision sequence?
5. Failure modes: what can invalidate the recommendation?
6. Evidence: what verification is proportional to the risk?
7. Stop condition: when is the decision sufficiently supported?

## Packaging

The distributable boundary is `skills/greatsword/`. Keep authoring rules, roadmap, tests, benchmarks, and CI outside that boundary. Static checks should verify both the directory allowlist and the generated distribution manifest.

## Roadmap

v0.1: short entry, four decision references, static package validation.
v0.2: reproducible scenario definitions and scoring rubrics.
v0.3: controlled no-skill vs skill runs with costs and regression reporting.
v1.0: only after measured usefulness and negative-transfer review.

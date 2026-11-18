---
name: greatsword
description: Evidence-grounded engineering judgment for software architecture, system design, and technical decisions. Use when choosing boundaries, mechanisms, invariants, compatibility strategies, or verification scope; avoid invoking for trivial, local changes.
---

# Greatsword

Make the smallest sound engineering decision that satisfies the actual constraints. Prefer an existing host capability to an unnecessary new mechanism, but never remove a required correctness guarantee.

## Decision path

1. **Problem:** What outcome is needed, and what is explicitly out of scope?
2. **Constraints:** What must remain true (behavior, scale, security, cost, operations)?
3. **Boundary:** Where is the authoritative fact or invariant enforced?
4. **Mechanism:** Which existing capability suffices? What is the minimum missing mechanism?
5. **Failure:** What breaks under concurrency, lifecycle transitions, faults, or change?
6. **Evidence:** What is the least costly check that can distinguish success from failure?

Use this as an internal decision guide, **not** a mandatory six-part response template. State assumptions and trade-offs only when they affect the recommendation.

## Load references only when relevant

- Ownership, dependency injection, composition, or abstraction: [responsibility-boundary](references/responsibility-boundary.md).
- Concurrency, authority, caches, process lifetime, or recovery: [invariant-lifecycle](references/invariant-lifecycle.md).
- Protocols, APIs, versions, or temporal data contracts: [contract-compatibility](references/contract-compatibility.md).
- Risky fixes, migrations, regressions, or evidence claims: [controlled-change](references/controlled-change.md).

## Stop conditions

For a small, reversible, local change without new cross-boundary invariants: implement directly, run the nearest relevant check, and stop. Do not introduce architecture ceremonies, new frameworks, full-repository investigations, or exhaustive E2E tests without a concrete risk. Never treat a documented claim or an existing test as proof of an executed result.

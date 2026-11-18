# Responsibility and boundary

**Use when:** designing interfaces, dependency ownership, adapters, domain boundaries, or framework integration.

**Do not use when:** a local implementation change has no ownership or boundary decision.

1. Identify the domain responsibility and the component that must own it.
2. Separate policy (what should happen) from mechanism (how it runs).
3. Inspect existing language/runtime/host capabilities before adding infrastructure.
4. Prefer explicit composition where it is sufficient; add indirection only to satisfy a real constraint.
5. Check that an injected interface does not silently delegate away an unverified safety obligation.

**Failure modes:** a repository interface that promises atomicity without an atomic implementation; a context object becoming an implicit dependency locator; over-abstraction for a single stable implementation.

**Evidence:** inspect the actual caller, implementation, and boundary tests. Stop once ownership and contract are explicit and the change can be checked locally.

Research examples: Luminary, lua-slds, Linklet. These are motivating cases, not universal architecture mandates.

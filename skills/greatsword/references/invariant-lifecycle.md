# Invariants and lifecycle

**Use when:** correctness depends on concurrency, cache invalidation, process reuse, shutdown, recovery, or distributed identity.

**Do not use when:** no shared state, cross-process behavior, or lifecycle-sensitive invariant is involved.

1. Write the invariant as an observable statement, including scope (process, node, cluster).
2. Find the authoritative enforcement point; distinguish cache and derived views.
3. Identify atomic operations and ordering requirements.
4. Examine crash, restart, retry, reuse, and stale-reader paths.
5. Verify at the boundary that can actually violate the invariant.

**Failure modes:** process-local uniqueness mistaken for distributed uniqueness; atomic publication mistaken for safe reader lifetime; invalidation signal without propagation and fallback; interface promises without provider guarantees.

**Evidence:** concurrency or fault-injection checks only where warranted. A single-process mock does not prove distributed behavior. Stop when the stated invariant and failure model have proportional evidence.

Research examples: Beacon, RevIdEngine, Linklet.

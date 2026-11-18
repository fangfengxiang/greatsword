# Controlled change and evidence

**Use when:** a change is high risk, difficult to reverse, security-sensitive, or a correctness claim needs stronger evidence.

**Do not use when:** a small, reversible change can be adequately checked with a focused test.

1. Pin the original behavior, version, constraints, and failure mechanism.
2. Classify what must change and what must remain stable.
   For performance or routing changes, record workload shape (including key distribution), critical-path dependencies, fault domain, and the relevant runtime/database version before selecting an algorithm or optimization.
3. Define a negative control (old failure) and a positive control (normal behavior).
4. Select the least intrusive observation points and ensure their semantics match the claim.
5. Check that tests actually execute and can fail when the target property is violated.
6. Record provenance, observations, assertion gates, limitations, and reproduction steps.
7. Separate execution completion, test assertions, business correctness, and quality scores; a successful workflow or HTTP response does not establish the stronger claims.
8. When a change spans artifacts or teams, identify which versioned contract is authoritative and verify that dependent outputs refer to the same version.

**Failure modes:** a test name claiming more than its assertion; instrumentation changing behavior; Python assertions disabled by optimization; passing a report with incomplete coverage; a workaround that suppresses legitimate behavior.

**Evidence:** distinguish docs, source, CI wiring, execution traces, and independent reproduction. For security and concurrency claims, avoid extrapolating beyond tested environments.

Research examples: PHP security backports and php-security-e2e. Stop when risk-proportionate evidence supports the specific claim; do not insist on exhaustive testing by default.

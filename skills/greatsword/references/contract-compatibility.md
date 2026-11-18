# Contract and compatibility

**Use when:** changing protocols, public APIs, serialized formats, historical data semantics, or supported versions.

**Do not use when:** a private local function changes without an external or temporal contract.

1. Name the observable contract: inputs, outputs, errors, ordering, and lifetime.
2. Separate semantic invariants from version-specific implementation details.
3. Identify both positive behavior and rejected/invalid cases.
4. Pin the actual versions and examine the change surface; do not assume mechanical backports.
5. Choose tests that exercise consumers, not only isolated implementations.
6. For multi-source or temporal data, specify precedence, fallback, validity interval, and conflict behavior; never let the newest value silently overwrite historical meaning.
7. For protocol adapters, verify framing, serialization, errors, and actual peer interoperability; source-level API resemblance is not wire compatibility.

**Failure modes:** protocol translation that loses error meaning; version-specific memory layout assumptions; temporal data fallback that changes meaning at a boundary.

**Evidence:** cross-version or cross-language E2E only when compatibility actually crosses those boundaries. Stop when supported versions and behavior are unambiguous.

Research examples: Yar bridge, Chinese ID Validator, PHP backports.

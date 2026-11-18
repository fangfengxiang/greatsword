# Technology selection and trade-offs

**Use when:** choosing an open-source product, platform, framework, build-vs-buy path, or the scope of a custom mechanism.

**Do not use when:** an existing dependency already satisfies a local task and no meaningful selection decision exists.

1. Define the required **end-to-end capability**, not a feature checklist detached from the workflow. Identify the business object, lifecycle, users, and operational obligations.
2. Classify each candidate honestly: library, adapter, execution engine, control plane, or complete product. Do not treat a capable node as an end-to-end system.
3. Separate must-have constraints from preferences: data ownership, private deployment, permissions, integration, reliability, extensibility, staffing, and total operating cost.
4. Inspect the actual edition, version, source, license, deployment dependencies, and integration surface. Distinguish documented features from code evidence and a working deployment.
5. Compare the **smallest sufficient** options, including using existing infrastructure and doing nothing. Count custom glue, migration, incident recovery, and ongoing ownership—not just initial code volume.
6. Identify the disqualifying gap and the condition under which the decision should be revisited. Validate the riskiest assumption with a focused proof before committing.

**Failure modes:** picking a UI component when a governed product is required; selecting a workflow engine for a single deterministic trigger; mistaking open source for unrestricted self-hosting features; building distributed storage before proving existing databases insufficient; assuming an Agent framework should own domain metrics or business verification.

**Evidence:** a decision matrix with explicit constraints, version-specific evidence, a targeted proof for the largest uncertainty, and a clear rollback/exit path. Stop once a sufficient candidate has been validated; do not benchmark every alternative without a decision-changing reason.

Research examples: AI-Native delivery workbench vs harness nodes; Rill/Lightdash/Graphic Walker; DataWorks vs open-source orchestrators; Linklet storage; Agent evaluation runners vs observability platforms. These are **context-specific decisions**, not permanent rankings or endorsements.

# DeepInterview Documentation Map

Start with the smallest maintained authority for the question at hand. The
repository, not this harness, owns product behavior.

## Product And Project Guidance

- [`../README.md`](../README.md): product overview, installation, maintenance,
  and development entry points.
- [`../README.vi.md`](../README.vi.md): Vietnamese product overview.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md): setup, monorepo ownership,
  provider-adapter, playbook, style, and test conventions.
- [`../SECURITY.md`](../SECURITY.md): secrets, disclosure, and security
  boundaries.
- [`ARCHITECTURE.md`](ARCHITECTURE.md): current product, code, state, update,
  and ownership boundaries.
- [`DEPLOY.md`](DEPLOY.md): deployment, Compose, observability, and manual
  release gates.
- [`LOCAL_MODELS.md`](LOCAL_MODELS.md): local model and real-time transport
  setup, with its evidence limits.
- [`OPENROUTER_AND_CPU_ONLY.md`](OPENROUTER_AND_CPU_ONLY.md): remote gateway and
  CPU-only constraints.
- [`AVATARS.md`](AVATARS.md): avatar assets and rendering guidance.
- [`GOOD_FIRST_ISSUES.md`](GOOD_FIRST_ISSUES.md): scoped contribution ideas.
- [`../skills/SCHEMA.md`](../skills/SCHEMA.md): playbook and rubric schema.
- [`../services/lightrag/README.md`](../services/lightrag/README.md): knowledge
  sidecar behavior and backend boundary.

## Repository-Owned Collaboration Guidance

- [`WORKFLOW.md`](WORKFLOW.md): request shape, authority, planning, delegation,
  operation, validation, and completion.
- [`HARNESS.md`](HARNESS.md): the checked-in harness contract and known
  residuals.
- [`decisions/README.md`](decisions/README.md): lasting choices future work
  must inherit.
- [`plans/README.md`](plans/README.md): durable working memory and lifecycle.
- [`plans/active/README.md`](plans/active/README.md): current plan location.
- [`plans/deferred/README.md`](plans/deferred/README.md): intentionally paused
  plans and resume rules.
- [`plans/completed/README.md`](plans/completed/README.md): validated historical
  plans.
- [`runbooks/README.md`](runbooks/README.md): verified offline, local, Compose,
  and deployment runbook index.
- [`patterns/encoding-invariants.md`](patterns/encoding-invariants.md): turn
  accepted architecture, reliability, security, and quality rules into native
  mechanical validation.
- [`templates/`](templates/): optional decision, plan, runbook, and
  Harness-improvement structures.
- [`../.agents/skills/`](../.agents/skills/): the four checked-in skills and
  their evidence references/scripts.

## Authority And Evidence

Maintained product READMEs and product docs establish intent; architecture,
deployment, contributor, security, and accepted decisions constrain it; source,
tests, schemas, CI, and configuration show implementation; observed runtime
signals show what happened in a named environment. Classify claims as
Authoritative, Observed, Derived, Decision required, or Unknown. Keep
offline/mock, local-process, Compose, real-provider/LiveKit, and hosted evidence
separate.

The shared-contract path is:

```text
packages/shared/src
  -> apps/agent/shared_models.py
  -> packages/shared/schema
  -> TypeScript round-trip/invariant tests
  -> Python parity/round-trip tests
  -> persisted fixture/default compatibility
```

The `.agents/skills` tree and these harness docs are checked in as
DeepInterview guidance. They do not replace product authority owned by the
application modules, add a task database, or create an external installer
lifecycle.

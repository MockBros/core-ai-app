# DeepInterview Repository Workflow

DeepInterview product behavior, architecture, decisions, plans, code, tests,
CI, and runtime signals are the system of record. The checked-in harness adds
collaboration and evidence discipline; it does not create product policy.

## Authority And Repository Map

Read the root [`AGENTS.md`](../AGENTS.md) and use the
[documentation map](README.md). Resolve claims in this order:

1. maintained product READMEs and product documents;
2. architecture, deployment/local-model, contributor, security, and accepted
   decision documents;
3. source, tests, schemas, CI, and configuration;
4. observed runtime evidence from the named environment.

The ownership map is:

| Path | Boundary |
| --- | --- |
| `apps/web` | Next.js UI, setup/session/interview/report/prep routes, Supabase helpers, uploads, and LiveKit token/browser-facing endpoints. |
| `apps/agent` | FastAPI API, prep/live/post/coach workers, persistence adapters, tracing, and provider adapters. |
| `services/lightrag` | Knowledge sidecar and NaiveRAG/LightRAG backends. |
| `packages/shared` | TypeScript/Zod contract source, generated schemas, and cross-language compatibility. |
| `cli` | Repository setup, skill-pack, avatar, and trace commands. |
| `skills` | Versioned interview playbooks and rubrics. |
| `supabase` | Database, auth, storage, and migrations. |
| `scripts` | Setup, development, release, evidence, and avatar support. |
| `docker-compose.yml` | Compose services and local integration syntax. |

When a shared contract changes, update and prove this sequence exactly:

```text
packages/shared/src
  -> apps/agent/shared_models.py
  -> packages/shared/schema
  -> TypeScript round-trip/invariant tests
  -> Python parity/round-trip tests
  -> persisted fixture/default compatibility
```

The concrete Pydantic mirror is under
`apps/agent/src/deepinterview_agent/shared_models.py`. A source or test can
show current behavior without authorizing a new externally observable policy.

## Choose The Work Shape

### Read-Only Request

For an answer, explanation, review, diagnosis, plan, or status report, inspect
only what is needed and change nothing. Discovery does not authorize a fix.

### Bounded Change

Restate the outcome, inspect authority, implementation, ownership, and proof;
make the smallest coherent change; run focused checks; and report changed paths,
evidence, unavailable prerequisites, residual risks, and unattempted work. No
parallel lifecycle record is required for a one-session bounded change.

### Durable Planned Change

Use one plan in [`plans/active/`](plans/active/) when work spans sessions,
coordinates contributors, has meaningful dependencies, needs recovery, or is
unsafe to resume from a diff alone. Use
[`templates/exec-plan.md`](templates/exec-plan.md); keep outcome, context,
approach, risks, progress, decisions, and validation in that file. Move it to
[`plans/deferred/`](plans/deferred/) when the work is intentionally paused
before its outcome and evidence are complete. Record the deferral date, reason,
and resume condition in the plan; deferred plans are retained context, not
active work instructions. Move the plan back to `plans/active/` before
resuming, and move it to [`plans/completed/`](plans/completed/) only after the
requested outcome and evidence are recorded.

### Improve The Harness

During ordinary work, report reusable agent friction without changing this
harness. When the user explicitly invokes `$improve-harness`, use
[`templates/harness-improvement.md`](templates/harness-improvement.md) to
preserve the baseline, locate the earliest owner, apply one bounded authorized
intervention, and require a materially equivalent fresh rerun before claiming
improvement.

## Human Judgment And Authority Gate

Before editing, identify authority for each new externally observable rule. If
materially different product, safety, compatibility, credential, cleanup, or
retention choices remain open, stop and request the smallest decision.
Configurable defaults, implementation patterns, tests, and task prompts are not
authority by themselves.

For architecture, reliability, security, or quality invariants, follow the
[encoding pattern](patterns/encoding-invariants.md): locate accepted authority,
define allowed and forbidden behavior, reuse the native validation owner, and
prove both directions. Do not install hooks or change CI, merge policy, or
branch protection without separate authorization.

## Evidence Modes And Validation Ladder

Label evidence by its operating mode:

| Mode | Boundary it can prove |
| --- | --- |
| **Offline/mock** | Deterministic local behavior and mock-provider paths without external services or provider credentials. |
| **Local-process** | Interfaces and correlations across separately started local processes. |
| **Compose** | Compose syntax, image/build behavior, or an owned container stack; syntax is not runtime readiness. |
| **Real-provider/LiveKit** | A named provider, LiveKit room, media/microphone path, or other real integration boundary in its environment. |
| **Hosted** | A deployed web, agent, sidecar, managed-data, or hosted-provider path observed after deployment. |

Use the narrowest proof that matches the claim. For the shared boundary, the
validation ladder is contract source, generated schema, TypeScript checks,
Python parity/round-trip checks, persisted-fixture compatibility, then the
relevant interface mode. For sidecar or Compose changes, add sidecar tests and
Compose syntax/configuration checks; they do not prove a real LightRAG backend,
provider, LiveKit session, or hosted readiness.

Plans, checklists, CI syntax, image builds, and passing proxies do not prove a
real user-visible outcome by themselves. Record unavailable `uv`, Docker,
provider, LiveKit, device, or hosted evidence as a limitation.

## Delegation And Handoff

Delegate bounded work by module or evidence lane. Name one owner per edited file;
the owner inspects and changes only that file within the assigned scope. Each
handoff includes exact changed paths, authority consulted, validation commands
and observed results, unavailable evidence, unattempted work, and residual
risks. Preserve unrelated tracked and untracked changes. Escalate overlapping
edits, conflicts, insufficient authority, or ambiguous product intent to the
parent agent instead of overwriting, guessing, or rebasing another worker's
changes.

## Operate The Application

When a task requires the real application:

1. Find the maintained DeepInterview runbook and verify prerequisites and
   ownership.
2. Start only an isolated instance and identify its project, processes,
   services, ports, and writable state.
3. Prove readiness through the relevant interface; a liveness endpoint is not
   dependency or provider readiness.
4. Create known state, exercise the real interface, and inspect correlated
   runtime evidence.
5. Validate the outcome, then stop only resources owned by this run when an
   existing runbook authorizes that cleanup.

The [runbook index](runbooks/README.md) links current sources. If no verified
runbook exists, inspect authority and report or propose the missing guidance;
do not invent commands, credentials, cleanup obligations, or product policy.

## Completion Standard

A change is complete when the outcome exists or its blocker is explicit,
repository truth remains current, behavior-appropriate proof passed or its gap
is disclosed, any required plan is current, and the report separates observed
facts, policy, unavailable evidence, residual risks, and unattempted work.
Descriptions and checklists do not replace observed proof.

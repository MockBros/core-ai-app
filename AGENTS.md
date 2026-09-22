# DeepInterview Agent Instructions

<!-- HARNESS:BEGIN -->
## Harness

Start with the requested outcome and use the DeepInterview repository as the
system of record. Read [`docs/WORKFLOW.md`](docs/WORKFLOW.md) and
[`docs/HARNESS.md`](docs/HARNESS.md), then only the relevant product,
architecture, plan, code, and validation material.

- Answers, explanations, reviews, diagnoses, plans, and status reports are
  read-only. Inspect only what is needed; change nothing.
- For a bounded change, inspect affected behavior and proof, implement, and
  validate. No task database, installer, or control-plane operation is
  required.
- Use one repository-owned plan in [`docs/plans/active/`](docs/plans/active/)
  when work spans sessions, coordinates contributors, has dependencies, or
  needs recovery. If the work is intentionally paused, record the deferral
  date, reason, and resume condition, then move the plan to
  [`docs/plans/deferred/`](docs/plans/deferred/). Return it to `active/` before
  resuming; move it to `docs/plans/completed/` only after validation is
  recorded.
- Before editing, identify repository authority for each new externally
  observable policy. If materially different choices remain open, stop before
  edits; configurable defaults are not authority.
- For architecture, reliability, security, or quality invariant work, read
  `docs/patterns/encoding-invariants.md` and enforce only accepted rules.
- Report reusable agent friction. Change guidance, tools, runbooks, or validation
  for that purpose only when explicitly asked to use `$improve-harness`.
- Also pause when product intent remains ambiguous, recovery is difficult,
  validation is weakened, or authority is insufficient.
- Claim completion only with executable or observable evidence. Report
  outcome, changes, validation, unavailable evidence, and residual risks.

Harness has no task database or orchestration lifecycle. Use repository plans,
Git, tests, runtime signals, and the Codex task tree as the collaboration
record; do not create parallel control-plane state.
<!-- HARNESS:END -->

## DeepInterview Authority And Ownership

DeepInterview is a pnpm/Turborepo monorepo with a Python agent and knowledge
sidecar. Resolve a claim in this order:

1. maintained product READMEs and product documents;
2. architecture, deployment/local-model, contributor, security, and accepted
   decision documents;
3. source, tests, schemas, CI, and configuration;
4. observed runtime evidence from the named environment.

Code, tests, defaults, and a task prompt prove current behavior or a scoped
request; they do not silently become product policy. Keep facts, policy,
unavailable evidence, and residual risks separate in handoffs and completion
reports.

| Path | Ownership boundary |
| --- | --- |
| `apps/web` | Next.js UI, setup/session/interview/report/prep routes, Supabase helpers, uploads, and LiveKit token/browser-facing endpoints. |
| `apps/agent` | FastAPI API, prep/live/post/coach workers, persistence adapters, tracing, and provider boundaries. |
| `services/lightrag` | FastAPI knowledge sidecar and its NaiveRAG/LightRAG backend boundary. |
| `packages/shared` | TypeScript/Zod contract source, generated schemas, and cross-language compatibility. |
| `cli` | Repository checkout setup, skill-pack, avatar, and trace commands. |
| `skills` | Versioned interview playbooks and rubrics with Markdown/YAML frontmatter. |
| `supabase` | Database, auth, storage, and migration surfaces owned by the repository. |
| `scripts` | Setup, development, release, evidence, and avatar support scripts. |
| `docker-compose.yml` | Compose service definitions and local integration syntax; syntax is not runtime or provider proof. |

When a contract changes, preserve this update sequence:

```text
packages/shared/src
  -> apps/agent/shared_models.py
  -> packages/shared/schema
  -> TypeScript round-trip/invariant tests
  -> Python parity/round-trip tests
  -> persisted fixture/default compatibility
```

The repository's actual Pydantic module is under
`apps/agent/src/deepinterview_agent/shared_models.py`; the sequence names the
contract role, not permission to skip the generated schema or compatibility
checks.

## Operating Modes And Evidence

Label evidence by the mode that produced it. Offline/mock tests establish
deterministic local behavior; local-process runs exercise separately started
services; Compose checks exercise container configuration or an owned stack;
real-provider/LiveKit runs exercise provider, media, or microphone boundaries;
hosted evidence exercises deployed infrastructure. Do not use one label as a
claim for another mode.

## Collaboration And Handoff

Delegate by module or evidence lane. Before work starts, name one owner for
each file being edited. A handoff names the exact changed paths, authority
consulted, validation commands and observed results, unavailable evidence,
unattempted work, and residual risks. Preserve unrelated tracked and
untracked changes. Escalate overlapping edits, authority conflicts, or
ambiguous product choices to the parent agent instead of guessing or rebasing
another contributor's work.

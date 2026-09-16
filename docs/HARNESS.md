# DeepInterview Harness Contract

This repository uses a small, checked-in collaboration harness. The
`.agents/skills/` tree and the guidance under `docs/` are repository-owned and
authoritative for agent workflow, evidence handling, and handoff boundaries.
They describe how to work with DeepInterview; they do not replace product
contracts or change application behavior.

## Installed-Core Model

The installed core is the committed root [`AGENTS.md`](../AGENTS.md), the four
skills under [`../.agents/skills/`](../.agents/skills/), and the linked workflow,
pattern, plan, decision, runbook, and template documents. There is no updater,
installer, task database, generated lifecycle registry, or
`.harness-core/manifest.json` in this tree. The `HARNESS:BEGIN` and
`HARNESS:END` markers in `AGENTS.md` are advisory boundaries for managed
guidance; their presence is not evidence that an external installer ran.

Use [`WORKFLOW.md`](WORKFLOW.md) for operating rules and
[`plans/active/`](plans/active/) for durable work that needs recovery or
coordination. Git, tests, runtime signals, and the Codex task tree are the
collaboration record.

## Authority And Claim Classification

Use maintained DeepInterview product READMEs and product documents first,
followed by architecture/deployment/local-model, contributor, security, and
accepted decision documents. Source, tests, schemas, CI, and configuration show
implementation; observed runtime evidence shows a named environment. Classify
each claim as:

- **Authoritative:** an accepted instruction, contract, decision, or maintained
  procedure states what must happen.
- **Observed:** source, configuration, or tests show current behavior.
- **Derived:** a direct consequence of verified implementation or configuration.
- **Decision required:** materially different normative choices remain open.
- **Unknown:** available evidence cannot establish the answer.

Do not turn an observed default, a passing proxy, or a task prompt into product
policy. Separate observed facts, policy, unavailable evidence, and residual risks
in every handoff and completion report.

## Module Ownership

| Module | Owned boundary |
| --- | --- |
| `apps/web` | Next.js UI, setup/session/interview/report/prep routes, Supabase helpers, uploads, and LiveKit token/browser-facing endpoints. |
| `apps/agent` | FastAPI API, prep/live/post/coach workers, persistence adapters, tracing, and provider adapters. |
| `services/lightrag` | FastAPI knowledge sidecar and NaiveRAG/LightRAG backend boundary. |
| `packages/shared` | TypeScript/Zod contract source, generated JSON Schemas, and cross-language compatibility. |
| `cli` | Repository checkout setup, skill-pack, avatar, and trace commands. |
| `skills` | Versioned interview playbooks and rubrics with Markdown/YAML frontmatter. |
| `supabase` | Database, auth, storage, and migration surfaces. |
| `scripts` | Setup, development, release, evidence, and avatar support scripts. |
| `docker-compose.yml` | Compose definitions and local integration syntax; syntax or image-build evidence is not runtime/provider proof. |

For a contract change, keep the complete update and proof sequence visible:

```text
packages/shared/src
  -> apps/agent/shared_models.py
  -> packages/shared/schema
  -> TypeScript round-trip/invariant tests
  -> Python parity/round-trip tests
  -> persisted fixture/default compatibility
```

The concrete Pydantic module currently lives at
`apps/agent/src/deepinterview_agent/shared_models.py`. Do not skip generated
schemas, parity tests, round-trip tests, or persisted-fixture compatibility.

## Operating Modes And Evidence

Use one explicit label for every result:

| Label | What it can establish |
| --- | --- |
| **Offline/mock** | Deterministic local code and mock-provider behavior without external services or provider credentials. |
| **Local-process** | Behavior across separately started local processes and their observed interfaces. |
| **Compose** | Compose configuration, image/build behavior, or an owned container stack; `docker compose config` alone is syntax evidence. |
| **Real-provider/LiveKit** | A named provider, LiveKit room, media path, microphone, or other real integration boundary exercised in its environment. |
| **Hosted** | A deployed web, agent, sidecar, managed data, or hosted-provider path observed after deployment. |

Do not report offline tests as provider, LiveKit, hosted, real-LightRAG, or
production readiness. A missing `uv`, Docker daemon, provider credential, or
device is unavailable evidence, not permission to substitute a weaker label.

## Collaboration Protocol

Delegation is bounded by module or evidence lane. Name one owner for each file
before editing it. Each worker hands back exact changed paths, authority
consulted, validation commands and observed results, unavailable evidence,
unattempted work, and residual risks. Preserve unrelated tracked and untracked
changes. Escalate overlapping edits, authority conflicts, recovery hazards, or
ambiguous product choices to the parent agent; do not guess, overwrite, or
rebase another contributor's work.

## Known Residuals

These are explicit current limits, not new policy or acceptance claims:

- NaiveRAG is the functional sidecar default and is in-memory/deterministic.
- The real LightRAG backend is not implemented.
- Health endpoints are liveness-only; they do not prove dependency or provider
  readiness.
- Session and trace reads are capability-based paths, not a universal auth or
  hosted-security guarantee.
- Local Compose model URL wiring is incomplete; a local model process may need
  separate configuration and cannot be assumed reachable by service name.
- This host may lack `uv`, a Docker daemon, provider credentials, or a real
  LiveKit/device environment.

Read the maintained DeepInterview runbooks and service documentation for the exact path;
this file records boundaries and limits rather than inventing commands,
credentials, cleanup obligations, retention policy, or deployment state.

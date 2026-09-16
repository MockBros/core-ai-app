# DeepInterview agent

`apps/agent` is the Python 3.11+ runtime for the FastAPI API, the prep and
post pipelines, and the optional LiveKit workers. Read the repository workflow
in [`docs/WORKFLOW.md`](../../docs/WORKFLOW.md) before making changes here.

## Runtime map

- `src/deepinterview_agent/app.py` builds the FastAPI application. `/health` is
  a liveness response. The guarded write routes are `/api/prep`, `/api/score`,
  `/api/coach/plan`, `/api/coach/chat`, and `/api/kb/{ingest,query}`. The
  session read is `GET /api/session/{session_id}`; the worker's
  `POST /api/session/{session_id}/live-result` is an internal write-back. The
  trace viewer exposes read-only `GET /api/traces` and
  `GET /api/traces/{trace_id}`.
- `prep/` is the current LangGraph graph: CV extraction, CV/JD analysis and
  company research fan out, then gap matching and question planning join the
  result. `run_prep_for_session` persists the `InterviewContext` and marks the
  session `ready` (or `rejected`/`error`) while the API route returns a
  `session_id` promptly.
- `worker.py` is a separate, optional LiveKit process. It loads the precomputed
  context from the API, keeps turn-path state local, captures transcript turns,
  and writes the final context/transcript back through `/live-result` before
  triggering `/api/score`. It first tries that API write because the API's
  process-local memory store is otherwise invisible to the worker; its direct
  repository write is a fallback that is useful when both processes share
  Supabase. `worker_coach.py` is the analogous optional spoken-coach worker;
  it persists a separate coach transcript and does not attach retrieval tools
  to the live turn loop.
- `post/` is a plain sequential scoring flow, not a LangGraph graph:
  competency evaluation, optional score verification, spoken-language
  assessment, and report/`ScoreCard` assembly are individually guarded and
  persisted by `run_score`. The HTTP coach implementation in `coach/` is also
  sequential: it builds a study plan from weak competencies or retrieves
  optional knowledge before synthesizing chat. The spoken coach worker is only
  the LiveKit transport for that latter experience.
- `core/persistence/repository.py` selects the process-wide in-memory
  `MemoryRepository` unless both Supabase settings are present, in which case
  it uses `SupabaseRepository`. The memory path is suitable for offline/dev
  work but does not survive a process restart; a worker's separate memory
  instance cannot substitute for the API's store.
- `core/tracing.py` writes local JSONL traces under `TRACE_DIR` (default
  `.deepinterview/traces`) for prep, score, and LiveKit worker runs. Hosted
  Langfuse/Sentry integrations are optional extras and best-effort. HTTP
  coach/KB routes do not automatically acquire the same prep/score/live trace
  spans.
- Provider selection belongs in `core/adapters/`: the default is deterministic
  mock adapters; real LLM, search, speech, Supabase, and knowledge providers
  are opt-in through settings and optional dependency extras. `LIGHTRAG_URL`
  selects the HTTP knowledge adapter; without it the agent uses its offline
  knowledge stub.

## Contract and evidence boundary

`packages/shared/src` is the TypeScript contract source of truth and
`shared_models.py` is its Pydantic mirror. Keep generated schemas, parity and
round-trip tests, and persisted fixture compatibility in the same change. The
offline suite (`uv --directory apps/agent run pytest`) exercises mock adapters
and LiveKit-free logic; it does not prove real provider credentials, a LiveKit
room, a hosted deployment, or production persistence. Do not describe those
paths as verified without corresponding runtime evidence.

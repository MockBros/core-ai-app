# services/lightrag — Knowledge sidecar (WP-8)

The DeepInterview **knowledge service** that powers the Prep Coach. It keeps one
RAG store/graph per sidecar partition key and answers grounded questions with
citations. The sidecar calls that key `user_id`; in the OSS auth-free flow it is
normally the interview `session_id` passed through the agent's `store_key`.

Runs as a standalone Docker sidecar on **:9621**. This is a self-contained `uv`
project (NOT a node/turbo workspace package): it does not import
`@deepinterview/shared` — the KB wire models are mirrored locally in
`src/lightrag_service/models.py` (snake_case identical to the shared contracts),
so the agent's `HttpKnowledge` client parses responses straight into the shared
`Citation` model.

## Endpoints

| Method | Path         | Body → Response |
| ------ | ------------ | --------------- |
| `GET`  | `/health`    | → `{ "status": "ok", "backend": "naive" }` (liveness only) |
| `POST` | `/kb/ingest` | `KbIngestRequest{ user_id, files[] }` → `KbIngestResponse{ track_id }` |
| `POST` | `/kb/query`  | `KbQueryRequest{ user_id, query, lang }` → `KbQueryResponse{ answer, citations[] }` |

`Citation = { title, url, snippet? }`. `lang` is one of the 10 supported languages
(EN default, multilingual — bge-m3 is cross-lingual).

The shared agent contract names the partition field `store_key`; the HTTP
adapter serializes it as the sidecar's `user_id` field. Prep ingests under the
session id and the coach queries with that same key. This gives capability-based
scoping, not authenticated tenant isolation: the sidecar trusts the caller's
string and does not resolve it to a signed-in user. Set `LIGHTRAG_API_SECRET`
and configure the same `lightrag_api_secret` on the agent to add a shared-secret
gate, but that is still not per-user authorization.

`/kb/ingest` fetches each `files[]` entry that looks like an `http(s)` URL using
httpx **if it is installed**. Non-URL entries are raw text; a refused URL or a
failed/missing fetch contributes no document body. The service is therefore
runnable fully offline with only `fastapi`/`uvicorn`/`pydantic`.

## Backends

The backend is chosen by the `RAG_BACKEND` env var (default `naive`).

### `naive` (default) — `NaiveRAG`

- Dependency-light, **in-memory, deterministic** store. Zero ML deps, no network.
- Ingest splits each doc into ~500-char chunks with source metadata.
- Query scores chunks by lowercased token-overlap (TF), takes the top-3, and
  composes a short extractive `answer` (lead with the best chunk). Each surfaced
  chunk becomes a `Citation` (`title`/`url` = source id, `snippet` = excerpt).
- This is what runs in CI and the default Docker image.

### `lightrag` — `LightRAGBackend` (scaffold; not implemented)

- The cross-lingual knowledge-graph stack: **LightRAG + RAG-Anything + bge-m3**
  embeddings (and `bge-reranker-v2-m3`). One LightRAG working dir / graph per
  `user_id`; RAG-Anything handles multimodal ingestion (PDF/DOCX/PPTX/images).
- Lazy-imported and **gated**: only constructed when `RAG_BACKEND=lightrag` and
  the optional `rag` extra is installed; otherwise it raises a clear error.
- The current class is a skeleton: `_instance`, `ingest`, and `query` raise
  `NotImplementedError`. Installing the extra or setting `RAG_BACKEND=lightrag`
  is not evidence that a usable LightRAG backend exists.
- The intended implementation would use LightRAG's retrieved chunks/sources —
  the `/query/data` response shape exposes the source documents behind an
  answer, which should map onto the `Citation` list returned by `/kb/query`.

## Future real-backend work

```bash
# Optional dependency set for the future implementation (not a working backend)
uv sync --extra rag
```

bge-m3 (`BAAI/bge-m3`) would be downloaded on first use by
`sentence-transformers`; `LIGHTRAG_WORKING_DIR` is reserved for the intended
per-partition graph storage. A real-backend change must separately prove
dependency installation, document ingestion, query answers, citation mapping,
partition isolation, and persistence; do not infer those results from `/health`
or an image build.

## Fetch and request-safety limits

The ingest SSRF guard is partial defence in depth. It accepts only `http` and
`https`, rejects literal loopback/private/link-local/reserved/multicast/
unspecified addresses and local hostnames, follows no redirects, and applies a
15-second httpx timeout. It does not DNS-resolve and re-check hostnames or
enforce network egress policy. There is also no sidecar-level maximum for the
number/length of `files[]`, request body size, fetched response bytes, or query
body. The agent's `/api/kb` routes add 100-file, 5 MB-total, and 10,000-character
query caps, but direct sidecar callers bypass those limits.

## Development

```bash
uv sync                 # naive deps only (fastapi/uvicorn/pydantic + dev)
uv run pytest           # offline tests, no ML deps, no network
uv run ruff check .
uv run python -m lightrag_service.app   # serve on :9621 (env LIGHTRAG_PORT)
```

## Environment

| Var                   | Default         | Purpose |
| --------------------- | --------------- | ------- |
| `RAG_BACKEND`         | `naive`         | Backend select: functional `naive`; `lightrag` is currently an unimplemented scaffold. |
| `LIGHTRAG_PORT`       | `9621`          | Port `main()` / the Docker `CMD` binds. |
| `LIGHTRAG_WORKING_DIR`| `./rag_storage` | (lightrag) where per-user graphs persist. |

> The **agent** calls this service via `LIGHTRAG_URL` (e.g. `http://lightrag:9621`)
> — that variable lives on the agent side, not here. The agent maps its
> `store_key` to this service's `user_id` field.

## Docker

```bash
docker build -t deepinterview-lightrag services/lightrag
docker run -p 9621:9621 deepinterview-lightrag   # NaiveRAG backend
```

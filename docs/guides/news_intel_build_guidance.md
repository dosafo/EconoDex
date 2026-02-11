# News Intelligence Platform — Build Guidance

This doc describes **how to build** each part of the first slice. The codebase keeps implementations minimal (stubs / in-memory where possible); use this guide to add the full implementation step by step. Implement incrementally—one agent or one endpoint at a time.

---

## 1. Data model & migrations

**Where:** `data_storage/models/news_intel_models.py`, `data_storage/migrations/001_news_intel_tables.py`

**Pattern:**

- One table per entity: `Article`, `StoryCluster`, `ClusterMember`, `AnalysisRun`. Use the same names as in `docs/news_intel_overview.md`.
- Use SQLAlchemy `Column(JSON)` for flexible fields (`metadata`, `output_json`). Keep a single source of truth for column names (e.g. `metadata_` in Python, `"metadata"` in DB via `Column("metadata", JSON)`).
- Migration: import `Base` and all model modules so `Base.metadata` has every table, then `Base.metadata.create_all(bind=engine)`. Run from project root: `PYTHONPATH=. python -m data_storage.migrations.001_news_intel_tables`.

**Schema rules:**

- `articles`: `id` (PK), `url`, `publisher`, `published_at`, `text`, `metadata` (JSON).
- `story_clusters`: `id`, `canonical_title`, `created_at`.
- `cluster_members`: `cluster_id`, `article_id`, `similarity_score` (composite PK).
- `analysis_runs`: `id`, `article_id`, `cluster_id`, `agent_name`, `schema_version`, `status`, `output_json`, `created_at`.

Leave `claims` and `evidence_links` for a later migration when you add Claim/Evidence agents.

---

## 2. Article ingest (POST /ingest/article)

**Where:** `backend/services/article_service.py` (`ingest_article`), `backend/api/news_intel.py` (route)

**How to build:**

1. **Request body:** Accept `url`, `raw_text`, `publisher`, `published_at`, `metadata` (optional). Validate at least one of `url` or `raw_text`.
2. **ID:** Generate `article_id = str(uuid.uuid4())`.
3. **Parse `published_at`:** If present as string, use `datetime.fromisoformat(published_at.replace("Z", "+00:00"))`; on failure keep `published_at` as `None`.
4. **Storage:** Create `Article(id=article_id, url=..., text=raw_text, publisher=..., published_at=..., metadata_=metadata or {})`, `session.add(article)`, `session.commit()`, return `article_id`.
5. **Session:** Use a shared session factory (e.g. `get_session_factory(engine)` from `data_storage.models.base`). Lazy-init engine from `DATABASE_URL` or default SQLite.
6. **Endpoint:** `POST /ingest/article` → call `ingest_article(**body)`, return `{"article_id": "..."}`.

---

## 3. Orchestrator skeleton

**Where:** `backend/news_intel_orchestrator/orchestrator.py`

**How to build:**

1. **Signature:** `analyze_article(article_id: str, get_article_fn, save_analysis_fn) -> None`.
2. **Dependencies:** Do not import storage or API; receive `get_article_fn(article_id)` and `save_analysis_fn(run_id, article_id, cluster_id, agent_name, schema_version, output_json, status="completed")` so the orchestrator stays testable and storage-agnostic.
3. **Flow:**  
   - Load article via `get_article_fn(article_id)`; if missing, return.  
   - Read `text` and `metadata` from the article object.  
   - Call ClusterAgent (stub or implementation): `artifact = cluster_agent_stub(article_id, text, metadata)`.  
   - Generate `run_id = str(uuid.uuid4())`.  
   - Call `save_analysis_fn(run_id=..., article_id=..., cluster_id=artifact.data["cluster_id"], agent_name="ClusterAgent", schema_version=artifact.schema_version, output_json=artifact.to_dict())`.
4. **Later agents:** Add steps in the same order as in `docs/news_intel_overview.md` (Extraction, Claim, Evidence, Sentiment, Bias, Timeline, Historical). Each step: call agent → `save_analysis_fn(...)` with that agent’s name and artifact. Support re-runs by always inserting new `analysis_runs` rows (versioned by `schema_version`).

---

## 4. ClusterAgent interface and stub

**Where:** `backend/news_intel_orchestrator/agents/cluster_agent.py`, `agents/base.py`

**How to build:**

1. **Shared primitive:** In `base.py` define `AnalysisArtifact(schema_version, data)` with `to_dict()` returning `{"schema_version": ..., **data}`.
2. **Contract:** Define a `Protocol`: `ClusterAgentContract` with `run(article_id, text, metadata) -> AnalysisArtifact`.
3. **Stub:** `cluster_agent_stub(article_id, text, metadata)` returns an artifact with:
   - `schema_version="1"`,
   - `data={"cluster_id": "<string>", "similar_articles": []}`.  
   For a minimal cluster_id, use e.g. `str(hash(topic) & 0x7FFFFFFF)` where `topic = metadata.get("headline") or text[:200] or article_id`.
4. **Upgrade path:** Replace the stub with a real implementation (e.g. embedding + similarity search) that still returns the same artifact shape; optionally persist `StoryCluster` and `ClusterMember` and return real `cluster_id` and `similar_articles` list.

---

## 5. GET /article/{id}/intel

**Where:** `backend/services/article_service.py` (`get_article_intel`), `backend/api/news_intel.py` (route)

**How to build:**

1. **Query:** From `analysis_runs` select rows where `article_id == article_id`, order by `created_at` descending.
2. **Shape:** Build a dict keyed by `agent_name`; for each agent keep only the latest run (first occurrence when iterating). Each value: `{"schema_version", "status", "output": output_json, "created_at"}`. Return `{"artifacts": by_agent}`.
3. **Endpoint:** `GET /article/{article_id}/intel` → call `get_article_intel(article_id)`, return the dict (or a Pydantic model with `artifacts: dict`). Do not overfit the response shape; consumers can branch on `agent_name` and `schema_version`.

---

## 6. EconomicDataAdapter

**Where:** `backend/adapters/economic_data_adapter.py`

**How to build (adapter only; do not change core hub):**

1. **search_series(entities, keywords):**  
   - Input: optional lists `entities`, `keywords`.  
   - Output: list of candidates, e.g. `[{ "series_id", "title", "source" }]`.  
   - Implementation: call existing data hub (e.g. BLS catalog or `data_collectors`) to resolve entities/keywords to series IDs; return list. Stub: return `[]`.
2. **build_query(series_id, params):**  
   - Input: `series_id`, optional `params` (e.g. `startyear`, `endyear`).  
   - Output: dict suitable for the hub (e.g. `{"series_id", "startyear", "endyear"}` for BLS).  
   - Implementation: build the payload your hub expects; no direct DB or API changes in the hub, only calls from this adapter. EvidenceAgent will use this to produce chart-ready query objects.

---

## 7. POST /analyze/article/{id}

**Where:** `backend/api/news_intel.py`

**How to build:**

1. Look up article by id (e.g. `article_service.get_article(article_id)`). If not found, return 404.
2. Call `analyze_article(article_id, get_article_fn=..., save_analysis_fn=...)` with the same functions the article service uses for get/save.
3. Return e.g. `{"status": "ok", "article_id": "..."}`. For async-friendly behavior later, you can enqueue a task and return 202 with a job id; for MVP, sync is fine.

---

## 8. Tests

**Contract test (e.g. ClusterAgent):** Call `cluster_agent_stub(article_id, text, metadata)` and assert: `artifact.to_dict()` has `schema_version == "1"`, `cluster_id` is a string, `similar_articles` is a list (empty for stub).

**Schema/snapshot test (optional):** After migration, assert that the tables exist and expected columns are present (e.g. via raw SQL or SQLAlchemy `inspector.get_columns(table)`).

---

## 9. Documentation

**Where:** `docs/news_intel_overview.md`

Keep it as the single place for: entity definitions, agent contracts (inputs/outputs), pipeline order, and artifact schema versioning rules. When you add an agent, add one line to the pipeline order and one row to the agent table; document the new artifact shape and schema version.

---

## 10. Changelog

After each iteration, add a short entry to `CHANGELOG.md`: what was added (e.g. “ClusterAgent stub + analysis_runs persistence”), and the next step (e.g. “Add BiasFramingAgent contract + stub”).

---

## Order of implementation (first slice)

1. Models + migration (tables exist).  
2. `ingest_article` + POST /ingest/article.  
3. `AnalysisArtifact` + ClusterAgent contract + stub.  
4. `save_analysis_run` + `analyze_article` (orchestrator) that runs ClusterAgent and saves.  
5. `get_article_intel` + GET /article/{id}/intel.  
6. POST /analyze/article/{id} that calls `analyze_article`.  
7. EconomicDataAdapter (stub).  
8. One contract test + `docs/news_intel_overview.md` + CHANGELOG entry.

After that, add one agent at a time: contract → stub → orchestrator step → test.

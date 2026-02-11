# Changelog

## [Unreleased]

### Added — News Intelligence Platform (first slice, scaffold + guidance)

- **Entities & storage**: Models and migration for `articles`, `story_clusters`, `cluster_members`, `analysis_runs` (schema-first; migration runnable with `PYTHONPATH=. python -m data_storage.migrations.001_news_intel_tables`).
- **POST /ingest/article**, **GET /article/{id}/intel**, **POST /analyze/article/{id}**: Implemented as thin endpoints; article storage is **in-memory stub** by default. Full DB implementation described in `docs/guides/news_intel_build_guidance.md`.
- **Orchestrator skeleton**: `analyze_article(article_id, get_article_fn, save_analysis_fn)` runs ClusterAgent stub and persists via provided `save_analysis_fn`; TODO scaffolds for other agents.
- **ClusterAgent**: Interface (`ClusterAgentContract`) + stub (hash-based cluster_id, empty similar_articles).
- **EconomicDataAdapter**: Stub only — `search_series` returns `[]`, `build_query` returns minimal dict; wiring to hub described in build guidance.
- **Documentation**: `docs/news_intel_overview.md` (entities, contracts, pipeline, versioning); **`docs/guides/news_intel_build_guidance.md`** (step-by-step how to build each piece).
- **Test**: Contract test for ClusterAgent stub.

### Next steps

- Replace in-memory article/intel storage with SQLAlchemy using the patterns in the build guidance.
- Add one agent at a time (e.g. BiasFramingAgent): contract → stub → orchestrator step → test.
- Add GET /cluster/{id}; wire EvidenceAgent to EconomicDataAdapter.

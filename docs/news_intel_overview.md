# News Intelligence Platform — Overview

**How to build each part:** see [news_intel_build_guidance.md](guides/news_intel_build_guidance.md).

## Goal

Transform the economic data hub into a **News Intelligence Platform** that ingests news articles and builds an intelligence surface per headline/story cluster: related coverage, bias/framing, sentiment, datasets/charts for cross-checking, story evolution timeline, and historical analogs.

## Entity Definitions

| Entity | Description |
|--------|-------------|
| **Article** | Ingested item: url, publisher, published_at, text, metadata (JSON). |
| **Source** | Publisher/source of articles (future). |
| **StoryCluster** | Group of articles covering the same story; canonical_title, created_at. |
| **ClusterMember** | Link article ↔ cluster with similarity_score. |
| **Claim** | Atomic statement candidate (e.g. numeric/causal); links to article. |
| **EvidenceLink** | Pointer to dataset/series + query params + provenance; links claim to economic hub. |
| **AnalysisRun** | One agent run: article_id or cluster_id, agent_name, schema_version, status, output_json. |

## Agent Contracts

Agents are defined as interfaces; each produces an **AnalysisArtifact** (JSON blob) with a **schema_version**.

| Agent | Input | Output (artifact) |
|-------|--------|-------------------|
| **ClusterAgent** | article | story_cluster_id, similar_articles[] |
| **BiasFramingAgent** | article + cluster | framing/bias signals |
| **SentimentAgent** | article | sentiment/emotion markers |
| **EvidenceAgent** | article/claims | dataset references + chart-ready queries (uses EconomicDataAdapter) |
| **TimelineAgent** | cluster | chronological story evolution + corrections/updates |
| **HistoricalAnalogyAgent** | cluster/topic | candidate historical analogs + confidence |

Shared primitives:

- **Extraction**: raw text → structured fields (headline, author, date, entities, keywords).
- **Claim**: atomic statement candidates (esp. numeric/causal).
- **EvidenceLink**: pointer to dataset series + query params + provenance.
- **AnalysisArtifact**: JSON blob with schema versioning per agent.

## Pipeline Order (MVP)

For a single ingested article:

1. Normalize + store article text/metadata.
2. Run **ClusterAgent** → assign cluster + similar articles.
3. Run **Extraction** + **ClaimExtraction** (lightweight heuristics).
4. Run **EvidenceAgent** (EconomicDataAdapter: map claims/entities → series, produce chart query objects).
5. Run **SentimentAgent** and **BiasFramingAgent**.
6. Persist every agent output as **analysis_runs** records.

Orchestrator supports **re-runs** and **schema upgrades** (versioned output_json).

## Artifact Schema Versioning

- Each agent records `schema_version` (e.g. `"1"`) in **analysis_runs**.
- `output_json` structure may change over time; consumers should check `schema_version` and handle backwards compatibility.
- New versions: add new runs with updated schema_version; do not overwrite old runs.

## API (thin endpoints)

- `POST /api/v1/news-intel/ingest/article` — url or raw text → article_id
- `POST /api/v1/news-intel/analyze/article/{id}` — kick orchestrator pipeline (async-friendly later)
- `GET /api/v1/news-intel/article/{id}/intel` — latest artifacts by agent name
- `GET /api/v1/news-intel/cluster/{id}` — members + timeline + aggregated intel (future)

Responses return artifacts by agent name; response formats stay flexible.

## Integration with Economic Hub

- **EconomicDataAdapter** is the only integration point: `search_series(entities, keywords)`, `build_query(series_id, params)`.
- Core economic hub (data_collectors, BLS, etc.) is unchanged; all access via adapter.

"""
Article ingest and intel retrieval.
Implementation guidance: docs/guides/news_intel_build_guidance.md (§2, §5).
Replace in-memory stubs below with SQLAlchemy + data_storage.models when ready.
"""
import uuid
from typing import Any, Optional

# In-memory stubs so the API runs without DB. Replace with real storage per guidance.
_articles: dict[str, dict] = {}
_analysis_runs: list[dict] = []


def ingest_article(
    *,
    url: Optional[str] = None,
    raw_text: Optional[str] = None,
    publisher: Optional[str] = None,
    published_at: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> str:
    """Store article; return article_id. See guidance for DB implementation."""
    article_id = str(uuid.uuid4())
    _articles[article_id] = {
        "id": article_id,
        "url": url,
        "text": raw_text,
        "publisher": publisher,
        "published_at": published_at,
        "metadata": metadata or {},
    }
    return article_id


def get_article(article_id: str):
    """Return article object with .text, .metadata_ for orchestrator. See guidance."""
    data = _articles.get(article_id)
    if not data:
        return None
    # Minimal object so orchestrator can get_article_fn(article_id) and read .text, .metadata_
    class _Article:
        pass
    o = _Article()
    o.id = data["id"]
    o.text = data.get("text") or ""
    o.metadata_ = data.get("metadata") or {}
    return o


def get_article_intel(article_id: str) -> dict[str, Any]:
    """Return latest artifacts keyed by agent name. See guidance for DB implementation."""
    by_agent: dict[str, Any] = {}
    for r in reversed(_analysis_runs):
        if r.get("article_id") != article_id:
            continue
        name = r.get("agent_name")
        if name and name not in by_agent:
            by_agent[name] = {
                "schema_version": r.get("schema_version"),
                "status": r.get("status", "completed"),
                "output": r.get("output_json"),
                "created_at": r.get("created_at"),
            }
    return {"artifacts": by_agent}


def save_analysis_run(
    run_id: str,
    article_id: str,
    cluster_id: Optional[str],
    agent_name: str,
    schema_version: str,
    output_json: dict,
    status: str = "completed",
) -> None:
    """Persist one agent run. See guidance for DB implementation."""
    from datetime import datetime
    _analysis_runs.append({
        "id": run_id,
        "article_id": article_id,
        "cluster_id": cluster_id,
        "agent_name": agent_name,
        "schema_version": schema_version,
        "status": status,
        "output_json": output_json,
        "created_at": datetime.utcnow().isoformat(),
    })

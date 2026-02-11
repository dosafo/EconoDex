"""
Orchestrator: runs pipeline per article; stores each agent output in analysis_runs.
Build guidance: docs/guides/news_intel_build_guidance.md (§3).
"""
import uuid

from .agents.cluster_agent import cluster_agent_stub

# TODO: Extraction + ClaimExtraction
# TODO: EvidenceAgent (EconomicDataAdapter)
# TODO: SentimentAgent, BiasFramingAgent
# TODO: TimelineAgent, HistoricalAnalogyAgent


def analyze_article(article_id: str, get_article_fn, save_analysis_fn) -> None:
    """
    Run agent pipeline for one article and persist artifacts.
    get_article_fn(article_id) -> object with .text, .metadata_; save_analysis_fn(run_id, article_id, cluster_id, agent_name, schema_version, output_json, status=...).
    """
    article = get_article_fn(article_id)
    if not article:
        return
    text = getattr(article, "text", None) or ""
    metadata = getattr(article, "metadata_", None) or {}

    artifact = cluster_agent_stub(article_id, text, metadata)
    run_id = str(uuid.uuid4())
    save_analysis_fn(
        run_id=run_id,
        article_id=article_id,
        cluster_id=artifact.data.get("cluster_id"),
        agent_name="ClusterAgent",
        schema_version=artifact.schema_version,
        output_json=artifact.to_dict(),
        status="completed",
    )

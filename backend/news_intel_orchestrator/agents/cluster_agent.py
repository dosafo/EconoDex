"""
ClusterAgent: article → story_cluster_id + similar articles.
Build guidance: docs/guides/news_intel_build_guidance.md (§4).
"""
from typing import Protocol

from .base import AnalysisArtifact


class ClusterAgentContract(Protocol):
    """Contract: given article content, return cluster assignment and similar articles."""

    def run(self, article_id: str, text: str, metadata: dict) -> AnalysisArtifact:
        ...


def cluster_agent_stub(article_id: str, text: str, metadata: dict) -> AnalysisArtifact:
    """Placeholder: cluster_id from topic hash; similar_articles empty. Replace per guidance."""
    topic = (metadata or {}).get("headline") or (text[:200] if text else article_id)
    cluster_id = str(hash(topic) & 0x7FFFFFFF)
    return AnalysisArtifact(
        schema_version="1",
        data={"cluster_id": cluster_id, "similar_articles": []},
    )

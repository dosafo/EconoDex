"""Contract test: ClusterAgent stub returns expected artifact shape and schema_version."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.news_intel_orchestrator.agents.cluster_agent import cluster_agent_stub


def test_cluster_agent_stub_returns_artifact_with_schema_version_and_cluster():
    artifact = cluster_agent_stub(
        article_id="test-id",
        text="Some headline about inflation.",
        metadata={"headline": "Fed raises rates again"},
    )
    out = artifact.to_dict()
    assert out["schema_version"] == "1"
    assert "cluster_id" in out
    assert isinstance(out["cluster_id"], str)
    assert out["similar_articles"] == []
    assert isinstance(out["similar_articles"], list)

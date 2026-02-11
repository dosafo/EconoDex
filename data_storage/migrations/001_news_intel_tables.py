"""
Migration 001: Create news_intel tables (articles, story_clusters, cluster_members, analysis_runs).
Run: PYTHONPATH=. python -m data_storage.migrations.001_news_intel_tables
Build guidance: docs/guides/news_intel_build_guidance.md (§1).
"""
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from data_storage.models import (
    Base,
    get_engine,
    Article,
    StoryCluster,
    ClusterMember,
    AnalysisRun,
)


def run():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("Created tables: articles, story_clusters, cluster_members, analysis_runs.")


if __name__ == "__main__":
    run()

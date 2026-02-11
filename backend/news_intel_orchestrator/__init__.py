"""
News Intelligence Orchestrator: runs agent pipeline per article/story cluster,
stores outputs in analysis_runs. Supports re-runs and schema upgrades.
"""
from .orchestrator import analyze_article

__all__ = ["analyze_article"]

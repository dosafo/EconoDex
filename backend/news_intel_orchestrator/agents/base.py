"""Agent contracts and shared primitives. All agents produce AnalysisArtifact.
Build guidance: docs/guides/news_intel_build_guidance.md (§4).
"""
from typing import Any, Protocol


class AnalysisArtifact:
    """JSON-serializable output per agent; schema versioned by agent_name + schema_version."""

    def __init__(self, schema_version: str, data: dict[str, Any]):
        self.schema_version = schema_version
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        return {"schema_version": self.schema_version, **self.data}

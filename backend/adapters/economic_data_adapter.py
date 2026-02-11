"""
EconomicDataAdapter: integrate with economic hub (BLS, etc.) only through this adapter.
Build guidance: docs/guides/news_intel_build_guidance.md (§6).
Do not modify core hub; EvidenceAgent will use search_series + build_query.
"""
from typing import Any


class EconomicDataAdapter:
    """Adapter: search_series, build_query. Implement per guidance; stub returns empty/defaults."""

    def search_series(
        self,
        entities: list[str] | None = None,
        keywords: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Return series candidates. Stub: []. Wire to hub catalog per guidance."""
        return []

    def build_query(
        self,
        series_id: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build query_json for chart/hub fetch. Stub: series_id + default years. Per guidance."""
        p = params or {}
        return {
            "series_id": series_id,
            "startyear": p.get("startyear", "2020"),
            "endyear": p.get("endyear", "2024"),
        }

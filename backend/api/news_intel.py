"""News Intel API: ingest, analyze, intel. Build guidance: docs/guides/news_intel_build_guidance.md (§2, §5, §7)."""
from fastapi import APIRouter, HTTPException

from backend.schemas.news_intel_schemas import (
    IngestArticleRequest,
    IngestArticleResponse,
    IntelResponse,
)
from backend.services import article_service
from backend.news_intel_orchestrator import analyze_article

router = APIRouter(prefix="/news-intel", tags=["news-intel"])


@router.post("/ingest/article", response_model=IngestArticleResponse)
def ingest_article_endpoint(body: IngestArticleRequest):
    """Store article (url or raw text); return article_id."""
    if not body.url and not body.raw_text:
        raise HTTPException(400, "Provide url or raw_text")
    article_id = article_service.ingest_article(
        url=body.url,
        raw_text=body.raw_text,
        publisher=body.publisher,
        published_at=body.published_at,
        metadata=body.metadata,
    )
    return IngestArticleResponse(article_id=article_id)


@router.post("/analyze/article/{article_id}")
def analyze_article_endpoint(article_id: str):
    """Kick orchestrator pipeline for this article (sync for MVP)."""
    article = article_service.get_article(article_id)
    if not article:
        raise HTTPException(404, "Article not found")
    analyze_article(
        article_id,
        get_article_fn=article_service.get_article,
        save_analysis_fn=article_service.save_analysis_run,
    )
    return {"status": "ok", "article_id": article_id}


@router.get("/article/{article_id}/intel", response_model=IntelResponse)
def get_article_intel_endpoint(article_id: str):
    """Return latest stored artifacts by agent name."""
    data = article_service.get_article_intel(article_id)
    return IntelResponse(artifacts=data.get("artifacts", {}))
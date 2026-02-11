"""Request/response schemas for news intel endpoints."""
from typing import Any, Optional

from pydantic import BaseModel


class IngestArticleRequest(BaseModel):
    url: Optional[str] = None
    raw_text: Optional[str] = None
    publisher: Optional[str] = None
    published_at: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class IngestArticleResponse(BaseModel):
    article_id: str


class IntelResponse(BaseModel):
    artifacts: dict[str, Any] = {}

"""FastAPI app entry point. Run: PYTHONPATH=. uvicorn backend.main:app --reload"""
from fastapi import FastAPI

from backend.api.news_intel import router as news_intel_router
from backend.api.local_tax_intel import router as local_tax_intel_router

app = FastAPI(title="EconoDex", version="0.1.0")
app.include_router(news_intel_router, prefix="/api/v1")
app.include_router(local_tax_intel_router, prefix="/api/v1")

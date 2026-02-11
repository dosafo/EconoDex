"""News Intelligence entities. Schema-first; flexible fields in JSON.
Build guidance: docs/guides/news_intel_build_guidance.md (§1).
Schema reference: docs/news_intel_overview.md.
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text, JSON
from .base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String(64), primary_key=True)
    url = Column(String(2048), nullable=True, index=True)
    publisher = Column(String(256), nullable=True)
    published_at = Column(DateTime, nullable=True)
    text = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True, default=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "publisher": self.publisher,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "text": self.text,
            "metadata": self.metadata_ or {},
        }


class StoryCluster(Base):
    __tablename__ = "story_clusters"

    id = Column(String(64), primary_key=True)
    canonical_title = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "canonical_title": self.canonical_title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class ClusterMember(Base):
    __tablename__ = "cluster_members"

    cluster_id = Column(String(64), ForeignKey("story_clusters.id"), primary_key=True)
    article_id = Column(String(64), ForeignKey("articles.id"), primary_key=True)
    similarity_score = Column(Float, nullable=True)


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(String(64), primary_key=True)
    article_id = Column(String(64), ForeignKey("articles.id"), nullable=True, index=True)
    cluster_id = Column(String(64), ForeignKey("story_clusters.id"), nullable=True, index=True)
    agent_name = Column(String(64), nullable=False, index=True)
    schema_version = Column(String(32), nullable=False, default="1")
    status = Column(String(32), nullable=False, default="completed")
    output_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "cluster_id": self.cluster_id,
            "agent_name": self.agent_name,
            "schema_version": self.schema_version,
            "status": self.status,
            "output_json": self.output_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

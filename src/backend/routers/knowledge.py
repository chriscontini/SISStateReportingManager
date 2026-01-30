"""
Knowledge base API router.

Provides endpoints for managing knowledge articles including
search, filtering by state, and CRUD operations.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.knowledge_service import KnowledgeService


router = APIRouter(prefix="/knowledge", tags=["knowledge"])


# Pydantic schemas
class ArticleCreate(BaseModel):
    """Schema for creating a knowledge article."""
    state_id: int
    title: str
    content: str
    category: str
    source_url: Optional[str] = None
    tags: Optional[List[str]] = None


class ArticleUpdate(BaseModel):
    """Schema for updating a knowledge article."""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    source_url: Optional[str] = None
    tags: Optional[List[str]] = None


class StateInfo(BaseModel):
    """Nested state info for article response."""
    id: int
    name: str
    abbreviation: str

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    """Schema for knowledge article response."""
    id: int
    state_id: int
    title: str
    content: str
    category: str
    source_url: Optional[str]
    tags: List[str]
    state: Optional[StateInfo] = None

    class Config:
        from_attributes = True


class ArticleListItem(BaseModel):
    """Schema for article list items (abbreviated)."""
    id: int
    state_id: int
    title: str
    category: str
    tags: List[str]
    state: Optional[StateInfo] = None

    class Config:
        from_attributes = True


@router.post("/articles", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new knowledge article."""
    service = KnowledgeService(db)
    created = await service.create_article(
        state_id=article.state_id,
        title=article.title,
        content=article.content,
        category=article.category,
        source_url=article.source_url,
        tags=article.tags,
    )
    return created


@router.get("/articles", response_model=List[ArticleListItem])
async def list_articles(
    state_id: Optional[int] = Query(None, description="Filter by state ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List all knowledge articles with optional filtering."""
    service = KnowledgeService(db)

    if state_id:
        articles = await service.get_articles_by_state(state_id, category)
    else:
        articles = await service.get_all_articles(category, limit, offset)

    return articles


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a single knowledge article by ID."""
    service = KnowledgeService(db)
    article = await service.get_article(article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article


@router.put("/articles/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a knowledge article."""
    service = KnowledgeService(db)
    updated = await service.update_article(
        article_id,
        **article.model_dump(exclude_none=True),
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Article not found")

    return updated


@router.delete("/articles/{article_id}")
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete a knowledge article."""
    service = KnowledgeService(db)
    deleted = await service.delete_article(article_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")

    return {"status": "deleted", "id": article_id}


@router.get("/search", response_model=List[ArticleListItem])
async def search_articles(
    q: str = Query(..., min_length=2, description="Search query"),
    state_id: Optional[int] = Query(None, description="Filter by state ID"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Search knowledge articles by title, content, or tags."""
    service = KnowledgeService(db)
    articles = await service.search_articles(
        query=q,
        state_id=state_id,
        category=category,
        limit=limit,
    )
    return articles


@router.get("/categories", response_model=List[str])
async def list_categories(
    db: AsyncSession = Depends(get_db),
):
    """Get all unique article categories."""
    service = KnowledgeService(db)
    return await service.get_categories()


@router.get("/articles/{article_id}/related", response_model=List[ArticleListItem])
async def get_related_articles(
    article_id: int,
    limit: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """Get articles related to the given article."""
    service = KnowledgeService(db)
    related = await service.get_related_articles(article_id, limit)
    return related


@router.get("/stats")
async def get_knowledge_stats(
    db: AsyncSession = Depends(get_db),
):
    """Get knowledge base statistics."""
    service = KnowledgeService(db)

    all_articles = await service.get_all_articles(limit=1000)
    categories = await service.get_categories()
    by_state = await service.get_article_count_by_state()

    return {
        "total_articles": len(all_articles),
        "categories": categories,
        "articles_by_state": by_state,
    }

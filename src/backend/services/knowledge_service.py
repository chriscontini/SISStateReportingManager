"""
Knowledge base service for managing state documentation and insights.

This service provides methods to create, retrieve, search, and manage
knowledge articles related to state reporting requirements.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import KnowledgeArticle, State


class KnowledgeService:
    """Service for managing knowledge base articles."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_article(
        self,
        state_id: int,
        title: str,
        content: str,
        category: str,
        source_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> KnowledgeArticle:
        """Create a new knowledge article.

        Args:
            state_id: ID of the state this article relates to
            title: Article title
            content: Full article content (markdown supported)
            category: Category (e.g., 'reporting', 'certification', 'integration')
            source_url: Optional URL source for the information
            tags: Optional list of tags for filtering

        Returns:
            The created KnowledgeArticle
        """
        article = KnowledgeArticle(
            state_id=state_id,
            title=title,
            content=content,
            category=category,
            source_url=source_url,
            tags=tags or [],
        )

        self.session.add(article)
        await self.session.commit()
        await self.session.refresh(article)

        return article

    async def get_article(self, article_id: int) -> Optional[KnowledgeArticle]:
        """Get a single article by ID.

        Args:
            article_id: The article ID

        Returns:
            The article or None if not found
        """
        result = await self.session.execute(
            select(KnowledgeArticle)
            .options(selectinload(KnowledgeArticle.state))
            .where(KnowledgeArticle.id == article_id)
        )
        return result.scalar_one_or_none()

    async def get_articles_by_state(
        self,
        state_id: int,
        category: Optional[str] = None,
    ) -> List[KnowledgeArticle]:
        """Get all articles for a specific state.

        Args:
            state_id: The state ID
            category: Optional category filter

        Returns:
            List of articles for the state
        """
        query = select(KnowledgeArticle).where(
            KnowledgeArticle.state_id == state_id
        )

        if category:
            query = query.where(KnowledgeArticle.category == category)

        query = query.order_by(KnowledgeArticle.created_at.desc())

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def search_articles(
        self,
        query: str,
        state_id: Optional[int] = None,
        category: Optional[str] = None,
        limit: int = 20,
    ) -> List[KnowledgeArticle]:
        """Search articles by title, content, or tags.

        Args:
            query: Search query string
            state_id: Optional state filter
            category: Optional category filter
            limit: Maximum number of results

        Returns:
            List of matching articles
        """
        search_pattern = f"%{query}%"

        stmt = select(KnowledgeArticle).options(
            selectinload(KnowledgeArticle.state)
        )

        # Search in title, content, and tags
        stmt = stmt.where(
            or_(
                KnowledgeArticle.title.ilike(search_pattern),
                KnowledgeArticle.content.ilike(search_pattern),
                func.array_to_string(KnowledgeArticle.tags, ' ').ilike(search_pattern),
            )
        )

        if state_id:
            stmt = stmt.where(KnowledgeArticle.state_id == state_id)

        if category:
            stmt = stmt.where(KnowledgeArticle.category == category)

        stmt = stmt.order_by(KnowledgeArticle.created_at.desc()).limit(limit)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_articles(
        self,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[KnowledgeArticle]:
        """Get all articles with optional filtering.

        Args:
            category: Optional category filter
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of articles
        """
        stmt = select(KnowledgeArticle).options(
            selectinload(KnowledgeArticle.state)
        )

        if category:
            stmt = stmt.where(KnowledgeArticle.category == category)

        stmt = stmt.order_by(KnowledgeArticle.created_at.desc())
        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_categories(self) -> List[str]:
        """Get all unique article categories.

        Returns:
            List of category names
        """
        result = await self.session.execute(
            select(KnowledgeArticle.category)
            .distinct()
            .order_by(KnowledgeArticle.category)
        )
        return [row[0] for row in result.all() if row[0]]

    async def get_related_articles(
        self,
        article_id: int,
        limit: int = 5,
    ) -> List[KnowledgeArticle]:
        """Get articles related to the given article.

        Related articles share the same state or category.

        Args:
            article_id: The source article ID
            limit: Maximum number of related articles

        Returns:
            List of related articles
        """
        # Get the source article
        source = await self.get_article(article_id)
        if not source:
            return []

        # Find articles with same state or category
        stmt = select(KnowledgeArticle).options(
            selectinload(KnowledgeArticle.state)
        ).where(
            KnowledgeArticle.id != article_id,
            or_(
                KnowledgeArticle.state_id == source.state_id,
                KnowledgeArticle.category == source.category,
            )
        ).order_by(
            # Prioritize same state
            KnowledgeArticle.state_id == source.state_id,
            KnowledgeArticle.created_at.desc(),
        ).limit(limit)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_article(
        self,
        article_id: int,
        **kwargs,
    ) -> Optional[KnowledgeArticle]:
        """Update an existing article.

        Args:
            article_id: The article ID
            **kwargs: Fields to update

        Returns:
            The updated article or None if not found
        """
        article = await self.get_article(article_id)
        if not article:
            return None

        allowed_fields = {'title', 'content', 'category', 'source_url', 'tags'}
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(article, field, value)

        article.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(article)

        return article

    async def delete_article(self, article_id: int) -> bool:
        """Delete an article.

        Args:
            article_id: The article ID

        Returns:
            True if deleted, False if not found
        """
        article = await self.get_article(article_id)
        if not article:
            return False

        await self.session.delete(article)
        await self.session.commit()
        return True

    async def get_article_count_by_state(self) -> dict:
        """Get article counts grouped by state.

        Returns:
            Dictionary mapping state_id to article count
        """
        result = await self.session.execute(
            select(
                KnowledgeArticle.state_id,
                func.count(KnowledgeArticle.id).label('count')
            ).group_by(KnowledgeArticle.state_id)
        )
        return {row.state_id: row.count for row in result.all()}

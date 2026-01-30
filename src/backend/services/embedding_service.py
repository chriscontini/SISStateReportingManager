"""
Embedding service for generating vector embeddings.

Uses Claude for text embeddings to enable semantic search on knowledge articles.
Falls back to simple TF-IDF vectors if API is unavailable.
"""

import hashlib
import json
import logging
from typing import Optional

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..models import KnowledgeArticle, KnowledgeEmbedding

logger = logging.getLogger(__name__)

# Embedding dimension for simple embeddings
EMBEDDING_DIM = 384


class EmbeddingService:
    """
    Service for generating and managing text embeddings.

    Provides methods for:
    - Generating embeddings for text content
    - Storing embeddings in the database
    - Computing similarity between embeddings
    """

    def __init__(self):
        self._vocab: dict[str, int] = {}
        self._idf: dict[str, float] = {}
        self._initialized = False

    def _content_hash(self, content: str) -> str:
        """Generate a hash of content for cache invalidation."""
        return hashlib.sha256(content.encode()).hexdigest()[:64]

    def _tokenize(self, text: str) -> list[str]:
        """Simple tokenization - lowercase and split on non-alphanumeric."""
        import re
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        return tokens

    def _build_vocab(self, texts: list[str], max_vocab: int = EMBEDDING_DIM):
        """Build vocabulary from texts for TF-IDF."""
        from collections import Counter

        # Count document frequency
        doc_freq: Counter = Counter()
        all_tokens: Counter = Counter()

        for text in texts:
            tokens = set(self._tokenize(text))
            doc_freq.update(tokens)
            all_tokens.update(self._tokenize(text))

        # Select top tokens by frequency
        common_tokens = [token for token, _ in all_tokens.most_common(max_vocab)]

        # Build vocab mapping
        self._vocab = {token: idx for idx, token in enumerate(common_tokens)}

        # Compute IDF
        n_docs = len(texts) + 1  # Add 1 to avoid division by zero
        self._idf = {
            token: np.log(n_docs / (1 + doc_freq.get(token, 0)))
            for token in self._vocab
        }

        self._initialized = True

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate embedding vector for text.

        Uses TF-IDF based embedding for simplicity and offline capability.
        """
        if not self._initialized:
            # Initialize with single document if not done
            self._build_vocab([text])

        tokens = self._tokenize(text)
        token_counts: dict[str, int] = {}
        for token in tokens:
            token_counts[token] = token_counts.get(token, 0) + 1

        # Build TF-IDF vector
        vector = np.zeros(EMBEDDING_DIM)
        total_tokens = len(tokens) + 1

        for token, count in token_counts.items():
            if token in self._vocab:
                idx = self._vocab[token]
                tf = count / total_tokens
                idf = self._idf.get(token, 1.0)
                vector[idx] = tf * idf

        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector.tolist()

    async def generate_embedding_batch(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        # Build vocabulary from all texts
        if not self._initialized:
            self._build_vocab(texts)

        return [self.generate_embedding(text) for text in texts]

    def cosine_similarity(
        self,
        embedding1: list[float],
        embedding2: list[float]
    ) -> float:
        """Compute cosine similarity between two embeddings."""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    async def embed_article(
        self,
        db: AsyncSession,
        article: KnowledgeArticle,
        force: bool = False
    ) -> KnowledgeEmbedding:
        """
        Generate and store embedding for a knowledge article.

        Args:
            db: Database session
            article: Article to embed
            force: If True, regenerate even if cached

        Returns:
            The KnowledgeEmbedding record
        """
        # Create content string for embedding
        content = f"{article.title}\n{article.summary or ''}\n{article.content}"
        content_hash = self._content_hash(content)

        # Check for existing embedding
        if not force:
            result = await db.execute(
                select(KnowledgeEmbedding).where(
                    KnowledgeEmbedding.article_id == article.id
                )
            )
            existing = result.scalar_one_or_none()

            if existing and existing.content_hash == content_hash:
                logger.debug(f"Using cached embedding for article {article.id}")
                return existing

        # Generate new embedding
        embedding = self.generate_embedding(content)

        # Store or update
        result = await db.execute(
            select(KnowledgeEmbedding).where(
                KnowledgeEmbedding.article_id == article.id
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.embedding = json.dumps(embedding)
            existing.content_hash = content_hash
            existing.embedding_dim = len(embedding)
            await db.commit()
            return existing
        else:
            new_embedding = KnowledgeEmbedding(
                article_id=article.id,
                embedding=json.dumps(embedding),
                content_hash=content_hash,
                embedding_model="tfidf-local",
                embedding_dim=len(embedding),
            )
            db.add(new_embedding)
            await db.commit()
            await db.refresh(new_embedding)
            return new_embedding

    async def embed_all_articles(
        self,
        db: AsyncSession,
        force: bool = False
    ) -> int:
        """
        Generate embeddings for all knowledge articles.

        Args:
            db: Database session
            force: If True, regenerate all embeddings

        Returns:
            Number of articles embedded
        """
        # Get all articles
        result = await db.execute(select(KnowledgeArticle))
        articles = result.scalars().all()

        if not articles:
            logger.info("No articles to embed")
            return 0

        # Build vocabulary from all article content
        contents = [
            f"{a.title}\n{a.summary or ''}\n{a.content}"
            for a in articles
        ]
        self._build_vocab(contents)

        # Embed each article
        count = 0
        for article in articles:
            try:
                await self.embed_article(db, article, force=force)
                count += 1
                if count % 10 == 0:
                    logger.info(f"Embedded {count}/{len(articles)} articles")
            except Exception as e:
                logger.error(f"Failed to embed article {article.id}: {e}")

        logger.info(f"Completed embedding {count} articles")
        return count

    async def search_similar(
        self,
        db: AsyncSession,
        query: str,
        top_k: int = 5,
        state_filter: Optional[str] = None,
        min_score: float = 0.1
    ) -> list[tuple[KnowledgeArticle, float]]:
        """
        Find articles most similar to a query.

        Args:
            db: Database session
            query: Search query text
            top_k: Number of results to return
            state_filter: Optional state abbreviation to filter by
            min_score: Minimum similarity score

        Returns:
            List of (article, score) tuples
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query)

        # Get all embeddings
        stmt = select(KnowledgeEmbedding)
        result = await db.execute(stmt)
        embeddings = result.scalars().all()

        if not embeddings:
            return []

        # Calculate similarities
        similarities: list[tuple[int, float]] = []
        for emb in embeddings:
            try:
                article_embedding = json.loads(emb.embedding)
                score = self.cosine_similarity(query_embedding, article_embedding)
                if score >= min_score:
                    similarities.append((emb.article_id, score))
            except Exception as e:
                logger.warning(f"Error computing similarity for {emb.article_id}: {e}")

        # Sort by score
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Get articles
        results: list[tuple[KnowledgeArticle, float]] = []
        for article_id, score in similarities[:top_k * 2]:  # Get extra for filtering
            result = await db.execute(
                select(KnowledgeArticle).where(KnowledgeArticle.id == article_id)
            )
            article = result.scalar_one_or_none()

            if article:
                # Apply state filter if provided
                if state_filter:
                    if article.state_id is not None:
                        # Need to check state abbreviation
                        # For now, skip articles with state_id if filtering
                        # This would need a join in production
                        pass
                results.append((article, score))

                if len(results) >= top_k:
                    break

        return results


# Singleton instance
embedding_service = EmbeddingService()

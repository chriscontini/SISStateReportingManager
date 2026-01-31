"""
Script to generate embeddings for all knowledge articles.

Run with: python -m src.backend.embed_articles
"""

import asyncio
import logging
import sys

from .database import get_engine, AsyncSessionLocal
from .services.embedding_service import embedding_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Generate embeddings for all knowledge articles."""
    logger.info("Starting embedding generation for knowledge articles...")

    async with AsyncSessionLocal() as db:
        try:
            count = await embedding_service.embed_all_articles(db=db, force=False)
            logger.info(f"Successfully embedded {count} articles")
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            sys.exit(1)

    logger.info("Embedding generation complete!")


if __name__ == "__main__":
    asyncio.run(main())

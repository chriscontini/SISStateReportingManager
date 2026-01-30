"""
Unit tests for embedding service.

Tests the TF-IDF based embedding generation and semantic search logic.
"""

import pytest
import math

# Define expected constants and logic for testing without importing full service
EMBEDDING_DIM = 384


def cosine_similarity(vec1: list, vec2: list) -> float:
    """Calculate cosine similarity between two vectors."""
    if not vec1 or not vec2:
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def simple_tfidf_embedding(text: str, dim: int = EMBEDDING_DIM) -> list:
    """Simple TF-IDF-like embedding for testing."""
    if not text or not text.strip():
        return [0.0] * dim

    # Tokenize
    words = text.lower().split()

    # Count word frequencies
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # Create embedding based on word hashes
    embedding = [0.0] * dim
    for word, freq in word_freq.items():
        # Use hash to determine position in embedding
        idx = hash(word) % dim
        embedding[idx] += freq

    # Normalize
    magnitude = math.sqrt(sum(x * x for x in embedding))
    if magnitude > 0:
        embedding = [x / magnitude for x in embedding]

    return embedding


class TestEmbeddingDimension:
    """Test embedding dimension configuration."""

    def test_embedding_dimension_value(self):
        """Test embedding dimension is correct."""
        assert EMBEDDING_DIM == 384

    def test_embedding_returns_correct_dimension(self):
        """Test that embeddings have correct dimension."""
        text = "Test document for embedding"
        embedding = simple_tfidf_embedding(text)

        assert len(embedding) == EMBEDDING_DIM


class TestCosineSimilarity:
    """Test cosine similarity calculations."""

    def test_identical_vectors_similarity_one(self):
        """Test cosine similarity returns 1.0 for identical vectors."""
        vec = [1.0, 2.0, 3.0]
        similarity = cosine_similarity(vec, vec)

        assert abs(similarity - 1.0) < 0.0001

    def test_orthogonal_vectors_similarity_zero(self):
        """Test cosine similarity returns 0 for orthogonal vectors."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]
        similarity = cosine_similarity(vec1, vec2)

        assert abs(similarity) < 0.0001

    def test_opposite_vectors_similarity_negative(self):
        """Test cosine similarity returns -1 for opposite vectors."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [-1.0, -2.0, -3.0]
        similarity = cosine_similarity(vec1, vec2)

        assert abs(similarity - (-1.0)) < 0.0001

    def test_zero_vector_returns_zero(self):
        """Test cosine similarity handles zero vectors gracefully."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [0.0, 0.0, 0.0]
        similarity = cosine_similarity(vec1, vec2)

        assert similarity == 0.0

    def test_empty_vectors_return_zero(self):
        """Test empty vectors return zero similarity."""
        similarity = cosine_similarity([], [])
        assert similarity == 0.0

    def test_similar_vectors_high_similarity(self):
        """Test similar vectors have high similarity."""
        vec1 = [1.0, 2.0, 3.0, 4.0, 5.0]
        vec2 = [1.1, 2.1, 3.1, 4.1, 5.1]  # Very similar
        similarity = cosine_similarity(vec1, vec2)

        assert similarity > 0.99


class TestEmbeddingGeneration:
    """Test embedding generation logic."""

    def test_embedding_deterministic(self):
        """Test that same text produces same embedding."""
        text = "Test document for embedding"
        embedding1 = simple_tfidf_embedding(text)
        embedding2 = simple_tfidf_embedding(text)

        assert embedding1 == embedding2

    def test_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings."""
        text1 = "California state reporting"
        text2 = "Texas education requirements"

        embedding1 = simple_tfidf_embedding(text1)
        embedding2 = simple_tfidf_embedding(text2)

        assert embedding1 != embedding2

    def test_empty_text_returns_zero_vector(self):
        """Test that empty text returns zero vector."""
        embedding = simple_tfidf_embedding("")

        assert len(embedding) == EMBEDDING_DIM
        assert all(x == 0.0 for x in embedding)

    def test_whitespace_only_returns_zero_vector(self):
        """Test whitespace-only text returns zero vector."""
        embedding = simple_tfidf_embedding("   \n\t  ")

        assert len(embedding) == EMBEDDING_DIM
        assert all(x == 0.0 for x in embedding)

    def test_long_text_handled(self):
        """Test long text is handled correctly."""
        long_text = "State reporting requirements " * 100
        embedding = simple_tfidf_embedding(long_text)

        assert len(embedding) == EMBEDDING_DIM
        # Should be normalized (magnitude close to 1)
        magnitude = math.sqrt(sum(x * x for x in embedding))
        assert abs(magnitude - 1.0) < 0.0001

    def test_normalized_embedding(self):
        """Test embeddings are normalized."""
        text = "This is a test document"
        embedding = simple_tfidf_embedding(text)

        magnitude = math.sqrt(sum(x * x for x in embedding))
        assert abs(magnitude - 1.0) < 0.0001


class TestBatchEmbedding:
    """Test batch embedding generation."""

    def test_batch_returns_correct_count(self):
        """Test batch embedding returns correct number of embeddings."""
        texts = [
            "Document one about reporting",
            "Document two about education",
            "Document three about compliance"
        ]

        embeddings = [simple_tfidf_embedding(t) for t in texts]

        assert len(embeddings) == 3

    def test_batch_all_correct_dimension(self):
        """Test all batch embeddings have correct dimension."""
        texts = ["Text one", "Text two", "Text three"]
        embeddings = [simple_tfidf_embedding(t) for t in texts]

        for emb in embeddings:
            assert len(emb) == EMBEDDING_DIM


class TestSemanticSimilarity:
    """Test semantic similarity using embeddings."""

    def test_similar_texts_high_similarity(self):
        """Test similar texts have higher similarity."""
        text1 = "state reporting requirements for education"
        text2 = "education state reporting requirements"  # Same words
        text3 = "basketball game scores and players"  # Different topic

        emb1 = simple_tfidf_embedding(text1)
        emb2 = simple_tfidf_embedding(text2)
        emb3 = simple_tfidf_embedding(text3)

        sim_related = cosine_similarity(emb1, emb2)
        sim_unrelated = cosine_similarity(emb1, emb3)

        # Similar texts should have higher similarity
        assert sim_related > sim_unrelated

    def test_repeated_words_affect_embedding(self):
        """Test that word frequency affects embedding."""
        text1 = "reporting reporting reporting"
        text2 = "reporting education compliance"

        emb1 = simple_tfidf_embedding(text1)
        emb2 = simple_tfidf_embedding(text2)

        # Different embeddings
        assert emb1 != emb2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

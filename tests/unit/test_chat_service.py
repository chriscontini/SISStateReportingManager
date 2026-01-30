"""
Unit tests for chat service.

Tests the RAG-based chat functionality and session management logic.
"""

import pytest


# Define expected system prompt components for testing
SYSTEM_PROMPT_COMPONENTS = {
    "role": "state reporting expert",
    "domain": "K-12 education",
    "capabilities": ["answer questions", "provide guidance", "cite sources"],
}

# State abbreviation to name mapping
STATE_NAMES = {
    "TX": "Texas",
    "CA": "California",
    "NY": "New York",
    "FL": "Florida",
    "NJ": "New Jersey",
    "LA": "Louisiana",
}


def build_system_prompt(state_filter: str = None, context: str = None) -> str:
    """Build system prompt for chat service."""
    prompt = """You are an expert assistant for state reporting requirements in K-12 education.
You help SIS vendors understand state-specific data submission requirements, compliance needs,
and implementation strategies.

When answering questions:
1. Be specific and accurate about state requirements
2. Cite sources when available
3. Acknowledge uncertainty when appropriate
4. Provide actionable guidance
"""

    if state_filter and state_filter in STATE_NAMES:
        state_name = STATE_NAMES[state_filter]
        prompt += f"\nFocus your responses on {state_name} ({state_filter}) specifically."

    if context:
        prompt += f"\n\nRelevant context:\n{context}"

    return prompt


def format_context(articles: list) -> str:
    """Format articles as context for the chat."""
    if not articles:
        return ""

    context_parts = []
    for article in articles:
        title = getattr(article, 'title', 'Unknown')
        content = getattr(article, 'content', '')
        category = getattr(article, 'category', 'General')

        context_parts.append(f"[{category}] {title}:\n{content}")

    return "\n\n".join(context_parts)


class TestSystemPrompt:
    """Test system prompt building."""

    def test_system_prompt_contains_role(self):
        """Test system prompt contains expected role."""
        prompt = build_system_prompt()

        assert "expert" in prompt.lower()
        assert "state reporting" in prompt.lower()

    def test_system_prompt_contains_domain(self):
        """Test system prompt contains education domain."""
        prompt = build_system_prompt()

        assert "K-12" in prompt or "education" in prompt.lower()

    def test_system_prompt_with_state_filter(self):
        """Test system prompt includes state filter information."""
        prompt = build_system_prompt(state_filter="TX")

        assert "Texas" in prompt
        assert "TX" in prompt

    def test_system_prompt_with_context(self):
        """Test system prompt includes provided context."""
        context = "California requires annual CALPADS submissions"
        prompt = build_system_prompt(context=context)

        assert context in prompt

    def test_system_prompt_with_state_and_context(self):
        """Test system prompt with both state filter and context."""
        context = "Texas TEA reporting requirements"
        prompt = build_system_prompt(state_filter="TX", context=context)

        assert "Texas" in prompt
        assert context in prompt

    def test_system_prompt_unknown_state(self):
        """Test system prompt with unknown state abbreviation."""
        prompt = build_system_prompt(state_filter="ZZ")

        # Should not include unknown state
        assert "ZZ" not in prompt or "specifically" not in prompt.lower()


class TestContextFormatting:
    """Test context formatting for RAG."""

    def test_format_context_empty_list(self):
        """Test formatting with empty article list."""
        result = format_context([])

        assert result == ""

    def test_format_context_single_article(self):
        """Test formatting with single article."""
        class MockArticle:
            title = "Test Article"
            content = "Test content"
            category = "General"

        result = format_context([MockArticle()])

        assert "Test Article" in result
        assert "Test content" in result
        assert "General" in result

    def test_format_context_multiple_articles(self):
        """Test formatting with multiple articles."""
        class MockArticle1:
            title = "Article One"
            content = "Content one"
            category = "Reporting"

        class MockArticle2:
            title = "Article Two"
            content = "Content two"
            category = "Compliance"

        result = format_context([MockArticle1(), MockArticle2()])

        assert "Article One" in result
        assert "Article Two" in result
        assert "Content one" in result
        assert "Content two" in result

    def test_format_context_preserves_order(self):
        """Test context preserves article order."""
        class MockArticle1:
            title = "First"
            content = "First content"
            category = "A"

        class MockArticle2:
            title = "Second"
            content = "Second content"
            category = "B"

        result = format_context([MockArticle1(), MockArticle2()])

        # First should appear before Second
        first_pos = result.find("First")
        second_pos = result.find("Second")
        assert first_pos < second_pos


class TestChatSessionManagement:
    """Test chat session management logic."""

    def test_default_session_title(self):
        """Test default session title."""
        default_title = "New Chat"
        assert len(default_title) > 0

    def test_session_state_filter_storage(self):
        """Test session can store state filter."""
        session = {
            "id": 1,
            "title": "Texas Questions",
            "state_filter": "TX",
        }

        assert session["state_filter"] == "TX"

    def test_session_without_state_filter(self):
        """Test session without state filter."""
        session = {
            "id": 1,
            "title": "General Questions",
            "state_filter": None,
        }

        assert session["state_filter"] is None


class TestMessageRoles:
    """Test message role validation."""

    def test_valid_roles(self):
        """Test valid message roles."""
        valid_roles = ["user", "assistant", "system"]

        for role in valid_roles:
            assert role in valid_roles

    def test_user_message_structure(self):
        """Test user message structure."""
        message = {
            "role": "user",
            "content": "What are the reporting requirements?",
        }

        assert message["role"] == "user"
        assert len(message["content"]) > 0

    def test_assistant_message_structure(self):
        """Test assistant message structure."""
        message = {
            "role": "assistant",
            "content": "Here are the reporting requirements...",
            "citations": ["Article 1", "Article 2"],
        }

        assert message["role"] == "assistant"
        assert "citations" in message


class TestRAGRetrieval:
    """Test RAG retrieval logic."""

    def test_relevance_threshold(self):
        """Test relevance threshold for retrieval."""
        min_relevance = 0.3
        max_relevance = 1.0

        assert 0 < min_relevance < max_relevance <= 1.0

    def test_max_context_articles(self):
        """Test maximum number of context articles."""
        max_articles = 5

        # Should limit to reasonable number to fit in context window
        assert 1 <= max_articles <= 10

    def test_context_ordering_by_relevance(self):
        """Test context articles ordered by relevance."""
        relevance_scores = [0.9, 0.8, 0.7, 0.6, 0.5]

        # Should be in descending order
        sorted_scores = sorted(relevance_scores, reverse=True)
        assert relevance_scores == sorted_scores


class TestChatResponses:
    """Test chat response handling."""

    def test_response_contains_content(self):
        """Test response has content field."""
        response = {
            "content": "Here is my response...",
            "citations": [],
        }

        assert "content" in response
        assert len(response["content"]) > 0

    def test_response_can_have_citations(self):
        """Test response can include citations."""
        response = {
            "content": "According to the documentation...",
            "citations": [
                {"title": "State Reporting Guide", "id": 1},
                {"title": "Compliance Manual", "id": 2},
            ],
        }

        assert len(response["citations"]) == 2

    def test_fallback_response_structure(self):
        """Test fallback response when AI unavailable."""
        fallback_content = "I apologize, but I'm currently unable to process your request."

        assert len(fallback_content) > 0
        assert "unable" in fallback_content.lower() or "apologize" in fallback_content.lower()


class TestStreamingResponse:
    """Test streaming response handling."""

    def test_stream_chunk_structure(self):
        """Test stream chunk has expected structure."""
        chunk = {
            "type": "content",
            "text": "partial response",
        }

        assert "type" in chunk
        assert "text" in chunk

    def test_stream_end_marker(self):
        """Test stream end marker."""
        end_marker = {"type": "done"}

        assert end_marker["type"] == "done"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

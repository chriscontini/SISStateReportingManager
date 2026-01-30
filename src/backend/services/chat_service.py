"""
Chat service for AI-powered conversational assistant.

Implements RAG (Retrieval-Augmented Generation) using the knowledge base
to provide grounded responses about state reporting requirements.
"""

import json
import logging
from datetime import datetime
from typing import Optional, AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..models import ChatSession, ChatMessage, KnowledgeArticle
from .embedding_service import embedding_service

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service for AI chat interactions with RAG support.

    Provides methods for:
    - Creating and managing chat sessions
    - Sending messages with context retrieval
    - Streaming responses
    """

    def __init__(self):
        self._client = None

    def _get_client(self):
        """Get or create the Anthropic client."""
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
                if settings.claude_api_key:
                    self._client = AsyncAnthropic(api_key=settings.claude_api_key)
            except ImportError:
                logger.warning("Anthropic package not installed")
        return self._client

    async def create_session(
        self,
        db: AsyncSession,
        title: str = "New Chat",
        state_filter: Optional[str] = None,
        context: Optional[str] = None
    ) -> ChatSession:
        """Create a new chat session."""
        session = ChatSession(
            title=title,
            state_filter=state_filter,
            context=context
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def get_session(
        self,
        db: AsyncSession,
        session_id: int
    ) -> Optional[ChatSession]:
        """Get a chat session by ID."""
        result = await db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_sessions(
        self,
        db: AsyncSession,
        limit: int = 20
    ) -> list[ChatSession]:
        """List recent chat sessions."""
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.is_active == True)
            .order_by(ChatSession.updated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def delete_session(
        self,
        db: AsyncSession,
        session_id: int
    ) -> bool:
        """Delete (deactivate) a chat session."""
        session = await self.get_session(db, session_id)
        if session:
            session.is_active = False
            await db.commit()
            return True
        return False

    async def get_messages(
        self,
        db: AsyncSession,
        session_id: int
    ) -> list[ChatMessage]:
        """Get all messages in a session."""
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at)
        )
        return list(result.scalars().all())

    async def _retrieve_context(
        self,
        db: AsyncSession,
        query: str,
        state_filter: Optional[str] = None,
        top_k: int = 3
    ) -> list[tuple[KnowledgeArticle, float]]:
        """Retrieve relevant knowledge articles for context."""
        return await embedding_service.search_similar(
            db=db,
            query=query,
            top_k=top_k,
            state_filter=state_filter
        )

    def _format_context(
        self,
        articles: list[tuple[KnowledgeArticle, float]]
    ) -> str:
        """Format retrieved articles as context for the prompt."""
        if not articles:
            return ""

        context_parts = ["Here is relevant information from the knowledge base:\n"]

        for i, (article, score) in enumerate(articles, 1):
            context_parts.append(f"[Source {i}: {article.title}]")
            context_parts.append(article.content[:1500])  # Limit content length
            if article.source_url:
                context_parts.append(f"Source URL: {article.source_url}")
            context_parts.append("")

        return "\n".join(context_parts)

    def _build_system_prompt(
        self,
        state_filter: Optional[str] = None
    ) -> str:
        """Build the system prompt for the chat."""
        base_prompt = """You are an expert AI assistant for SIS (Student Information System) state expansion planning.
You help development teams understand state reporting requirements, compare states, and plan implementations.

Your knowledge covers:
- K-12 state reporting requirements for all 50 US states
- Data element definitions and CEDS mappings
- Submission formats and validation rules
- Certification processes
- Competitive landscape
- Implementation best practices

Guidelines:
- Always cite your sources using [Source N] format when referencing knowledge base content
- If you're not sure about something, say so
- Be concise and technical when appropriate
- When comparing states, highlight key differences
- For implementation questions, reference the LA benchmark (30 months, 15,000 hours, 5 FTE)"""

        if state_filter:
            base_prompt += f"\n\nThe user is currently focused on {state_filter}. Prioritize information about this state."

        return base_prompt

    async def send_message(
        self,
        db: AsyncSession,
        session_id: int,
        user_message: str
    ) -> ChatMessage:
        """
        Send a message and get a response.

        Args:
            db: Database session
            session_id: Chat session ID
            user_message: The user's message

        Returns:
            The assistant's response message
        """
        # Get session
        session = await self.get_session(db, session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Save user message
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=user_message
        )
        db.add(user_msg)
        await db.commit()

        # Retrieve context
        relevant_articles = await self._retrieve_context(
            db=db,
            query=user_message,
            state_filter=session.state_filter
        )

        # Get conversation history
        messages = await self.get_messages(db, session_id)
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages[-10:]  # Last 10 messages for context
        ]

        # Build prompt with context
        context = self._format_context(relevant_articles)
        system_prompt = self._build_system_prompt(session.state_filter)

        if context:
            augmented_message = f"{context}\n\nUser question: {user_message}"
        else:
            augmented_message = user_message

        # Prepare messages for Claude
        claude_messages = history[:-1]  # Exclude the just-added user message
        claude_messages.append({"role": "user", "content": augmented_message})

        # Generate response
        response_text = await self._generate_response(
            system_prompt=system_prompt,
            messages=claude_messages
        )

        # Extract citations
        citations = [
            article.id for article, _ in relevant_articles
        ] if relevant_articles else []

        # Save assistant message
        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=response_text,
            citations=json.dumps(citations) if citations else None,
            model_used="claude-sonnet-4-20250514"
        )
        db.add(assistant_msg)

        # Update session title if first message
        if len(messages) <= 1:
            # Generate title from first message
            session.title = user_message[:50] + ("..." if len(user_message) > 50 else "")

        session.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(assistant_msg)

        return assistant_msg

    async def _generate_response(
        self,
        system_prompt: str,
        messages: list[dict]
    ) -> str:
        """Generate a response using Claude."""
        client = self._get_client()

        if client is None:
            # Fallback response when API is not available
            return self._fallback_response(messages[-1]["content"] if messages else "")

        try:
            response = await client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                system=system_prompt,
                messages=messages
            )
            return response.content[0].text

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error generating a response. Please try again. Error: {str(e)}"

    def _fallback_response(self, query: str) -> str:
        """Generate a fallback response when API is unavailable."""
        return """I apologize, but I'm currently unable to generate a detailed response as the AI service is not available.

To get information about state reporting requirements, you can:
1. Check the Knowledge Base for relevant articles
2. Use the State Rankings page to compare states
3. Review the Gap Analysis for specific states

Please ensure the ANTHROPIC_API_KEY is configured in your environment."""

    async def stream_message(
        self,
        db: AsyncSession,
        session_id: int,
        user_message: str
    ) -> AsyncIterator[str]:
        """
        Send a message and stream the response.

        Yields chunks of the response as they are generated.
        """
        # Get session
        session = await self.get_session(db, session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Save user message
        user_msg = ChatMessage(
            session_id=session_id,
            role="user",
            content=user_message
        )
        db.add(user_msg)
        await db.commit()

        # Retrieve context
        relevant_articles = await self._retrieve_context(
            db=db,
            query=user_message,
            state_filter=session.state_filter
        )

        # Get conversation history
        messages = await self.get_messages(db, session_id)
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages[-10:]
        ]

        # Build prompt with context
        context = self._format_context(relevant_articles)
        system_prompt = self._build_system_prompt(session.state_filter)

        if context:
            augmented_message = f"{context}\n\nUser question: {user_message}"
        else:
            augmented_message = user_message

        claude_messages = history[:-1]
        claude_messages.append({"role": "user", "content": augmented_message})

        # Stream response
        client = self._get_client()
        full_response = ""

        if client is None:
            # Fallback for when API is unavailable
            fallback = self._fallback_response(user_message)
            yield fallback
            full_response = fallback
        else:
            try:
                async with client.messages.stream(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2048,
                    system=system_prompt,
                    messages=claude_messages
                ) as stream:
                    async for text in stream.text_stream:
                        yield text
                        full_response += text
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                yield error_msg
                full_response = error_msg

        # Save assistant message
        citations = [
            article.id for article, _ in relevant_articles
        ] if relevant_articles else []

        assistant_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=full_response,
            citations=json.dumps(citations) if citations else None,
            model_used="claude-sonnet-4-20250514"
        )
        db.add(assistant_msg)

        # Update session
        if len(messages) <= 1:
            session.title = user_message[:50] + ("..." if len(user_message) > 50 else "")

        session.updated_at = datetime.utcnow()
        await db.commit()


# Singleton instance
chat_service = ChatService()

"""
Chat API router for AI assistant functionality.

Provides endpoints for:
- Creating and managing chat sessions
- Sending messages and receiving responses
- Streaming responses
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


# Request/Response Models

class CreateSessionRequest(BaseModel):
    title: Optional[str] = "New Chat"
    state_filter: Optional[str] = None
    context: Optional[str] = None


class CreateSessionResponse(BaseModel):
    id: int
    title: str
    state_filter: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class SendMessageRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    citations: Optional[list[int]] = None
    created_at: str

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: int
    title: str
    state_filter: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    sessions: list[SessionResponse]


# Endpoints

@router.post("/sessions", response_model=CreateSessionResponse)
async def create_session(
    request: CreateSessionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a new chat session."""
    session = await chat_service.create_session(
        db=db,
        title=request.title or "New Chat",
        state_filter=request.state_filter,
        context=request.context
    )
    return CreateSessionResponse(
        id=session.id,
        title=session.title,
        state_filter=session.state_filter,
        created_at=session.created_at.isoformat()
    )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List recent chat sessions."""
    sessions = await chat_service.list_sessions(db=db, limit=limit)
    return SessionListResponse(
        sessions=[
            SessionResponse(
                id=s.id,
                title=s.title,
                state_filter=s.state_filter,
                is_active=s.is_active,
                created_at=s.created_at.isoformat(),
                updated_at=s.updated_at.isoformat()
            )
            for s in sessions
        ]
    )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a chat session with all messages."""
    session = await chat_service.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = await chat_service.get_messages(db=db, session_id=session_id)

    return SessionResponse(
        id=session.id,
        title=session.title,
        state_filter=session.state_filter,
        is_active=session.is_active,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
        messages=[
            MessageResponse(
                id=m.id,
                role=m.role,
                content=m.content,
                citations=_parse_citations(m.citations),
                created_at=m.created_at.isoformat()
            )
            for m in messages
        ]
    )


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete (deactivate) a chat session."""
    success = await chat_service.delete_session(db=db, session_id=session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted", "session_id": session_id}


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: int,
    request: SendMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a message and get a response."""
    session = await chat_service.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    try:
        response_msg = await chat_service.send_message(
            db=db,
            session_id=session_id,
            user_message=request.content
        )

        return MessageResponse(
            id=response_msg.id,
            role=response_msg.role,
            content=response_msg.content,
            citations=_parse_citations(response_msg.citations),
            created_at=response_msg.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.post("/sessions/{session_id}/messages/stream")
async def stream_message(
    session_id: int,
    request: SendMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a message and stream the response using Server-Sent Events."""
    session = await chat_service.get_session(db=db, session_id=session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    async def generate():
        try:
            async for chunk in chat_service.stream_message(
                db=db,
                session_id=session_id,
                user_message=request.content
            ):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


def _parse_citations(citations_json: Optional[str]) -> Optional[list[int]]:
    """Parse citations JSON string to list of article IDs."""
    if not citations_json:
        return None
    try:
        import json
        return json.loads(citations_json)
    except:
        return None

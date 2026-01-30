"""
Integration tests for main API endpoints.

These tests verify API endpoints work correctly with the database.
"""

import pytest
from httpx import AsyncClient, ASGITransport
import sys

sys.path.insert(0, '/home/user/SISStateReportingManager/src/backend')


@pytest.fixture
def app():
    """Get the FastAPI application."""
    from main import app
    return app


@pytest.fixture
async def client(app):
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    """Test health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self, client):
        """Test /health returns success status."""
        response = await client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] in ["ok", "degraded"]
        assert "timestamp" in data
        assert "version" in data

    @pytest.mark.asyncio
    async def test_health_includes_database_status(self, client):
        """Test /health includes database connectivity info."""
        response = await client.get("/health")
        data = response.json()

        assert "database" in data
        assert "status" in data["database"]


class TestRootEndpoint:
    """Test root endpoint."""

    @pytest.mark.asyncio
    async def test_root_returns_api_info(self, client):
        """Test / returns API information."""
        response = await client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "SISStateReportingManager API"
        assert "version" in data
        assert "endpoints" in data

    @pytest.mark.asyncio
    async def test_root_lists_endpoints(self, client):
        """Test / lists all available endpoints."""
        response = await client.get("/")
        data = response.json()

        expected_endpoints = ["states", "rankings", "auth", "gap_analysis", "roadmaps", "knowledge", "chat"]
        for endpoint in expected_endpoints:
            assert endpoint in data["endpoints"], f"Missing endpoint: {endpoint}"


class TestAdminStatsEndpoint:
    """Test admin statistics endpoint."""

    @pytest.mark.asyncio
    async def test_admin_stats_returns_counts(self, client):
        """Test /api/admin/stats returns record counts."""
        response = await client.get("/api/admin/stats")
        assert response.status_code == 200

        data = response.json()
        assert "counts" in data
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_admin_stats_includes_expected_models(self, client):
        """Test admin stats includes counts for all main models."""
        response = await client.get("/api/admin/stats")
        data = response.json()

        expected_models = ["states", "roadmaps", "knowledge_articles", "chat_sessions"]
        for model in expected_models:
            assert model in data["counts"], f"Missing count for: {model}"


class TestStatesEndpoint:
    """Test states API endpoints."""

    @pytest.mark.asyncio
    async def test_list_states_returns_list(self, client):
        """Test GET /api/states returns a list."""
        response = await client.get("/api/states")

        # May return empty list if not seeded
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_states_have_required_fields(self, client):
        """Test state objects have required fields."""
        response = await client.get("/api/states")
        states = response.json()

        if len(states) > 0:
            state = states[0]
            assert "id" in state
            assert "name" in state
            assert "abbreviation" in state


class TestAuthEndpoint:
    """Test authentication endpoints."""

    @pytest.mark.asyncio
    async def test_login_requires_password(self, client):
        """Test login fails without password."""
        response = await client.post("/api/auth/login", json={})
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(self, client):
        """Test login fails with wrong password."""
        response = await client.post(
            "/api/auth/login",
            json={"password": "wrong_password_12345"}
        )
        assert response.status_code == 401


class TestRankingsEndpoint:
    """Test rankings API endpoints."""

    @pytest.mark.asyncio
    async def test_get_rankings_returns_data(self, client):
        """Test GET /api/rankings returns rankings data."""
        response = await client.get("/api/rankings")
        assert response.status_code == 200

        data = response.json()
        assert "rankings" in data or isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_factors_returns_list(self, client):
        """Test GET /api/rankings/factors returns factors."""
        response = await client.get("/api/rankings/factors")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)


class TestKnowledgeEndpoint:
    """Test knowledge base API endpoints."""

    @pytest.mark.asyncio
    async def test_list_articles_returns_list(self, client):
        """Test GET /api/knowledge/articles returns list."""
        response = await client.get("/api/knowledge/articles")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_get_categories_returns_list(self, client):
        """Test GET /api/knowledge/categories returns list."""
        response = await client.get("/api/knowledge/categories")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio
    async def test_search_requires_query(self, client):
        """Test search endpoint requires query parameter."""
        response = await client.get("/api/knowledge/search")
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_search_with_query(self, client):
        """Test search with valid query."""
        response = await client.get("/api/knowledge/search?q=reporting")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestRoadmapsEndpoint:
    """Test roadmaps API endpoints."""

    @pytest.mark.asyncio
    async def test_list_roadmaps_returns_list(self, client):
        """Test GET /api/roadmaps returns list."""
        response = await client.get("/api/roadmaps/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestChatEndpoint:
    """Test chat API endpoints."""

    @pytest.mark.asyncio
    async def test_list_sessions_returns_list(self, client):
        """Test GET /api/chat/sessions returns list."""
        response = await client.get("/api/chat/sessions")
        assert response.status_code == 200

        data = response.json()
        assert "sessions" in data
        assert isinstance(data["sessions"], list)

    @pytest.mark.asyncio
    async def test_create_session(self, client):
        """Test POST /api/chat/sessions creates a new session."""
        response = await client.post(
            "/api/chat/sessions",
            json={"title": "Test Session"}
        )
        assert response.status_code == 200

        data = response.json()
        assert "session_id" in data
        assert data["title"] == "Test Session"

    @pytest.mark.asyncio
    async def test_create_session_with_state_filter(self, client):
        """Test creating session with state filter."""
        response = await client.post(
            "/api/chat/sessions",
            json={
                "title": "Texas Questions",
                "state_filter": "TX"
            }
        )
        assert response.status_code == 200

        data = response.json()
        assert data["state_filter"] == "TX"

    @pytest.mark.asyncio
    async def test_get_session_not_found(self, client):
        """Test GET /api/chat/sessions/{id} returns 404 for non-existent session."""
        response = await client.get("/api/chat/sessions/99999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_session(self, client):
        """Test DELETE /api/chat/sessions/{id} deletes session."""
        # First create a session
        create_response = await client.post(
            "/api/chat/sessions",
            json={"title": "To Delete"}
        )
        session_id = create_response.json()["session_id"]

        # Then delete it
        delete_response = await client.delete(f"/api/chat/sessions/{session_id}")
        assert delete_response.status_code == 200

        # Verify it's deleted
        get_response = await client.get(f"/api/chat/sessions/{session_id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_send_message_to_session(self, client):
        """Test POST /api/chat/sessions/{id}/messages sends a message."""
        # First create a session
        create_response = await client.post(
            "/api/chat/sessions",
            json={"title": "Message Test"}
        )
        session_id = create_response.json()["session_id"]

        # Send a message
        message_response = await client.post(
            f"/api/chat/sessions/{session_id}/messages",
            json={"content": "Hello, what is state reporting?"}
        )
        assert message_response.status_code == 200

        data = message_response.json()
        assert "content" in data
        assert data["role"] == "assistant"

    @pytest.mark.asyncio
    async def test_send_message_requires_content(self, client):
        """Test message endpoint requires content field."""
        # First create a session
        create_response = await client.post(
            "/api/chat/sessions",
            json={"title": "Validation Test"}
        )
        session_id = create_response.json()["session_id"]

        # Try to send message without content
        response = await client.post(
            f"/api/chat/sessions/{session_id}/messages",
            json={}
        )
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_send_message_to_nonexistent_session(self, client):
        """Test sending message to non-existent session returns 404."""
        response = await client.post(
            "/api/chat/sessions/99999/messages",
            json={"content": "Hello"}
        )
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

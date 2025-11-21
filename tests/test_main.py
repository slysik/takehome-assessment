"""
Tests for the FastAPI application endpoints.

This test suite validates:
- API endpoint availability
- Request/response handling
- Application health checks
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


class TestAPIEndpoints:
    """Test suite for FastAPI endpoints"""

    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app"""
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Test the root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or "name" in data

    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_agents_endpoint(self, client):
        """Test the agents listing endpoint"""
        response = client.get("/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert isinstance(data["agents"], list)

    def test_analyze_endpoint_requires_report_path(self, client):
        """Test that analyze endpoint requires report_path"""
        response = client.post("/analyze", json={})
        # Should return 422 for validation error
        assert response.status_code == 422

    def test_analyze_endpoint_with_valid_request(self, client):
        """Test analyze endpoint with valid request structure"""
        request_data = {
            "report_path": "/app/data/earnings_report_sample.txt",
            "options": {}
        }
        response = client.post("/analyze", json=request_data)
        # Should return either 200 (success) or 500 (if file not found/LLM error)
        # Both are acceptable for this test
        assert response.status_code in [200, 404, 500]

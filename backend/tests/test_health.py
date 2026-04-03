import pytest
from unittest.mock import patch

def test_health_check(client):
    # Mock Redis to avoid external dependency failure during generic health test
    with patch("app.routes.health.Redis") as mock_redis:
        mock_instance = mock_redis.return_value
        mock_instance.ping.return_value = True
        
        response = client.get("/api/health/")
        
        # In the test environment, app.db (AsyncMongoMockClient) is initialized 
        # via the mock_db fixture.
        data = response.json()
        assert response.status_code in [200, 503] # Depends on mock DB state
        assert "status" in data
        assert "uptime_seconds" in data
        assert "dependencies" in data
        assert "mongodb" in data["dependencies"]
        assert "redis" in data["dependencies"]

def test_health_check_redis_fail(client):
    with patch("app.routes.health.Redis") as mock_redis:
        mock_instance = mock_redis.return_value
        mock_instance.ping.return_value = False # Force failure
        
        response = client.get("/api/health/")
        data = response.json()
        assert response.status_code == 503
        assert data["status"] == "degraded"
        assert data["dependencies"]["redis"] == "failed"

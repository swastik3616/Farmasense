import pytest
from unittest.mock import patch, MagicMock

def test_health_check_success(client):
    """Test health check with all systems UP."""
    with patch("app.routes.health.Redis") as mock_redis:
        mock_instance = mock_redis.return_value
        mock_instance.ping.return_value = True
        
        response = client.get("/api/health/")
        
        data = response.json
        assert response.status_code in [200, 503]
        assert "status" in data
        assert "uptime_seconds" in data
        assert "dependencies" in data
        # Route returns "ok" for healthy dependencies
        assert data["dependencies"]["mongodb"] in ["ok", "connected"]
        assert data["dependencies"]["redis"] == "ok"

def test_health_check_redis_fail(client):
    """Test health check when Redis is down."""
    with patch("app.routes.health.Redis") as mock_redis:
        mock_instance = mock_redis.return_value
        mock_instance.ping.return_value = False
        
        response = client.get("/api/health/")
        
        data = response.json
        assert response.status_code == 503
        assert data["status"] == "degraded"
        assert data["dependencies"]["redis"] == "failed"

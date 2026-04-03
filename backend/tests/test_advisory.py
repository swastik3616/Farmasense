import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.models.documents import Farm, Advisory, AdvisoryReport
from beanie import PydanticObjectId

@pytest.fixture
def mock_token():
    # Return a dummy JWT token for testing
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="dummy_user_id")

def test_advisory_history(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    mock_id = PydanticObjectId()
    
    # Mock Farm.get and Advisory.find as AsyncMocks
    with patch("app.routes.advisory.Farm.get", new_callable=AsyncMock) as mock_farm_get, \
         patch("app.routes.advisory.Advisory.find") as mock_find:
        
        # Setup mock farm
        mock_farm = MagicMock(spec=Farm)
        mock_farm.id = mock_id
        mock_farm_get.return_value = mock_farm
        
        # Setup mock advisory find query
        mock_query = MagicMock()
        mock_advisory = MagicMock(spec=Advisory)
        mock_advisory.id = PydanticObjectId()
        mock_advisory.season = "Kharif"
        mock_advisory.created_at = "mock_date"
        
        # Chain: find(...).sort(...).to_list()
        mock_query.sort.return_value.to_list = AsyncMock(return_value=[mock_advisory])
        mock_find.return_value = mock_query
        
        response = client.get(f"/api/advisory/history/{mock_id}", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert len(data) == 1
        assert data[0]["season"] == "Kharif"

def test_advisory_404_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    # 1. Invalid ObjectId format
    response = client.get(f"/api/advisory/history/invalidobjectidformat", headers=headers)
    assert response.status_code == 400
    assert "error" in response.json
    
    # 2. Farm not found
    with patch("app.routes.advisory.Farm.get", new_callable=AsyncMock) as mock_farm_get:
        mock_farm_get.return_value = None
        
        response = client.post("/api/advisory/generate", json={"farm_id": str(PydanticObjectId())}, headers=headers)
        assert response.status_code == 404
        assert "error" in response.json

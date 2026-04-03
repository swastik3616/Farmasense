import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.models.documents import Farm
from beanie import PydanticObjectId

@pytest.fixture
def mock_token():
    # Return a dummy JWT token for testing
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="dummy_user_id")

def test_create_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    payload = {
        "name": "Green Acres",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "land_size_acres": 10.5,
        "water_source": "Borewell",
        "district": "Bangalore",
        "state": "Karnataka",
        "soil_type": "Red Soil"
    }
    
    with patch("app.models.documents.Farm.insert", new_callable=AsyncMock) as mock_insert:
        mock_insert.return_value = None
        response = client.post("/api/farm/create", json=payload, headers=headers)
        assert response.status_code == 201
        assert response.json["message"] == "Farm created"
        assert "farm_id" in response.json

def test_get_user_farms(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    with patch("app.models.documents.Farm.find") as mock_find:
        mock_query = MagicMock()
        f1 = Farm(user_id="dummy_user_id", name="Farm 1")
        f1.id = PydanticObjectId()
        f2 = Farm(user_id="dummy_user_id", name="Farm 2")
        f2.id = PydanticObjectId()
        
        mock_query.to_list = AsyncMock(return_value=[f1, f2])
        mock_find.return_value = mock_query
        
        response = client.get("/api/farm/", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert len(data) == 2

def test_get_single_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    mock_id = PydanticObjectId()
    
    with patch("app.models.documents.Farm.get", new_callable=AsyncMock) as mock_get:
        mock_farm = Farm(user_id="dummy_user_id", name="Specific Farm", land_size_acres=5.0)
        mock_farm.id = mock_id
        mock_get.return_value = mock_farm
        
        response = client.get(f"/api/farm/{mock_id}", headers=headers)
        assert response.status_code == 200
        assert response.json["name"] == "Specific Farm"

def test_update_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    mock_id = PydanticObjectId()
    
    with patch("app.models.documents.Farm.get", new_callable=AsyncMock) as mock_get, \
         patch("app.models.documents.Farm.save", new_callable=AsyncMock) as mock_save:
        
        mock_farm = Farm(user_id="dummy_user_id", name="Old Name")
        mock_farm.id = mock_id
        mock_get.return_value = mock_farm
        mock_save.return_value = None
        
        payload = {"name": "New Name", "land_size_acres": 20.0}
        response = client.put(f"/api/farm/{mock_id}", json=payload, headers=headers)
        assert response.status_code == 200
        assert response.json["message"] == "Farm updated"

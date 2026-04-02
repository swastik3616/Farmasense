import pytest
from app.models.documents import Farm
from beanie import PydanticObjectId

@pytest.fixture
def mock_token():
    # Return a dummy JWT token for testing
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="dummy_user_id")

@pytest.mark.asyncio
async def test_create_farm(client, mock_token):
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
    
    response = await client.post("/api/farm/create", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Farm created"
    assert "farm_id" in data
    
    # Verify DB insertion
    farm = await Farm.get(PydanticObjectId(data["farm_id"]))
    assert farm is not None
    assert farm.name == "Green Acres"
    assert farm.user_id == "dummy_user_id"

@pytest.mark.asyncio
async def test_get_user_farms(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    # Insert two farms manually
    f1 = Farm(user_id="dummy_user_id", name="Farm 1")
    f2 = Farm(user_id="dummy_user_id", name="Farm 2")
    f3 = Farm(user_id="other_user_id", name="Farm 3") # Should not appear
    await f1.insert()
    await f2.insert()
    await f3.insert()
    
    response = await client.get("/api/farm/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [f["name"] for f in data]
    assert "Farm 1" in names
    assert "Farm 2" in names

@pytest.mark.asyncio
async def test_get_single_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    farm = Farm(user_id="dummy_user_id", name="Specific Farm", land_size_acres=5.0)
    await farm.insert()
    
    response = await client.get(f"/api/farm/{farm.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Specific Farm"
    assert data["land_size_acres"] == 5.0

@pytest.mark.asyncio
async def test_update_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    farm = Farm(user_id="dummy_user_id", name="Old Name")
    await farm.insert()
    
    payload = {"name": "New Name", "land_size_acres": 20.0}
    response = await client.put(f"/api/farm/{farm.id}", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Farm updated"
    
    # Verify update in DB
    updated_farm = await Farm.get(farm.id)
    assert updated_farm.name == "New Name"
    assert updated_farm.land_size_acres == 20.0

import pytest
from app.models.documents import Farm, Advisory, AdvisoryReport
from beanie import PydanticObjectId

@pytest.fixture
def mock_token():
    # Return a dummy JWT token for testing
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="dummy_user_id")

@pytest.mark.asyncio
async def test_advisory_history(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    # 1. Create a mock farm using Beanie
    farm = Farm(user_id="dummy_user_id", name="Test Farm")
    await farm.insert()
    
    # 2. Add an Advisory
    advisory = Advisory(farm_id=str(farm.id), season="Kharif", report_id="dummy_report")
    await advisory.insert()
    
    response = client.get(f"/api/advisory/history/{farm.id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["season"] == "Kharif"

@pytest.mark.asyncio
async def test_advisory_404_farm(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    response = client.get(f"/api/advisory/history/invalidobjectidformat", headers=headers)
    assert response.status_code == 400
    assert "error" in response.get_json()
    
    response = client.post("/api/advisory/generate", json={"farm_id": str(PydanticObjectId())}, headers=headers)
    assert response.status_code == 404
    assert "error" in response.get_json()

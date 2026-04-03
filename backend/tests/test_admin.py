import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.models.documents import Admin, User, Farm, Advisory, Alert
from app.routes.admin import hash_password
from beanie import PydanticObjectId

@pytest.fixture
def admin_token():
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="admin_user_id", additional_claims={"role": "admin"})

def test_admin_setup(client):
    with patch.object(Admin, 'find_one', new_callable=AsyncMock) as mock_find_one, \
         patch.object(Admin, 'insert', new_callable=AsyncMock) as mock_insert:
        # Success case
        mock_find_one.return_value = None
        response = client.post("/api/admin/setup", json={"email": "admin@test.com", "password": "pass"})
        assert response.status_code == 201
        assert response.json["message"] == "Admin created successfully"
        mock_insert.assert_called_once()
        
        # Already exists case
        mock_find_one.return_value = Admin(email="existing@admin.com", password="hash")
        response2 = client.post("/api/admin/setup", json={"email": "admin2@test.com", "password": "pass"})
        assert response2.status_code == 400
        assert "already exists" in response2.json["error"]

def test_admin_login(client):
    with patch.object(Admin, 'find_one', new_callable=AsyncMock) as mock_find_one:
        # Invalid case
        mock_find_one.return_value = None
        response = client.post("/api/admin/login", json={"email": "wrong@admin.com", "password": "pass"})
        assert response.status_code == 401
        
        # Success case
        admin = Admin(email="admin@test.com", password=hash_password("correct_pass"))
        admin.id = PydanticObjectId()
        mock_find_one.return_value = admin
        
        response2 = client.post("/api/admin/login", json={"email": "admin@test.com", "password": "correct_pass"})
        assert response2.status_code == 200
        assert "token" in response2.json

def test_admin_farmers(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    with patch.object(User, 'find_all') as mock_find_all, \
         patch.object(Farm, 'find') as mock_farm_find:
        
        mock_query = MagicMock()
        user1 = User(mobile="123", name="U1")
        user1.id = PydanticObjectId()
        mock_query.sort.return_value.to_list = AsyncMock(return_value=[user1])
        mock_find_all.return_value = mock_query
        
        mock_farm_query = MagicMock()
        mock_farm_query.count = AsyncMock(return_value=2)
        mock_farm_find.return_value = mock_farm_query
        
        response = client.get("/api/admin/farmers", headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["name"] == "U1"

def test_admin_analytics(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    with patch.object(User, 'count', new_callable=AsyncMock) as mock_uc, \
         patch.object(Farm, 'count', new_callable=AsyncMock) as mock_fc, \
         patch.object(Advisory, 'count', new_callable=AsyncMock) as mock_adc, \
         patch.object(Alert, 'count', new_callable=AsyncMock) as mock_alc:
        
        mock_uc.return_value = 10
        mock_fc.return_value = 5
        mock_adc.return_value = 2
        mock_alc.return_value = 0
        
        response = client.get("/api/admin/analytics", headers=headers)
        assert response.status_code == 200
        assert response.json["total_farmers"] == 10
        assert response.json["total_farms"] == 5

def test_admin_advisories(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    with patch.object(Advisory, 'find_all') as mock_find_all:
        mock_query = MagicMock()
        adv = Advisory(farm_id="farm123")
        adv.id = PydanticObjectId()
        mock_query.sort.return_value.limit.return_value.to_list = AsyncMock(return_value=[adv])
        mock_find_all.return_value = mock_query
        
        response = client.get("/api/admin/advisories", headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["farm_id"] == "farm123"

def test_admin_alerts(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    with patch.object(Alert, 'find_all') as mock_find_all:
        mock_query = MagicMock()
        al = Alert(farm_id="farm123", alert_type="weather", severity="high", message="test", sent_via="sms")
        al.id = PydanticObjectId()
        mock_query.sort.return_value.limit.return_value.to_list = AsyncMock(return_value=[al])
        mock_find_all.return_value = mock_query
        
        response = client.get("/api/admin/alerts", headers=headers)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]["alert_type"] == "weather"

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.models.documents import Alert, CommunityReport
from beanie import PydanticObjectId

@pytest.fixture
def mock_token():
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="dummy_user_id")

def test_get_alerts_success(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    farm_id = str(PydanticObjectId())
    
    with patch("app.models.documents.Alert.find") as mock_find:
        mock_query = MagicMock()
        a1 = Alert(farm_id=farm_id, alert_type="Weather", message="Storm coming", severity="high")
        a1.id = PydanticObjectId()
        
        mock_query.sort.return_value.limit.return_value.to_list = AsyncMock(return_value=[a1])
        mock_find.return_value = mock_query
        
        response = client.get(f"/api/alerts/{farm_id}", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert len(data) == 1
        assert data[0]["type"] == "Weather"

def test_create_alert_with_sms(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    farm_id = str(PydanticObjectId())
    payload = {
        "farm_id": farm_id,
        "alert_type": "Pest",
        "message": "Pest outbreak detected",
        "severity": "high",
        "sent_via": "sms"
    }
    
    with patch("app.models.documents.Alert.insert", new_callable=AsyncMock) as mock_insert, \
         patch("app.tasks.communications.dispatch_sms_alert.delay") as mock_sms:
        
        response = client.post("/api/alerts/create", json=payload, headers=headers)
        assert response.status_code == 201
        assert response.json["message"] == "Alert created"
        mock_sms.assert_called_once()

def test_community_report_success(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    payload = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "report_type": "Flood",
        "description": "Severe flooding near the river"
    }
    
    with patch("app.models.documents.CommunityReport.insert", new_callable=AsyncMock) as mock_insert:
        response = client.post("/api/alerts/community/report", json=payload, headers=headers)
        assert response.status_code == 201
        assert response.json["message"] == "Report submitted"

def test_nearby_reports_success(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    
    with patch("app.models.documents.CommunityReport.find") as mock_find:
        mock_query = MagicMock()
        r1 = CommunityReport(user_id="u1", latitude=12.0, longitude=77.0, report_type="Hail", description="Hailstorm", verified=True)
        r1.id = PydanticObjectId()
        
        mock_query.sort.return_value.limit.return_value.to_list = AsyncMock(return_value=[r1])
        mock_find.return_value = mock_query
        
        response = client.get("/api/alerts/community/nearby", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert len(data) == 1
        assert data[0]["report_type"] == "Hail"

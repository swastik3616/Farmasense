import pytest
from unittest.mock import patch, MagicMock, AsyncMock


@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def auth_headers():
    from flask_jwt_extended import create_access_token
    from app import create_app
    app = create_app()
    with app.app_context():
        token = create_access_token(identity="test_user_id")
    return {"Authorization": f"Bearer {token}"}


# ── /advisory/generate ────────────────────────────────────────────────────────

@patch('app.routes.advisory.Farm')
@patch('app.routes.advisory.farm_graph', create=True)
def test_generate_advisory_invalid_farm_id(mock_graph, mock_farm, client):
    headers = auth_headers()
    resp = client.post("/advisory/generate",
                       json={"farm_id": "bad-id", "language": "English"},
                       headers=headers)
    assert resp.status_code == 400
    assert b"Invalid farm ID" in resp.data


@patch('app.routes.advisory.Farm')
def test_generate_advisory_farm_not_found(mock_farm_cls, client):
    mock_farm_cls.get = AsyncMock(return_value=None)
    headers = auth_headers()
    resp = client.post("/advisory/generate",
                       json={"farm_id": "6640a1b2c3d4e5f6a7b8c9d0", "language": "English"},
                       headers=headers)
    assert resp.status_code == 404
    assert b"Farm not found" in resp.data


@patch('app.routes.advisory.Advisory')
@patch('app.routes.advisory.AdvisoryReport')
@patch('app.routes.advisory.validate_advisory_output')
@patch('app.routes.advisory.farm_graph')
@patch('app.routes.advisory.Farm')
def test_generate_advisory_success(mock_farm_cls, mock_graph, mock_validate,
                                    mock_report_cls, mock_advisory_cls, client):
    mock_farm = MagicMock()
    mock_farm.id = "6640a1b2c3d4e5f6a7b8c9d0"
    mock_farm.latitude = 17.0
    mock_farm.longitude = 78.0
    mock_farm.district = "Hyderabad"
    mock_farm.state = "Telangana"
    mock_farm.soil_type = "Clay"
    mock_farm.soil_health_card_no = "123"
    mock_farm.land_size_acres = 5.0
    mock_farm.water_source = "Borewell"
    mock_farm_cls.get = AsyncMock(return_value=mock_farm)

    mock_graph.invoke.return_value = {"advisory_result": {"season": "Kharif", "recommended_crop": "Rice"}}
    mock_validate.return_value = ({"season": "Kharif", "recommended_crop": "Rice"}, [])

    mock_report_instance = MagicMock()
    mock_report_instance.id = "report123"
    mock_report_instance.insert = AsyncMock()
    mock_report_cls.return_value = mock_report_instance

    mock_advisory_instance = MagicMock()
    mock_advisory_instance.id = "advisory123"
    mock_advisory_instance.insert = AsyncMock()
    mock_advisory_cls.return_value = mock_advisory_instance

    headers = auth_headers()
    resp = client.post("/advisory/generate",
                       json={"farm_id": "6640a1b2c3d4e5f6a7b8c9d0", "language": "English"},
                       headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["season"] == "Kharif"


# ── /advisory/history ─────────────────────────────────────────────────────────

def test_advisory_history_invalid_id(client):
    headers = auth_headers()
    resp = client.get("/advisory/history/bad-id", headers=headers)
    assert resp.status_code == 400
    assert b"Invalid farm ID" in resp.data


@patch('app.routes.advisory.Advisory')
def test_advisory_history_success(mock_advisory_cls, client):
    mock_advisory = MagicMock()
    mock_advisory.id = "adv1"
    mock_advisory.season = "Kharif"
    mock_advisory.created_at = "2024-01-01"

    mock_query = MagicMock()
    mock_query.sort.return_value.to_list = AsyncMock(return_value=[mock_advisory])
    mock_advisory_cls.find.return_value = mock_query

    headers = auth_headers()
    resp = client.get("/advisory/history/6640a1b2c3d4e5f6a7b8c9d0", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["season"] == "Kharif"


# ── /advisory/chat ────────────────────────────────────────────────────────────

def test_advisory_chat_missing_farm_id(client):
    headers = auth_headers()
    resp = client.post("/advisory/chat",
                       json={"message": "Should I water?", "language": "English"},
                       headers=headers)
    assert resp.status_code == 400
    assert b"Missing farm_id" in resp.data


@patch('app.routes.advisory.Farm')
def test_advisory_chat_invalid_farm_id(mock_farm_cls, client):
    headers = auth_headers()
    resp = client.post("/advisory/chat",
                       json={"farm_id": "bad-id", "message": "Hello", "language": "English"},
                       headers=headers)
    assert resp.status_code == 400


@patch('app.routes.advisory.farm_graph')
@patch('app.routes.advisory.Farm')
def test_advisory_chat_success(mock_farm_cls, mock_graph, client):
    mock_farm = MagicMock()
    mock_farm.land_size_acres = 5.0
    mock_farm.soil_type = "Clay"
    mock_farm.district = "Hyderabad"
    mock_farm.state = "Telangana"
    mock_farm.water_source = "Borewell"
    mock_farm_cls.get = AsyncMock(return_value=mock_farm)

    mock_graph.invoke.return_value = {"chat_reply": "Water your crops regularly."}

    headers = auth_headers()
    resp = client.post("/advisory/chat",
                       json={
                           "farm_id": "6640a1b2c3d4e5f6a7b8c9d0",
                           "message": "Should I water?",
                           "language": "English",
                           "history": [{"role": "user", "content": "Hello"}]
                       },
                       headers=headers)
    assert resp.status_code == 200
    assert b"Water" in resp.data
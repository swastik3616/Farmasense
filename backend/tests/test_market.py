import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_token():
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="dummy_user_id")

def test_get_prices_success(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    district = "Bangalore"
    
    with patch("app.routes.market.requests.get") as mock_get:
        # Mock weather API response
        mock_res = MagicMock()
        mock_res.json.return_value = {
            "records": [
                {
                    "Modal_x0020_Price": 2500,
                    "Min_x0020_Price": 2200,
                    "Max_x0020_Price": 2800,
                    "Market": "KR Market"
                }
            ]
        }
        mock_get.return_value = mock_res
        
        response = client.get(f"/api/market/prices/{district}?crops=Rice", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert "Rice" in data
        assert data["Rice"]["modal_price"] == 2500
        assert data["Rice"]["market"] == "KR Market"

def test_get_prices_error(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    district = "Bangalore"
    
    with patch("app.routes.market.requests.get", side_effect=Exception("API Down")):
        response = client.get(f"/api/market/prices/{district}?crops=Rice", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert "Rice" in data
        assert "error" in data["Rice"]

def test_predict_price_success(client, mock_token):
    headers = {"Authorization": f"Bearer {mock_token}"}
    response = client.get("/api/market/predict/Wheat/Pune", headers=headers)
    assert response.status_code == 200
    data = response.json
    assert data["crop"] == "Wheat"
    assert data["trend"] == "rising"
    assert data["predicted_30_day"] == 1450

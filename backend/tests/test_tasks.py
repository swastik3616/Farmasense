import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.tasks.weather_monitor import check_weather_and_alert
from app.models.documents import Farm, User, Alert
import asyncio

def test_weather_monitor_severe_rain(app):
    """Test that severe rain triggers an alert and SMS dispatch."""
    
    # 1. Setup mock data
    mock_farm = MagicMock(spec=Farm)
    mock_farm.id = "mock_farm_id"
    mock_farm.name = "Mock Farm"
    mock_farm.latitude = 12.9716
    mock_farm.longitude = 77.5946
    mock_farm.user_id = "mock_user_id"
    
    mock_user = MagicMock(spec=User)
    mock_user.mobile = "+919876543210"
    
    # 2. Mock external dependencies
    with patch("app.tasks.weather_monitor.Farm.find_all") as mock_find_farms, \
         patch("app.tasks.weather_monitor.User.get", new_callable=AsyncMock) as mock_get_user, \
         patch("app.tasks.weather_monitor.requests.get") as mock_requests_get, \
         patch("app.tasks.weather_monitor.Alert.insert", new_callable=AsyncMock) as mock_alert_insert, \
         patch("app.tasks.weather_monitor.dispatch_sms_alert.delay") as mock_sms_delay, \
         patch("app.tasks.weather_monitor.init_beanie", new_callable=AsyncMock) as mock_init_beanie:
        
        # Setup mock behavior
        # find_all().to_list() helper pattern
        mock_query = MagicMock()
        mock_query.to_list = AsyncMock(return_value=[mock_farm])
        mock_find_farms.return_value = mock_query
        
        mock_get_user.return_value = mock_user
        
        # Mock weather API response (Severe Rain: 60mm)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "daily": {
                "precipitation_sum": [60.0],
                "wind_speed_10m_max": [10.0]
            }
        }
        mock_requests_get.return_value = mock_response
        
        # 3. Run the async task logic using asyncio.run
        asyncio.run(check_weather_and_alert())
        
        # 4. Assertions
        mock_alert_insert.assert_called()
        mock_sms_delay.assert_called()
        
        # Verify message content
        args, kwargs = mock_sms_delay.call_args
        assert "Heavy Rain (60.0mm)" in kwargs["body"]
        assert kwargs["phone_number"] == "+919876543210"

def test_weather_monitor_no_severe_weather(app):
    """Test that mild weather does NOT trigger an alert."""
    
    mock_farm = MagicMock(spec=Farm)
    mock_farm.latitude = 12.9716
    mock_farm.longitude = 77.5946
    
    with patch("app.tasks.weather_monitor.Farm.find_all") as mock_find_farms, \
         patch("app.tasks.weather_monitor.requests.get") as mock_requests_get, \
         patch("app.tasks.weather_monitor.Alert.insert", new_callable=AsyncMock) as mock_alert_insert, \
         patch("app.tasks.weather_monitor.init_beanie", new_callable=AsyncMock):
        
        mock_query = MagicMock()
        mock_query.to_list = AsyncMock(return_value=[mock_farm])
        mock_find_farms.return_value = mock_query
        
        # Mock mild weather (5mm rain, 10km/h wind)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "daily": {
                "precipitation_sum": [5.0],
                "wind_speed_10m_max": [10.0]
            }
        }
        mock_requests_get.return_value = mock_response
        
        asyncio.run(check_weather_and_alert())
        
        # No alert should be inserted
        mock_alert_insert.assert_not_called()

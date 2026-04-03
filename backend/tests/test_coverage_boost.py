import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.tasks.communications import send_sms_with_retry, dispatch_sms_alert
from app.tasks.logging_tasks import log_activity
from app.services.dlq_service import log_to_dlq
import asyncio

def test_send_sms_success_mock_mode():
    """Test SMS dispatch when Twilio keys are missing (mock mode)."""
    with patch("os.getenv", side_effect=lambda k, d=None: None):
        sid = send_sms_with_retry("+919876543210", "Test Message")
        assert sid == "mock_sid_123"

def test_log_activity_task():
    """Test background activity logging task."""
    result = log_activity("user_123", "logged_in")
    assert result is True

def test_log_to_dlq_service():
    """Test that DLQ service correctly handles database insertion."""
    with patch("app.services.dlq_service._log_to_dlq_async", new_callable=AsyncMock) as mock_async_log:
        log_to_dlq("+919876543210", "Failed Msg", {"ctx": "val"}, "Test Error")
        mock_async_log.assert_called_once_with("+919876543210", "Failed Msg", {"ctx": "val"}, "Test Error")

def test_dispatch_sms_alert_dlq_fallback():
    """Test that dispatch_sms_alert logs to DLQ on permanent failure."""
    with patch("app.tasks.communications.send_sms_with_retry", side_effect=Exception("Twilio Down")), \
         patch("app.tasks.communications.log_to_dlq") as mock_dlq:
        
        result = dispatch_sms_alert(None, "+919876543210", "Alert Body")
        assert result is None
        mock_dlq.assert_called_once()

def test_send_sms_retry_logic():
    """Test that send_sms_with_retry actually retries on Twilio exceptions."""
    from twilio.base.exceptions import TwilioRestException
    
    # Mock Twilio Client
    with patch("app.tasks.communications.Client") as mock_client_cls, \
         patch("app.tasks.communications.os.getenv", side_effect=lambda k: "secret" if "TWILIO" in k else None):
        
        mock_client = mock_client_cls.return_value
        # Fail twice with TwilioRestException, then succeed
        error = TwilioRestException(500, "http://err", "Twilio Error")
        mock_client.messages.create.side_effect = [error, error, MagicMock(sid="real_sid")]
        
        sid = send_sms_with_retry("+919876543210", "Body")
        assert sid == "real_sid"
        assert mock_client.messages.create.call_count == 3

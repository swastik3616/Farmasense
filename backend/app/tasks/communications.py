import os
from twilio.rest import Client
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.extensions import celery
from app.services.dlq_service import log_to_dlq
from twilio.base.exceptions import TwilioRestException

@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(TwilioRestException),
    reraise=True
)
def send_sms_with_retry(phone_number: str, body: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_raw = os.getenv("TWILIO_PHONE_NUMBER")
    
    if not account_sid or not auth_token:
        # Development / Stub logic
        print(f"[MOCK SMS] To: {phone_number} | Body: {body}")
        return "mock_sid_123"
        
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=from_raw,
        to=phone_number
    )
    return message.sid

@celery.task(bind=True, max_retries=1)
def dispatch_sms_alert(self, phone_number: str, body: str, context_dict: dict = None):
    """
    Celery background worker task.
    Will exponentially retry 3 times under the hood via Tenacity.
    If it completely fails, routes safely to DLQ.
    """
    try:
        sid = send_sms_with_retry(phone_number, body)
        return sid
    except Exception as e:
        log_to_dlq(phone_number, body, context_dict, str(e))
        print(f"[DLQ TRIGGERED] SMS dispatch failed permanently: {e}")
        # Not re-raising here to prevent Celery from retrying infinitely,
        # we have securely trapped it in the Database DLQ queue.
        return None

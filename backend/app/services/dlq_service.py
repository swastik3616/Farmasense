from datetime import datetime
from flask import current_app

def log_to_dlq(phone_number: str, message: str, context: dict, error_reason: str):
    """
    Saves a failed Twilio dispatch into the dlq_sms MongoDB collection
    so that farmers don't silently miss critical alerts.
    """
    try:
        db = current_app.db
        db["dlq_sms"].insert_one({
            "phone_number": phone_number,
            "message": message,
            "context": context,
            "error_reason": str(error_reason),
            "created_at": datetime.utcnow()
        })
    except Exception as db_err:
        print(f"CRITICAL: Failed to write to DLQ in MongoDB: {db_err}")

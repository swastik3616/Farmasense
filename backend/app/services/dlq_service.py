import asyncio
from typing import Optional
from app.models.documents import DLQSms

async def _log_to_dlq_async(phone_number: str, message: str, context: Optional[dict], error_reason: str):
    """
    Async implementation to insert DLQ message using Beanie ODM.
    """
    try:
        dlq_entry = DLQSms(
            phone_number=phone_number,
            message=message,
            context=context or {},
            error_reason=str(error_reason)
        )
        await dlq_entry.insert()
    except Exception as db_err:
        print(f"CRITICAL: Failed to write to DLQ in MongoDB via Beanie: {db_err}")

def log_to_dlq(phone_number: str, message: str, context: Optional[dict], error_reason: str):
    """
    Synchronous wrapper for Celery tasks. 
    It creates a new event loop to safely execute the async Beanie insertion.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(_log_to_dlq_async(phone_number, message, context, error_reason))

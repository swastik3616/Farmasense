from datetime import datetime
from typing import Optional, Any
from pydantic import Field
from beanie import Document, Indexed

class User(Document):
    mobile: str = Indexed(unique=True)
    name: Optional[str] = None
    language: str = "English"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            "mobile",
            "created_at"
        ]

class Admin(Document):
    email: str = Indexed(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "admins"

class Farm(Document):
    user_id: Indexed(str)
    name: str = "My Farm"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    district: Optional[str] = None
    state: Optional[str] = None
    soil_type: Optional[str] = None
    soil_health_card_no: Optional[str] = None
    land_size_acres: Optional[float] = None
    water_source: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "farms"
        indexes = [
            "user_id",
            "created_at",
            [("state", 1), ("district", 1)]
        ]

class Advisory(Document):
    farm_id: Indexed(str)
    season: Optional[str] = None
    report_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "advisories"
        indexes = [
            "farm_id",
            "created_at"
        ]

class AdvisoryReport(Document):
    farm_id: Indexed(str)
    result: dict
    warnings: list = []
    language: str = "English"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "advisory_reports"
        indexes = [
            "farm_id"
        ]

class Alert(Document):
    farm_id: Indexed(str)
    alert_type: str
    message: str
    severity: str = "medium"
    sent_via: str = "sms"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "alerts"
        indexes = [
            "farm_id",
            "created_at"
        ]

class CommunityReport(Document):
    user_id: Indexed(str)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    report_type: str
    description: str
    verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "community_reports"
        indexes = [
            "verified",
            "created_at"
        ]

class DLQSms(Document):
    phone_number: Indexed(str)
    message: str
    context: Optional[dict] = None
    error_reason: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "dlq_sms"
        indexes = [
            "created_at"
        ]

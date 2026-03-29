from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id                  = db.Column(db.Integer, primary_key=True)
    mobile_number       = db.Column(db.String(15), unique=True, nullable=False)
    name                = db.Column(db.String(100))
    language_preference = db.Column(db.String(5), default="en")
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    farms = db.relationship("Farm", backref="owner", lazy=True)


class Farm(db.Model):
    __tablename__ = "farms"
    id                  = db.Column(db.Integer, primary_key=True)
    user_id             = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name                = db.Column(db.String(100))
    latitude            = db.Column(db.Float)
    longitude           = db.Column(db.Float)
    land_size_acres     = db.Column(db.Float)
    water_source        = db.Column(db.String(50))
    soil_health_card_no = db.Column(db.String(50))
    soil_type           = db.Column(db.String(50))
    district            = db.Column(db.String(100))
    state               = db.Column(db.String(100))
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    advisories = db.relationship("Advisory", backref="farm", lazy=True)


class Advisory(db.Model):
    __tablename__ = "advisories"
    id                  = db.Column(db.Integer, primary_key=True)
    farm_id             = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)
    recommended_crop    = db.Column(db.String(100))
    second_option_crop  = db.Column(db.String(100))
    avoid_crop          = db.Column(db.String(100))
    expected_profit_min = db.Column(db.Integer)
    expected_profit_max = db.Column(db.Integer)
    confidence_score    = db.Column(db.Float)
    season              = db.Column(db.String(20))
    mongo_report_id     = db.Column(db.String(50))
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)


class Alert(db.Model):
    __tablename__ = "alerts"
    id          = db.Column(db.Integer, primary_key=True)
    farm_id     = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)
    alert_type  = db.Column(db.String(30))
    message     = db.Column(db.Text)
    severity    = db.Column(db.String(10))
    sent_via    = db.Column(db.String(20))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class CommunityReport(db.Model):
    __tablename__ = "community_reports"
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    latitude    = db.Column(db.Float)
    longitude   = db.Column(db.Float)
    report_type = db.Column(db.String(30))
    description = db.Column(db.Text)
    verified    = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    __tablename__ = "admins"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(100), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
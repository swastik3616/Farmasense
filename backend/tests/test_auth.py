import pytest
import asyncio
from app.models.documents import User
from app.routes.auth import otp_store

def test_send_otp(client):
    """Test that OTP is successfully generated and stored."""
    response = client.post("/api/auth/send-otp", json={
        "mobile_number": "9876543210"
    })
    
    assert response.status_code == 200
    assert response.json() == {"message": "OTP sent successfully"}
    assert "9876543210" in otp_store
    assert len(otp_store["9876543210"]) == 6

def test_verify_otp_creates_user(client):
    """Test verify-otp creates a new user if one doesn't exist."""
    mobile = "1234567890"
    otp_store[mobile] = "112233"
    
    # Wrap Beanie find_one in asyncio.run
    user_exists = asyncio.run(User.find_one(User.mobile == mobile))
    assert user_exists is None
    
    response = client.post("/api/auth/verify-otp", json={
        "mobile_number": mobile,
        "otp": "112233",
        "name": "Test Farmer"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["name"] == "Test Farmer"
    assert "user_id" in data
    
    # Verify User was actually saved to DB
    saved_user = asyncio.run(User.find_one(User.mobile == mobile))
    assert saved_user is not None
    assert str(saved_user.id) == data["user_id"]
    
    # Verify OTP was removed
    assert mobile not in otp_store

def test_verify_otp_invalid(client):
    """Test verify-otp with bad credentials."""
    mobile = "1234567890"
    otp_store[mobile] = "112233"
    
    response = client.post("/api/auth/verify-otp", json={
        "mobile_number": mobile,
        "otp": "wrong",
        "name": "Test Farmer"
    })
    
    assert response.status_code == 401
    assert "error" in response.json()

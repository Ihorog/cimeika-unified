"""
Tests for status endpoint
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment variables before importing app
os.environ['ENVIRONMENT'] = 'test'
os.environ['LOG_LEVEL'] = 'ERROR'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_USER'] = 'test_user'
os.environ['POSTGRES_PASSWORD'] = 'test_pass'

from main import app

# Create test client
client = TestClient(app)


def test_status_endpoint_returns_200():
    """Test that status endpoint returns 200"""
    response = client.get("/api/status")
    assert response.status_code == 200


def test_status_endpoint_has_required_fields():
    """Test that status endpoint returns all required fields"""
    response = client.get("/api/status")
    assert response.status_code == 200
    
    data = response.json()
    
    # Required fields from spec
    required_fields = [
        "active_persona",
        "активні_персони",
        "розгортання",
        "статус",
        "версія",
        "загальна_кількість_взаємодій",
        "uptime",
        "timezone",
        "utc_time",
        "local_time",
        "participant_api",
        "requests_last_5m",
        "errors_last_5m"
    ]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


def test_status_endpoint_timezone_is_kyiv():
    """Test that timezone is Europe/Kyiv"""
    response = client.get("/api/status")
    data = response.json()
    
    assert data["timezone"] == "Europe/Kyiv"


def test_status_endpoint_time_formats():
    """Test that time fields are in correct format"""
    response = client.get("/api/status")
    data = response.json()
    
    # UTC time should be ISO8601 with Z
    assert "utc_time" in data
    assert isinstance(data["utc_time"], str)
    assert "T" in data["utc_time"]  # ISO8601 format
    
    # Local time should be ISO8601 with timezone
    assert "local_time" in data
    assert isinstance(data["local_time"], str)
    assert "T" in data["local_time"]
    
    # Uptime should be HH:MM:SS format
    assert "uptime" in data
    assert isinstance(data["uptime"], str)
    import re
    assert re.match(r'\d{2}:\d{2}:\d{2}', data["uptime"])


def test_status_endpoint_participant_api_structure():
    """Test that participant_api field has correct structure"""
    response = client.get("/api/status")
    data = response.json()
    
    assert "participant_api" in data
    participant_api = data["participant_api"]
    
    assert isinstance(participant_api, dict)
    assert "enabled" in participant_api
    assert participant_api["enabled"] is True
    assert "last_call_at" in participant_api
    # last_call_at can be None or ISO8601 string
    if participant_api["last_call_at"] is not None:
        assert isinstance(participant_api["last_call_at"], str)


def test_status_endpoint_persona_fields():
    """Test persona-related fields"""
    response = client.get("/api/status")
    data = response.json()
    
    assert data["active_persona"] == "ci"
    assert data["активні_персони"] == 5
    assert data["розгортання"] == "HuggingFace / Docker"
    assert data["статус"] == "running"


def test_status_endpoint_version():
    """Test that version is v2.2.1"""
    response = client.get("/api/status")
    data = response.json()
    
    assert data["версія"] == "2.2.1"


def test_status_endpoint_interaction_count():
    """Test that interaction count is an integer"""
    response = client.get("/api/status")
    data = response.json()
    
    assert isinstance(data["загальна_кількість_взаємодій"], int)
    assert data["загальна_кількість_взаємодій"] >= 0


def test_status_endpoint_request_error_counts():
    """Test that request and error counts are integers"""
    response = client.get("/api/status")
    data = response.json()
    
    assert isinstance(data["requests_last_5m"], int)
    assert isinstance(data["errors_last_5m"], int)
    assert data["requests_last_5m"] >= 0
    assert data["errors_last_5m"] >= 0


def test_status_endpoint_performance():
    """Test that status endpoint responds quickly"""
    import time
    
    start_time = time.time()
    response = client.get("/api/status")
    end_time = time.time()
    
    assert response.status_code == 200
    
    # Status check should be fast (< 1 second)
    duration = end_time - start_time
    assert duration < 1.0, f"Status check took too long: {duration}s"

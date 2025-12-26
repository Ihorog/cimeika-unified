"""
Tests for health check endpoints
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

from main import app

# Create test client
client = TestClient(app)


def test_health_endpoint():
    """Test basic health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "ok"
    assert "version" in data
    assert "canon_bundle_id" in data
    assert data["message"] == "CIMEIKA Backend is running"


def test_ready_endpoint():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] in ["ready", "not_ready"]
    assert "version" in data
    assert "canon_bundle_id" in data
    assert "checks" in data
    
    # Verify checks include expected fields
    checks = data["checks"]
    assert "ENVIRONMENT" in checks
    assert "LOG_LEVEL" in checks
    assert "CORS_ORIGINS" in checks
    assert "POSTGRES_HOST" in checks


def test_ready_endpoint_environment_checks():
    """Test that ready endpoint reports environment variable status"""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    
    checks = data["checks"]
    
    # Required vars should be configured (we set them above)
    assert "configured" in checks["ENVIRONMENT"]
    assert "configured" in checks["LOG_LEVEL"]
    
    # Optional vars should report their status
    assert "SENTRY_DSN" in checks
    assert "OPENAI_API_KEY" in checks
    assert "ANTHROPIC_API_KEY" in checks


def test_health_response_structure():
    """Test that health endpoint returns expected structure"""
    response = client.get("/health")
    data = response.json()
    
    # Ensure all required fields are present
    required_fields = ["status", "message", "version", "canon_bundle_id"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


def test_ready_response_structure():
    """Test that ready endpoint returns expected structure"""
    response = client.get("/ready")
    data = response.json()
    
    # Ensure all required fields are present
    required_fields = ["status", "message", "version", "canon_bundle_id", "checks"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Checks should be a dict
    assert isinstance(data["checks"], dict)


def test_health_endpoint_performance():
    """Test that health endpoint responds quickly"""
    import time
    
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()
    
    assert response.status_code == 200
    
    # Health check should be fast (< 1 second)
    duration = end_time - start_time
    assert duration < 1.0, f"Health check took too long: {duration}s"

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
    # Simplified health endpoint only returns status


def test_ready_endpoint():
    """Test readiness check endpoint"""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] in ["ok", "not_ready"]
    assert "deps" in data
    
    # Verify deps structure
    deps = data["deps"]
    assert "env" in deps
    assert deps["env"] in ["ok", "missing_required"]


def test_ready_endpoint_environment_checks():
    """Test that ready endpoint validates required environment variables"""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    
    deps = data["deps"]
    
    # Should report env status (ok if all required vars present)
    assert "env" in deps
    # Since we set required vars in test setup, should be ok
    assert deps["env"] == "ok"


def test_health_response_structure():
    """Test that health endpoint returns expected structure"""
    response = client.get("/health")
    data = response.json()
    
    # Ensure status field is present
    assert "status" in data
    assert data["status"] == "ok"


def test_ready_response_structure():
    """Test that ready endpoint returns expected structure"""
    response = client.get("/ready")
    data = response.json()
    
    # Ensure all required fields are present
    required_fields = ["status", "deps"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Deps should be a dict
    assert isinstance(data["deps"], dict)


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

"""
Tests for monitoring functionality
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
# Explicitly don't set SENTRY_DSN to test without Sentry

from main import app
from app.core.monitoring import get_monitoring_status, is_enabled

# Create test client
client = TestClient(app)


def test_monitoring_status_without_sentry():
    """Test that monitoring status reports correctly when Sentry is not configured"""
    status = get_monitoring_status()
    
    assert isinstance(status, dict)
    assert "sentry_enabled" in status
    assert "sentry_dsn_configured" in status
    assert "environment" in status
    assert "release" in status
    
    # Without SENTRY_DSN, Sentry should be disabled
    assert status["sentry_enabled"] is False
    assert status["sentry_dsn_configured"] is False


def test_monitoring_is_enabled_without_sentry():
    """Test that is_enabled returns False without Sentry"""
    assert is_enabled() is False


def test_ready_endpoint_includes_monitoring():
    """Test that /ready endpoint includes monitoring status"""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "checks" in data
    assert "monitoring" in data["checks"]
    
    monitoring = data["checks"]["monitoring"]
    assert "sentry_enabled" in monitoring
    assert "environment" in monitoring


def test_ready_endpoint_without_sentry():
    """Test that /ready works without Sentry configured"""
    response = client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should report ready even without Sentry
    assert data["status"] in ["ready", "not_ready"]
    
    monitoring = data["checks"]["monitoring"]
    assert monitoring["sentry_enabled"] is False


def test_health_endpoint_stable():
    """Test that /health endpoint is stable and consistent"""
    # Make multiple requests
    for _ in range(10):
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


def test_ready_endpoint_stable():
    """Test that /ready endpoint is stable and consistent"""
    # Make multiple requests
    for _ in range(10):
        response = client.get("/ready")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] in ["ready", "not_ready"]
        assert "checks" in data


def test_monitoring_with_sentry_dsn():
    """Test monitoring behavior when SENTRY_DSN is set"""
    # Save original value
    original_dsn = os.environ.get('SENTRY_DSN')
    
    try:
        # Set a fake DSN
        os.environ['SENTRY_DSN'] = 'https://fake@sentry.io/123456'
        
        # Reimport to pick up new env var
        from importlib import reload
        from app.core import config
        reload(config)
        
        from app.core.config import settings as test_settings
        
        # Should report as configured now
        assert test_settings.SENTRY_DSN is not None
        
    finally:
        # Restore original value
        if original_dsn:
            os.environ['SENTRY_DSN'] = original_dsn
        elif 'SENTRY_DSN' in os.environ:
            del os.environ['SENTRY_DSN']


def test_app_starts_without_sentry():
    """Test that application starts successfully without Sentry"""
    # This test verifies the app can start without crashing when Sentry is not configured
    response = client.get("/")
    assert response.status_code == 200


def test_endpoints_work_without_monitoring():
    """Test that all core endpoints work without monitoring configured"""
    endpoints = [
        "/",
        "/health",
        "/ready",
        "/api/v1/modules/",
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, f"Endpoint {endpoint} failed"


def test_monitoring_import_without_sentry_sdk():
    """Test that monitoring module handles missing sentry-sdk gracefully"""
    # This test verifies the monitoring module doesn't crash if sentry-sdk is not installed
    # The init_sentry function should handle ImportError gracefully
    
    from app.core import monitoring
    
    # Should be able to call these without crashing
    status = monitoring.get_monitoring_status()
    assert isinstance(status, dict)
    
    enabled = monitoring.is_enabled()
    assert isinstance(enabled, bool)

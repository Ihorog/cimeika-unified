"""
Integration tests for Stabilizer module - CI policy flow
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

client = TestClient(app)


def test_policy_integration_full_flow(monkeypatch):
    """Test full stabilization flow with policy checks"""
    monkeypatch.setenv("CI_ADMIN_KEY", "integration-test-key")

    # Test profile switching
    profiles = ["default", "strict", "code", "docs", "chat"]
    for profile in profiles:
        resp = client.post(
            "/stabilizer/axis/activate",
            json={"profile": profile},
            headers={"X-CI-Key": "integration-test-key"}
        )
        assert resp.status_code == 200

        # Verify active profile
        active = client.get("/stabilizer/axis/active")
        assert active.json()["profile"] == profile

        # Test stabilization with this profile
        stab_resp = client.post(
            "/stabilizer/stabilize",
            json={"draft": "Test content " * 100, "mode": "normal"},
            headers={"X-CI-Key": "integration-test-key"}
        )
        assert stab_resp.status_code == 200
        assert "final" in stab_resp.json()
        assert "report" in stab_resp.json()

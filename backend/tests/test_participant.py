"""
Tests for participant API endpoint
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
os.environ['CIMEIKA_PARTICIPANT_KEY'] = 'test_api_key_12345'

from main import app

# Create test client
client = TestClient(app)


def test_participant_message_without_api_key():
    """Test that participant endpoint requires X-API-KEY"""
    response = client.post(
        "/api/participant/message",
        json={
            "conversation_id": "test-123",
            "mode": "analysis",
            "topic": "test failure",
            "input": {
                "text": "npm ci failed with lockfile error",
                "artifacts": [],
                "metadata": {
                    "source": "ci"
                }
            }
        }
    )
    
    assert response.status_code == 422  # FastAPI validation error for missing header


def test_participant_message_with_invalid_api_key():
    """Test that participant endpoint rejects invalid API key"""
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "invalid_key"},
        json={
            "conversation_id": "test-123",
            "mode": "analysis",
            "topic": "test failure",
            "input": {
                "text": "npm ci failed with lockfile error",
                "artifacts": [],
                "metadata": {
                    "source": "ci"
                }
            }
        }
    )
    
    assert response.status_code == 401


def test_participant_message_with_valid_api_key():
    """Test that participant endpoint accepts valid API key and returns protocol fields"""
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "test_api_key_12345"},
        json={
            "conversation_id": "test-123",
            "mode": "analysis",
            "topic": "npm ci failure",
            "input": {
                "text": "npm ci failed with error: npm ERR! lockfile version mismatch",
                "artifacts": [],
                "metadata": {
                    "source": "ci",
                    "repo": "test/repo",
                    "run_id": "12345"
                }
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify protocol fields
    assert data["participant"] == "cimeika-api"
    assert "message" in data
    assert data["severity"] in ["info", "warn", "error"]
    assert "outputs" in data
    assert "patch_unified_diff" in data["outputs"]
    assert "actions" in data["outputs"]
    assert isinstance(data["outputs"]["actions"], list)
    
    # If actions exist, verify structure
    if data["outputs"]["actions"]:
        action = data["outputs"]["actions"][0]
        assert "type" in action
        assert action["type"] in ["suggest", "check", "patch"]
        assert "title" in action
        assert "details" in action


def test_participant_message_recognizes_npm_lockfile_pattern():
    """Test that rule engine recognizes npm lockfile issues"""
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "test_api_key_12345"},
        json={
            "conversation_id": "test-lockfile",
            "mode": "analysis",
            "topic": "lockfile error",
            "input": {
                "text": "npm ERR! lockfile version mismatch. Expected 3, got 2",
                "artifacts": [],
                "metadata": {"source": "ci"}
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should detect npm lockfile issue
    assert "lockfile" in data["message"].lower() or "npm" in data["message"].lower()
    assert len(data["outputs"]["actions"]) > 0


def test_participant_message_recognizes_python_import_error():
    """Test that rule engine recognizes Python import errors"""
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "test_api_key_12345"},
        json={
            "conversation_id": "test-import",
            "mode": "analysis",
            "topic": "import error",
            "input": {
                "text": "ModuleNotFoundError: No module named 'pytest'",
                "artifacts": [],
                "metadata": {"source": "ci"}
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should detect import error
    assert data["severity"] in ["error", "warn"]
    assert len(data["outputs"]["actions"]) > 0


def test_participant_message_unrecognized_pattern():
    """Test that unrecognized patterns return generic message"""
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "test_api_key_12345"},
        json={
            "conversation_id": "test-unknown",
            "mode": "analysis",
            "topic": "unknown error",
            "input": {
                "text": "Some completely random error message that doesn't match any pattern",
                "artifacts": [],
                "metadata": {"source": "ci"}
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return info severity for unrecognized patterns
    assert data["severity"] == "info"
    assert "no recognized" in data["message"].lower() or "review" in data["message"].lower()


def test_participant_message_increments_interaction_counter():
    """Test that successful participant calls increment interaction counter"""
    from app.core.metrics import get_interaction_count
    
    # Get initial count
    initial_count = get_interaction_count()
    
    # Make a successful request
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "test_api_key_12345"},
        json={
            "conversation_id": "test-counter",
            "mode": "analysis",
            "topic": "test",
            "input": {
                "text": "test error",
                "artifacts": [],
                "metadata": {"source": "ci"}
            }
        }
    )
    
    assert response.status_code == 200
    
    # Count should have incremented
    new_count = get_interaction_count()
    assert new_count == initial_count + 1


def test_participant_message_modes():
    """Test different operation modes"""
    modes = ["analysis", "autofix", "logger"]
    
    for mode in modes:
        response = client.post(
            "/api/participant/message",
            headers={"X-API-KEY": "test_api_key_12345"},
            json={
                "conversation_id": f"test-mode-{mode}",
                "mode": mode,
                "topic": "test",
                "input": {
                    "text": "npm ci failed",
                    "artifacts": [],
                    "metadata": {"source": "ci"}
                }
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["participant"] == "cimeika-api"


def test_participant_message_with_artifacts():
    """Test participant endpoint with artifacts"""
    import base64
    
    # Create a simple artifact
    content = "package.json content"
    content_b64 = base64.b64encode(content.encode()).decode()
    
    response = client.post(
        "/api/participant/message",
        headers={"X-API-KEY": "test_api_key_12345"},
        json={
            "conversation_id": "test-artifacts",
            "mode": "autofix",
            "topic": "with artifacts",
            "input": {
                "text": "npm ci failed",
                "artifacts": [
                    {
                        "name": "package.json",
                        "content_base64": content_b64
                    }
                ],
                "metadata": {"source": "ci"}
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["participant"] == "cimeika-api"

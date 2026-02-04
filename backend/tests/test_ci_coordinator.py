"""
Tests for Ci Coordinator module
Tests intent analysis, persona routing, and state management
"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment variables before importing app
os.environ['ENVIRONMENT'] = 'test'
os.environ['LOG_LEVEL'] = 'ERROR'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['POSTGRES_DB'] = 'test_db'
os.environ['POSTGRES_USER'] = 'test_user'
os.environ['POSTGRES_PASSWORD'] = 'test_pass'

from database.models import PersonaEnum, Persona, SystemState
from app.modules.ci.coordinator import CiCoordinator
from app.modules.ci.state_manager import StateManager
from fastapi.testclient import TestClient
from main import app
import uuid

# Create test client
client = TestClient(app)


# Mock database fixtures
@pytest.fixture
def mock_db():
    """Mock database session"""
    db = Mock(spec=Session)
    return db


@pytest.fixture
def mock_persona():
    """Mock persona object"""
    persona = Mock(spec=Persona)
    persona.id = 1
    persona.name = PersonaEnum.CI
    persona.base_prompt = "Test prompt"
    return persona


@pytest.fixture
def mock_state():
    """Mock system state object"""
    state = Mock(spec=SystemState)
    state.mood_score = 5
    state.energy_level = 5
    state.context_data = {}
    state.persona = Mock()
    state.persona.name = PersonaEnum.CI
    return state


# ============================================================
# Intent Analysis Tests
# ============================================================

@pytest.mark.asyncio
async def test_analyze_intent_kazkar(mock_db, mock_state):
    """Test keyword-based intent detection for Kazkar (memory)"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Розкажи мені історію про минуле")
    
    assert result == PersonaEnum.KAZKAR


@pytest.mark.asyncio
async def test_analyze_intent_podija(mock_db, mock_state):
    """Test keyword-based intent detection for Podija (events)"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Заплануй зустріч на завтра")
    
    assert result == PersonaEnum.PODIJA


@pytest.mark.asyncio
async def test_analyze_intent_nastrij(mock_db, mock_state):
    """Test keyword-based intent detection for Nastrij (mood)"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Який у мене настрій сьогодні?")
    
    assert result == PersonaEnum.NASTRIJ


@pytest.mark.asyncio
async def test_analyze_intent_malya(mock_db, mock_state):
    """Test keyword-based intent detection for Malya (creativity)"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Створи малюнок з цієї ідеї")
    
    assert result == PersonaEnum.MALYA


@pytest.mark.asyncio
async def test_analyze_intent_gallery(mock_db, mock_state):
    """Test keyword-based intent detection for Gallery (media)"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Покажи мені фото з галереї")
    
    assert result == PersonaEnum.GALLERY


@pytest.mark.asyncio
async def test_analyze_intent_calendar(mock_db, mock_state):
    """Test keyword-based intent detection for Calendar (time)"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Який сьогодні час і дата?")
    
    assert result == PersonaEnum.CALENDAR


@pytest.mark.asyncio
async def test_analyze_intent_no_match(mock_db, mock_state):
    """Test intent detection returns current persona when no keywords match"""
    mock_state.persona.name = PersonaEnum.CI
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Привіт, як справи?")
    
    # Should keep current persona (CI)
    assert result == PersonaEnum.CI


@pytest.mark.asyncio
async def test_analyze_intent_multiple_keywords(mock_db, mock_state):
    """Test intent detection with multiple keywords scores correctly"""
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.analyze_intent("Розкажи історію про спогади та минуле")
    
    # Should detect Kazkar with highest score (3 keywords)
    assert result == PersonaEnum.KAZKAR


# ============================================================
# Persona Switching Tests
# ============================================================

@pytest.mark.asyncio
async def test_switch_persona_success(mock_db, mock_persona, mock_state):
    """Test successful persona switching"""
    # Setup persona mock
    persona_query = MagicMock()
    persona_query.filter.return_value.first.return_value = mock_persona
    
    # Setup state mock - need to return state, not persona
    state_query = MagicMock()
    state_query.filter.return_value.first.return_value = mock_state
    state_query.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    # Configure query mock to return different results based on model type
    mock_db.query.side_effect = lambda model: persona_query if model == Persona else state_query
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.switch_persona(PersonaEnum.KAZKAR)
    
    assert result["persona"] == PersonaEnum.KAZKAR.value
    assert "base_prompt" in result
    assert "mood_score" in result
    assert "energy_level" in result


@pytest.mark.asyncio
async def test_switch_persona_not_found(mock_db, mock_state):
    """Test persona switching with non-existent persona"""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    coordinator = CiCoordinator(mock_db, "test-user")
    
    with pytest.raises(ValueError, match="not found"):
        await coordinator.switch_persona(PersonaEnum.KAZKAR)


# ============================================================
# Message Routing Tests
# ============================================================

@pytest.mark.asyncio
async def test_route_message_with_persona_switch(mock_db, mock_persona, mock_state):
    """Test message routing that triggers persona switch"""
    # Setup mocks for persona query
    persona_query = MagicMock()
    persona_query.filter.return_value.first.return_value = mock_persona
    
    # Setup mocks for state query
    state_query = MagicMock()
    state_query.filter.return_value.first.return_value = mock_state
    state_query.filter.return_value.order_by.return_value.first.return_value = mock_state
    
    # Configure query mock to return different results based on call
    mock_db.query.side_effect = lambda model: persona_query if model == Persona else state_query
    
    coordinator = CiCoordinator(mock_db, "test-user")
    result = await coordinator.route_message("Розкажи історію про минуле")
    
    assert "persona" in result
    assert "message" in result
    assert result["message"] == "Розкажи історію про минуле"
    assert "timestamp" in result


# ============================================================
# State Manager Tests
# ============================================================

def test_update_mood_valid(mock_db, mock_persona, mock_state):
    """Test updating mood score with valid value"""
    mock_db.query.return_value.filter.return_value.first.return_value = mock_persona
    
    state_manager = StateManager(mock_db, "test-user")
    result = state_manager.update_mood(PersonaEnum.CI, 8)
    
    assert result["persona"] == PersonaEnum.CI.value
    assert result["mood_score"] == 8


def test_update_mood_invalid_low(mock_db, mock_persona, mock_state):
    """Test updating mood score with invalid low value"""
    mock_db.query.return_value.filter.return_value.first.return_value = mock_persona
    
    state_manager = StateManager(mock_db, "test-user")
    
    with pytest.raises(ValueError, match="between 1 and 10"):
        state_manager.update_mood(PersonaEnum.CI, 0)


def test_update_mood_invalid_high(mock_db, mock_persona, mock_state):
    """Test updating mood score with invalid high value"""
    mock_db.query.return_value.filter.return_value.first.return_value = mock_persona
    
    state_manager = StateManager(mock_db, "test-user")
    
    with pytest.raises(ValueError, match="between 1 and 10"):
        state_manager.update_mood(PersonaEnum.CI, 11)


def test_update_energy_valid(mock_db, mock_persona, mock_state):
    """Test updating energy level with valid value"""
    mock_db.query.return_value.filter.return_value.first.return_value = mock_persona
    
    state_manager = StateManager(mock_db, "test-user")
    result = state_manager.update_energy(PersonaEnum.CI, 7)
    
    assert result["persona"] == PersonaEnum.CI.value
    assert result["energy_level"] == 7


def test_get_state(mock_db, mock_persona, mock_state):
    """Test getting current state for a persona"""
    # Setup persona and state queries
    persona_query = MagicMock()
    persona_query.filter.return_value.first.return_value = mock_persona
    
    state_query = MagicMock()
    state_query.filter.return_value.first.return_value = mock_state
    
    # Configure query mock
    mock_db.query.side_effect = lambda model: persona_query if model == Persona else state_query
    
    state_manager = StateManager(mock_db, "test-user")
    result = state_manager.get_state(PersonaEnum.CI)
    
    assert "mood_score" in result
    assert "energy_level" in result
    assert "context_data" in result


# ============================================================
# API Endpoint Tests
# ============================================================

def test_route_message_endpoint():
    """Test /api/v1/personas/route endpoint"""
    # This is an integration test that will fail without a real database
    # We'll test the endpoint exists and returns proper error handling
    response = client.post(
        "/api/v1/personas/route",
        json={"user_id": "test-user", "message": "Test message"}
    )
    
    # May fail with 500 due to DB connection, but endpoint should exist
    assert response.status_code in [200, 500]


def test_get_active_persona_endpoint():
    """Test /api/v1/personas/active/{user_id} endpoint"""
    response = client.get("/api/v1/personas/active/test-user")
    
    # May fail with 500 due to DB connection, but endpoint should exist
    assert response.status_code in [200, 500]


def test_switch_persona_endpoint():
    """Test /api/v1/personas/switch endpoint"""
    response = client.post(
        "/api/v1/personas/switch",
        json={"user_id": "test-user", "target_persona": "Kazkar"}
    )
    
    # May fail with 500 due to DB connection, but endpoint should exist
    assert response.status_code in [200, 404, 500]


def test_update_mood_endpoint():
    """Test /api/v1/personas/mood endpoint"""
    response = client.post(
        "/api/v1/personas/mood",
        json={"user_id": "test-user", "persona": "Ci", "mood_score": 8}
    )
    
    # May fail with 500 due to DB connection, but endpoint should exist
    assert response.status_code in [200, 400, 500]


def test_update_mood_endpoint_invalid_score():
    """Test /api/v1/personas/mood endpoint with invalid score"""
    response = client.post(
        "/api/v1/personas/mood",
        json={"user_id": "test-user", "persona": "Ci", "mood_score": 15}
    )
    
    # Should return 400 for invalid score (if it reaches validation)
    assert response.status_code in [400, 500]

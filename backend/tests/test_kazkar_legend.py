"""
Tests for Kazkar module - Legend functionality (schema validation only)
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.modules.kazkar.schema import KazkarStoryCreate, KazkarStoryUpdate


def test_legend_schema_creation():
    """Test creating a legend schema"""
    legend_data = KazkarStoryCreate(
        title="Легенда про засновника",
        content="Давним-давно жив собі засновник роду...",
        story_type="legend",
        participants=["Іван", "Марія"],
        location="Київ",
        tags=["сім'я", "історія"]
    )
    
    assert legend_data.title == "Легенда про засновника"
    assert legend_data.story_type == "legend"
    assert legend_data.content == "Давним-давно жив собі засновник роду..."
    assert legend_data.participants == ["Іван", "Марія"]
    assert legend_data.location == "Київ"
    assert legend_data.tags == ["сім'я", "історія"]


def test_story_type_validation():
    """Test that story types are validated correctly"""
    valid_types = ['story', 'memory', 'legend', 'fact']
    
    for story_type in valid_types:
        legend_data = KazkarStoryCreate(
            title=f"Test {story_type}",
            content="Test content",
            story_type=story_type
        )
        assert legend_data.story_type == story_type


def test_legend_with_minimal_data():
    """Test creating a legend with only required fields"""
    legend_data = KazkarStoryCreate(
        title="Коротка легенда",
        content="Текст легенди"
    )
    
    assert legend_data.title == "Коротка легенда"
    assert legend_data.content == "Текст легенди"
    assert legend_data.story_type is None  # Optional field


def test_legend_update_schema():
    """Test updating a legend"""
    update_data = KazkarStoryUpdate(
        title="Оновлена назва",
        story_type="legend"
    )
    
    assert update_data.title == "Оновлена назва"
    assert update_data.story_type == "legend"


def test_legend_with_empty_lists():
    """Test creating a legend with empty lists for optional fields"""
    legend_data = KazkarStoryCreate(
        title="Легенда без тегів",
        content="Зміст",
        story_type="legend",
        participants=[],
        tags=[]
    )
    
    assert legend_data.participants == []
    assert legend_data.tags == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

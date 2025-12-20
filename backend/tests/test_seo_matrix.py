"""
Tests for SEO Matrix functionality
"""
import pytest
from pathlib import Path
from app.utils.seo_matrix import SEOMatrix, get_seo_matrix


def test_seo_matrix_loads():
    """Test that SEO matrix loads successfully"""
    seo = get_seo_matrix()
    assert seo is not None
    assert seo._data is not None


def test_get_all_states():
    """Test getting all emotional states"""
    seo = get_seo_matrix()
    states = seo.get_all_states()
    
    assert len(states) == 7
    assert 'fatigue' in states
    assert 'tension' in states
    assert 'anxiety' in states
    assert 'joy' in states
    assert 'loss' in states
    assert 'anticipation' in states
    assert 'change' in states


def test_get_all_intents():
    """Test getting all intents for a state"""
    seo = get_seo_matrix()
    intents = seo.get_all_intents('fatigue')
    
    assert len(intents) == 7
    assert 'understand' in intents
    assert 'capture' in intents
    assert 'calm' in intents
    assert 'check' in intents
    assert 'preserve' in intents
    assert 'connect' in intents
    assert 'prepare' in intents


def test_get_meta():
    """Test getting meta information"""
    seo = get_seo_matrix()
    meta = seo.get_meta('fatigue', 'understand')
    
    assert meta is not None
    assert 'title' in meta
    assert 'description' in meta
    assert meta['title'] == 'Understand your fatigue'
    assert meta['description'] == 'Clarify fatigue. One step, clear result.'


def test_canonical_lang():
    """Test canonical language configuration"""
    seo = get_seo_matrix()
    assert seo.canonical_lang == 'en'


def test_hreflang_patterns():
    """Test hreflang URL patterns"""
    seo = get_seo_matrix()
    patterns = seo.hreflang_patterns
    
    assert 'en' in patterns
    assert 'uk' in patterns
    assert patterns['en'] == '/en/{state}/{intent}'
    assert patterns['uk'] == '/uk/{state}/{intent}'


def test_rules():
    """Test validation rules"""
    seo = get_seo_matrix()
    rules = seo.rules
    
    assert 'title_max' in rules
    assert 'description_max' in rules
    assert rules['title_max'] == 60
    assert rules['description_max'] == 155


def test_get_canonical_url():
    """Test canonical URL generation"""
    seo = get_seo_matrix()
    url = seo.get_canonical_url('fatigue', 'understand')
    
    assert url == '/en/fatigue/understand'


def test_get_canonical_url_with_lang():
    """Test canonical URL generation with specific language"""
    seo = get_seo_matrix()
    
    url_en = seo.get_canonical_url('fatigue', 'understand', lang='en')
    assert url_en == '/en/fatigue/understand'
    
    url_uk = seo.get_canonical_url('fatigue', 'understand', lang='uk')
    assert url_uk == '/uk/fatigue/understand'


def test_get_hreflang_tags():
    """Test hreflang tags generation"""
    seo = get_seo_matrix()
    tags = seo.get_hreflang_tags('fatigue', 'understand')
    
    assert 'en' in tags
    assert 'uk' in tags
    assert tags['en'] == '/en/fatigue/understand'
    assert tags['uk'] == '/uk/fatigue/understand'


def test_validate_meta_valid():
    """Test meta validation with valid data"""
    seo = get_seo_matrix()
    validation = seo.validate_meta('Short title', 'Short description')
    
    assert validation['title']['valid'] is True
    assert validation['description']['valid'] is True


def test_validate_meta_invalid():
    """Test meta validation with invalid data"""
    seo = get_seo_matrix()
    
    long_title = 'a' * 70  # Exceeds 60 char limit
    long_description = 'b' * 200  # Exceeds 155 char limit
    
    validation = seo.validate_meta(long_title, long_description)
    
    assert validation['title']['valid'] is False
    assert validation['description']['valid'] is False
    assert validation['title']['length'] > validation['title']['max']
    assert validation['description']['length'] > validation['description']['max']


def test_get_full_seo_data():
    """Test getting complete SEO data"""
    seo = get_seo_matrix()
    data = seo.get_full_seo_data('fatigue', 'understand')
    
    assert 'meta' in data
    assert 'canonical_url' in data
    assert 'hreflang' in data
    assert 'validation' in data
    
    assert data['meta']['title'] == 'Understand your fatigue'
    assert data['canonical_url'] == '/en/fatigue/understand'
    assert data['validation']['title']['valid'] is True


def test_all_meta_entries_valid():
    """Test that all meta entries pass validation"""
    seo = get_seo_matrix()
    
    failed_entries = []
    
    for state in seo.get_all_states():
        for intent in seo.get_all_intents(state):
            meta = seo.get_meta(state, intent)
            if meta:
                validation = seo.validate_meta(meta['title'], meta['description'])
                
                if not validation['title']['valid'] or not validation['description']['valid']:
                    failed_entries.append(f"{state}/{intent}")
    
    assert len(failed_entries) == 0, f"Failed validation for: {failed_entries}"


def test_singleton_pattern():
    """Test that get_seo_matrix returns the same instance"""
    seo1 = get_seo_matrix()
    seo2 = get_seo_matrix()
    
    assert seo1 is seo2

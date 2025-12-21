"""
Test script for SEO service
Validates all SEO functionality including:
- States and intents
- Entry retrieval (EN + UK)
- Module mapping
- Writes policy
- URL generation
- Routing validation
- Sitemap generation
"""
import sys
sys.path.insert(0, '.')

from app.config.seo import seo_service
import json


def test_basic_getters():
    """Test basic getter methods"""
    print("=" * 60)
    print("TEST: Basic Getters")
    print("=" * 60)
    
    states = seo_service.get_states()
    print(f"✓ States ({len(states)}): {states}")
    assert len(states) == 7, "Should have 7 states"
    
    intents = seo_service.get_intents()
    print(f"✓ Intents ({len(intents)}): {intents}")
    assert len(intents) == 7, "Should have 7 intents"
    
    languages = seo_service.get_languages()
    print(f"✓ Languages ({len(languages)}): {languages}")
    assert len(languages) == 2, "Should have 2 languages"
    
    print("\n✅ All basic getters passed\n")


def test_routing_validation():
    """Test routing validation"""
    print("=" * 60)
    print("TEST: Routing Validation")
    print("=" * 60)
    
    # Valid cases
    assert seo_service.validate_routing('en', 'fatigue', 'understand') == True
    print("✓ Valid: en/fatigue/understand")
    
    assert seo_service.validate_routing('uk', 'loss', 'calm') == True
    print("✓ Valid: uk/loss/calm")
    
    # Invalid cases
    assert seo_service.validate_routing('de', 'fatigue', 'understand') == False
    print("✓ Invalid: de/fatigue/understand (bad language)")
    
    assert seo_service.validate_routing('en', 'happy', 'understand') == False
    print("✓ Invalid: en/happy/understand (bad state)")
    
    assert seo_service.validate_routing('en', 'fatigue', 'discover') == False
    print("✓ Invalid: en/fatigue/discover (bad intent)")
    
    print("\n✅ All routing validation tests passed\n")


def test_url_building():
    """Test URL building"""
    print("=" * 60)
    print("TEST: URL Building")
    print("=" * 60)
    
    url1 = seo_service.build_url('en', 'fatigue', 'understand')
    assert url1 == '/en/fatigue/understand'
    print(f"✓ URL: {url1}")
    
    url2 = seo_service.build_url('uk', 'anticipation', 'prepare')
    assert url2 == '/uk/anticipation/prepare'
    print(f"✓ URL: {url2}")
    
    print("\n✅ All URL building tests passed\n")


def test_module_mapping():
    """Test module mapping"""
    print("=" * 60)
    print("TEST: Module Mapping")
    print("=" * 60)
    
    test_cases = [
        ('fatigue', 'nastrij'),
        ('tension', 'nastrij'),
        ('anxiety', 'nastrij'),
        ('joy', 'nastrij'),
        ('loss', 'kazkar'),
        ('anticipation', 'podija'),
        ('change', 'podija')
    ]
    
    for state, expected_module in test_cases:
        module = seo_service.get_module(state)
        assert module == expected_module, f"State {state} should map to {expected_module}"
        print(f"✓ {state} → {module}")
    
    print("\n✅ All module mapping tests passed\n")


def test_writes_policy():
    """Test writes policy"""
    print("=" * 60)
    print("TEST: Writes Policy")
    print("=" * 60)
    
    # Test with module
    policy = seo_service.get_writes_policy('nastrij')
    assert policy['min'] == 2
    assert policy['max'] == 3
    assert 'calendar.time_point' in policy['mandatory']
    assert policy['optional'] == 'nastrij.state_mark'
    print(f"✓ Nastrij policy: {json.dumps(policy, indent=2)}")
    
    # Test without module
    policy_base = seo_service.get_writes_policy()
    assert 'optional' not in policy_base
    print(f"✓ Base policy (no optional): {json.dumps(policy_base, indent=2)}")
    
    print("\n✅ All writes policy tests passed\n")


def test_entry_retrieval():
    """Test entry retrieval"""
    print("=" * 60)
    print("TEST: Entry Retrieval")
    print("=" * 60)
    
    # Test EN entry
    entry_en = seo_service.get_entry('en', 'fatigue', 'understand')
    assert entry_en is not None
    assert entry_en['title'] == 'Understand your fatigue'
    assert entry_en['module'] == 'nastrij'
    assert entry_en['lang'] == 'en'
    print(f"✓ EN entry: {entry_en['title']}")
    print(f"  Module: {entry_en['module']}")
    print(f"  URL: {entry_en['url']}")
    
    # Test UK entry
    entry_uk = seo_service.get_entry('uk', 'loss', 'calm')
    assert entry_uk is not None
    assert entry_uk['title'] == 'Заспокоїти втрату'
    assert entry_uk['module'] == 'kazkar'
    assert entry_uk['lang'] == 'uk'
    print(f"✓ UK entry: {entry_uk['title']}")
    print(f"  Module: {entry_uk['module']}")
    print(f"  URL: {entry_uk['url']}")
    
    # Test invalid entry
    entry_invalid = seo_service.get_entry('en', 'invalid', 'understand')
    assert entry_invalid is None
    print("✓ Invalid entry returns None")
    
    print("\n✅ All entry retrieval tests passed\n")


def test_all_entries():
    """Test getting all entries for a language"""
    print("=" * 60)
    print("TEST: All Entries Retrieval")
    print("=" * 60)
    
    entries_en = seo_service.get_all_entries('en')
    assert len(entries_en) == 49  # 7 states × 7 intents
    print(f"✓ EN entries: {len(entries_en)} (expected 49)")
    
    entries_uk = seo_service.get_all_entries('uk')
    assert len(entries_uk) == 49
    print(f"✓ UK entries: {len(entries_uk)} (expected 49)")
    
    # Verify each entry has required fields
    for entry in entries_en[:3]:
        assert 'title' in entry
        assert 'description' in entry
        assert 'url' in entry
        assert 'module' in entry
        assert 'writes_policy' in entry
        print(f"✓ Entry structure valid: {entry['state']}/{entry['intent']}")
    
    print("\n✅ All entries retrieval tests passed\n")


def test_sitemap_generation():
    """Test sitemap generation"""
    print("=" * 60)
    print("TEST: Sitemap Generation")
    print("=" * 60)
    
    sitemap = seo_service.generate_sitemap_entries('https://cimeika.com')
    assert len(sitemap) == 49  # 7 states × 7 intents
    print(f"✓ Sitemap entries: {len(sitemap)} (expected 49)")
    
    # Check first entry structure
    first_entry = sitemap[0]
    assert 'loc' in first_entry
    assert 'alternates' in first_entry
    assert len(first_entry['alternates']) == 2  # EN + UK
    print(f"✓ First entry: {first_entry['loc']}")
    print(f"  Alternates: {len(first_entry['alternates'])}")
    
    # Verify hreflang
    for alt in first_entry['alternates']:
        assert 'hreflang' in alt
        assert 'href' in alt
        assert alt['hreflang'] in ['en', 'uk']
        print(f"  - {alt['hreflang']}: {alt['href']}")
    
    print("\n✅ All sitemap generation tests passed\n")


def test_coverage():
    """Test complete coverage of 7×7 matrix"""
    print("=" * 60)
    print("TEST: 7×7 Matrix Coverage")
    print("=" * 60)
    
    states = seo_service.get_states()
    intents = seo_service.get_intents()
    
    total = 0
    missing = []
    
    for state in states:
        for intent in intents:
            entry_en = seo_service.get_entry('en', state, intent)
            entry_uk = seo_service.get_entry('uk', state, intent)
            
            if entry_en and entry_uk:
                total += 1
            else:
                missing.append(f"{state}/{intent}")
    
    print(f"✓ Total coverage: {total}/49")
    
    if missing:
        print(f"✗ Missing entries: {missing}")
        assert False, "Some entries are missing"
    else:
        print("✓ All 49 combinations have EN and UK entries")
    
    print("\n✅ Full 7×7 matrix coverage confirmed\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CIMEIKA SEO SERVICE TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_basic_getters()
        test_routing_validation()
        test_url_building()
        test_module_mapping()
        test_writes_policy()
        test_entry_retrieval()
        test_all_entries()
        test_sitemap_generation()
        test_coverage()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

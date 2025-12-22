"""
Test script for SEO Matrix Service
Tests the new Family Memory & Planning Hub SEO matrix
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.config.seo.seo_matrix_service import SEOMatrixService, get_seo_matrix_service


def test_initialization():
    """Test service initialization"""
    print("=" * 60)
    print("TEST: Service Initialization")
    print("=" * 60)
    
    try:
        service = get_seo_matrix_service()
        print("✓ Service initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Service initialization failed: {e}")
        return False


def test_product_strategy():
    """Test product strategy retrieval"""
    print("\n" + "=" * 60)
    print("TEST: Product Strategy")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    
    print(f"Wedge Market: {service.wedge_market}")
    print(f"Core Promise: {service.core_promise}")
    print(f"Primary CTA: {service.primary_cta}")
    
    assert service.wedge_market == "Family Memory & Planning Hub"
    assert "Фото" in service.core_promise
    print("✓ Product strategy loaded correctly")
    return True


def test_modules():
    """Test module retrieval"""
    print("\n" + "=" * 60)
    print("TEST: Modules")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    modules = service.get_modules()
    
    print(f"Total modules: {len(modules)}")
    assert len(modules) == 7, f"Expected 7 modules, got {len(modules)}"
    
    module_ids = [m['id'] for m in modules]
    expected_ids = ['ci', 'kazkar', 'podija', 'nastrij', 'malya', 'calendar', 'gallery']
    
    for expected_id in expected_ids:
        assert expected_id in module_ids, f"Missing module: {expected_id}"
        print(f"  ✓ {expected_id}")
    
    print("✓ All 7 modules found")
    return True


def test_categories():
    """Test traffic categories"""
    print("\n" + "=" * 60)
    print("TEST: Traffic Categories")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    categories = service.get_traffic_categories()
    
    print(f"Total categories: {len(categories)}")
    assert len(categories) == 7, f"Expected 7 categories, got {len(categories)}"
    
    category_ids = [c['id'] for c in categories]
    expected_ids = ['use_cases', 'how_to', 'templates', 'examples', 'features', 'problems', 'comparisons']
    
    for expected_id in expected_ids:
        assert expected_id in category_ids, f"Missing category: {expected_id}"
        print(f"  ✓ {expected_id}")
    
    print("✓ All 7 categories found")
    return True


def test_patterns():
    """Test 7×7 patterns matrix"""
    print("\n" + "=" * 60)
    print("TEST: Patterns (7×7 Matrix)")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    
    # Test individual pattern
    pattern = service.get_pattern('ci', 'use_cases')
    assert pattern is not None, "Pattern ci/use_cases not found"
    assert pattern['intent'] == 'action hub'
    assert len(pattern['pages']) > 0
    print(f"✓ Pattern ci/use_cases: {pattern['intent']}")
    
    # Test all patterns
    all_patterns = service.get_all_patterns()
    assert len(all_patterns) == 7, f"Expected 7 modules in patterns, got {len(all_patterns)}"
    
    total_patterns = 0
    for module_id, categories in all_patterns.items():
        total_patterns += len(categories)
    
    print(f"✓ Total patterns: {total_patterns} (expected 49)")
    assert total_patterns == 49, f"Expected 49 patterns, got {total_patterns}"
    
    return True


def test_pages():
    """Test page generation"""
    print("\n" + "=" * 60)
    print("TEST: Pages")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    pages = service.get_all_pages()
    
    print(f"Total pages: {len(pages)}")
    
    # Sample a few pages
    sample_pages = pages[:5]
    for page in sample_pages:
        print(f"  ✓ {page['slug']}")
        print(f"    - Module: {page['module']}, Category: {page['category']}")
        print(f"    - EN: {page['url_en']}")
        print(f"    - UA: {page['url_ua']}")
    
    # Test filtering by module
    ci_pages = service.get_all_pages('ci')
    print(f"\n✓ CI module pages: {len(ci_pages)}")
    
    return True


def test_url_generation():
    """Test URL generation"""
    print("\n" + "=" * 60)
    print("TEST: URL Generation")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    
    # Test basic URL
    url = service.build_url('en', 'ci', 'use_cases')
    assert url == '/en/ci/use_cases'
    print(f"✓ Basic URL: {url}")
    
    # Test URL with page path
    url_with_path = service.build_url('ua', 'kazkar', 'examples', 'kazkar/examples/wedding')
    assert url_with_path == '/ua/kazkar/examples/wedding'
    print(f"✓ URL with path: {url_with_path}")
    
    # Test validation
    assert service.validate_routing('en', 'ci', 'use_cases') == True
    assert service.validate_routing('invalid', 'ci', 'use_cases') == False
    print("✓ URL validation works")
    
    return True


def test_sitemap():
    """Test sitemap generation"""
    print("\n" + "=" * 60)
    print("TEST: Sitemap Generation")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    
    # Test sitemap entries
    entries = service.generate_sitemap_entries('https://cimeika.com')
    print(f"✓ Sitemap entries: {len(entries)}")
    
    # Sample entry
    if entries:
        sample = entries[0]
        print(f"  Sample entry:")
        print(f"    - loc: {sample['loc']}")
        print(f"    - alternates: {len(sample['alternates'])}")
    
    # Test XML generation
    xml = service.generate_sitemap_xml('https://cimeika.com')
    assert '<?xml version="1.0"' in xml
    assert 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' in xml
    print("✓ Sitemap XML generated")
    
    return True


def test_robots_txt():
    """Test robots.txt generation"""
    print("\n" + "=" * 60)
    print("TEST: Robots.txt Generation")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    robots = service.generate_robots_txt('https://cimeika.com/sitemap.xml')
    
    assert 'User-agent: *' in robots
    assert 'Allow: /' in robots
    assert 'Sitemap:' in robots
    print("✓ robots.txt generated")
    print(robots)
    
    return True


def test_meta_tags():
    """Test meta tags generation"""
    print("\n" + "=" * 60)
    print("TEST: Meta Tags Generation")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    tags = service.generate_meta_tags(
        title="Family Stories - Kazkar",
        description="Capture and share your family stories",
        url="https://cimeika.com/en/kazkar/family-stories",
        image="https://cimeika.com/og-image.jpg",
        lang="en"
    )
    
    assert tags['title'] == "Family Stories - Kazkar"
    assert tags['canonical'] == "https://cimeika.com/en/kazkar/family-stories"
    assert 'og:title' in tags
    assert 'twitter:card' in tags
    
    print("✓ Meta tags generated:")
    for key, value in tags.items():
        print(f"  - {key}: {value}")
    
    return True


def test_status_and_strategy():
    """Test status and execution strategy"""
    print("\n" + "=" * 60)
    print("TEST: Status and Execution Strategy")
    print("=" * 60)
    
    service = get_seo_matrix_service()
    
    status = service.status
    print("Implementation Status:")
    for key, value in status.items():
        print(f"  - {key}: {value}")
    
    priority = service.get_priority_order()
    print(f"\n✓ Priority items: {len(priority)}")
    for item in priority:
        print(f"  - {item}")
    
    gates = service.get_gates()
    print(f"\n✓ Gates defined: {len(gates)}")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("SEO MATRIX SERVICE TEST SUITE")
    print("Family Memory & Planning Hub")
    print("=" * 60)
    
    tests = [
        ("Initialization", test_initialization),
        ("Product Strategy", test_product_strategy),
        ("Modules", test_modules),
        ("Categories", test_categories),
        ("Patterns", test_patterns),
        ("Pages", test_pages),
        ("URL Generation", test_url_generation),
        ("Sitemap", test_sitemap),
        ("Robots.txt", test_robots_txt),
        ("Meta Tags", test_meta_tags),
        ("Status & Strategy", test_status_and_strategy),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n✗ {name} FAILED")
        except Exception as e:
            failed += 1
            print(f"\n✗ {name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return True
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

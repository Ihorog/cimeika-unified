"""
SEO Matrix Service for Family Memory & Planning Hub
Manages SEO for 7 modules × 7 traffic categories = 49 patterns
"""
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path


class SEOMatrixService:
    """
    SEO Matrix Service for Cimeika Family Memory & Planning Hub
    Provides access to:
    - 7 modules (Ci, Kazkar, Podija, Nastrij, Malya, Calendar, Gallery)
    - 7 traffic categories (use_cases, how_to, templates, examples, features, problems, comparisons)
    - 49 content patterns (7×7)
    - Bilingual support (en/ua)
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SEO Matrix Service
        
        Args:
            config_path: Path to cimeika_seo_matrix.yaml. If None, uses default location.
        """
        if config_path is None:
            # Try multiple possible locations
            possible_paths = [
                Path(__file__).parent.parent / "cimeika_seo_matrix.yaml",
                Path(__file__).parent.parent.parent.parent.parent / ".governance" / "seo" / "cimeika_seo_matrix.yaml",
            ]
            
            for path in possible_paths:
                if path.exists():
                    config_path = path
                    break
            
            if config_path is None:
                config_path = possible_paths[0]  # Use first as default
        
        self.config_path = Path(config_path)
        self._data: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load SEO matrix configuration from YAML"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"SEO matrix file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._data = yaml.safe_load(f)
    
    # ===== Product Strategy =====
    
    @property
    def product_strategy(self) -> Dict[str, Any]:
        """Get product strategy configuration"""
        return self._data.get('product_strategy', {})
    
    @property
    def wedge_market(self) -> str:
        """Get wedge market positioning"""
        return self.product_strategy.get('wedge_market', '')
    
    @property
    def core_promise(self) -> str:
        """Get core promise"""
        return self.product_strategy.get('core_promise', '')
    
    @property
    def primary_cta(self) -> str:
        """Get primary call-to-action"""
        return self.product_strategy.get('primary_cta', '')
    
    # ===== Network Matrix =====
    
    def get_modules(self) -> List[Dict[str, str]]:
        """Get all modules with their metadata"""
        return self._data.get('network_matrix', {}).get('modules', [])
    
    def get_module(self, module_id: str) -> Optional[Dict[str, str]]:
        """
        Get module metadata by ID
        
        Args:
            module_id: Module identifier (ci, kazkar, podija, etc.)
            
        Returns:
            Module metadata or None if not found
        """
        for module in self.get_modules():
            if module.get('id') == module_id:
                return module
        return None
    
    def get_traffic_categories(self) -> List[Dict[str, str]]:
        """Get all traffic categories"""
        return self._data.get('network_matrix', {}).get('traffic_categories', [])
    
    def get_category(self, category_id: str) -> Optional[Dict[str, str]]:
        """
        Get traffic category by ID
        
        Args:
            category_id: Category identifier
            
        Returns:
            Category metadata or None if not found
        """
        for category in self.get_traffic_categories():
            if category.get('id') == category_id:
                return category
        return None
    
    # ===== Patterns (7×7 Matrix) =====
    
    def get_pattern(self, module_id: str, category_id: str) -> Optional[Dict[str, Any]]:
        """
        Get pattern for specific module and category
        
        Args:
            module_id: Module identifier
            category_id: Category identifier
            
        Returns:
            Pattern data with intent and pages, or None if not found
        """
        patterns = self._data.get('patterns_49', {})
        module_patterns = patterns.get(module_id, {})
        return module_patterns.get(category_id)
    
    def get_all_patterns(self, module_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Get all patterns, optionally filtered by module
        
        Args:
            module_id: Optional module filter
            
        Returns:
            Dictionary of patterns
        """
        patterns = self._data.get('patterns_49', {})
        
        if module_id:
            return {module_id: patterns.get(module_id, {})}
        
        return patterns
    
    def get_all_pages(self, module_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of all pages, optionally filtered by module
        
        Args:
            module_id: Optional module filter
            
        Returns:
            List of page dictionaries with module, category, intent, and slug
        """
        pages = []
        patterns = self.get_all_patterns(module_id)
        
        for mod_id, categories in patterns.items():
            for cat_id, pattern in categories.items():
                if pattern and 'pages' in pattern:
                    for page_slug in pattern['pages']:
                        pages.append({
                            'module': mod_id,
                            'category': cat_id,
                            'intent': pattern.get('intent', ''),
                            'slug': page_slug,
                            'url_en': f'/en/{page_slug}',
                            'url_ua': f'/ua/{page_slug}'
                        })
        
        return pages
    
    # ===== URL Generation =====
    
    def build_url(self, lang: str, module_id: str, category_id: str, page_path: Optional[str] = None) -> str:
        """
        Build SEO-friendly URL
        
        Args:
            lang: Language code (en/ua)
            module_id: Module identifier
            category_id: Category identifier
            page_path: Optional specific page path
            
        Returns:
            URL path string
        """
        if page_path:
            return f"/{lang}/{page_path}"
        
        return f"/{lang}/{module_id}/{category_id}"
    
    def validate_routing(self, lang: str, module_id: str, category_id: str) -> bool:
        """
        Validate routing parameters
        
        Args:
            lang: Language code
            module_id: Module identifier
            category_id: Category identifier
            
        Returns:
            True if valid, False otherwise
        """
        valid_langs = ['en', 'ua']
        valid_modules = [m['id'] for m in self.get_modules()]
        valid_categories = [c['id'] for c in self.get_traffic_categories()]
        
        return (
            lang in valid_langs and
            module_id in valid_modules and
            category_id in valid_categories
        )
    
    # ===== Sitemap Generation =====
    
    def generate_sitemap_entries(self, base_url: str = "") -> List[Dict[str, Any]]:
        """
        Generate sitemap entries for all pages
        
        Args:
            base_url: Base URL for the site
            
        Returns:
            List of sitemap entries with URLs and hreflang alternates
        """
        entries = []
        pages = self.get_all_pages()
        
        # Group pages by slug for hreflang alternates
        pages_by_slug = {}
        for page in pages:
            slug = page['slug']
            if slug not in pages_by_slug:
                pages_by_slug[slug] = []
            pages_by_slug[slug].append(page)
        
        # Create sitemap entries
        seen_slugs = set()
        for page in pages:
            slug = page['slug']
            
            # Only create one entry per slug (avoid duplicates)
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            
            entry = {
                'loc': base_url + page['url_en'],
                'alternates': [
                    {'hreflang': 'en', 'href': base_url + page['url_en']},
                    {'hreflang': 'uk', 'href': base_url + page['url_ua']},
                ]
            }
            entries.append(entry)
        
        return entries
    
    def generate_sitemap_xml(self, base_url: str = "https://cimeika.com") -> str:
        """
        Generate complete sitemap XML
        
        Args:
            base_url: Base URL for the site
            
        Returns:
            Sitemap XML string
        """
        entries = self.generate_sitemap_entries(base_url)
        
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        ]
        
        for entry in entries:
            xml_lines.append('  <url>')
            xml_lines.append(f'    <loc>{entry["loc"]}</loc>')
            
            for alt in entry['alternates']:
                xml_lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{alt["hreflang"]}" '
                    f'href="{alt["href"]}" />'
                )
            
            xml_lines.append('  </url>')
        
        xml_lines.append('</urlset>')
        
        return '\n'.join(xml_lines)
    
    # ===== Robots.txt =====
    
    def generate_robots_txt(self, sitemap_url: str = "https://cimeika.com/sitemap.xml") -> str:
        """
        Generate robots.txt content
        
        Args:
            sitemap_url: URL to sitemap
            
        Returns:
            robots.txt content
        """
        return f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""
    
    # ===== Meta Tags =====
    
    def generate_meta_tags(
        self,
        title: str,
        description: str,
        url: str,
        image: Optional[str] = None,
        lang: str = 'en'
    ) -> Dict[str, str]:
        """
        Generate meta tags for a page
        
        Args:
            title: Page title
            description: Page description
            url: Canonical URL
            image: Optional Open Graph image URL
            lang: Language code
            
        Returns:
            Dictionary of meta tags
        """
        tags = {
            'title': title,
            'description': description,
            'canonical': url,
            'og:title': title,
            'og:description': description,
            'og:url': url,
            'og:type': 'website',
            'twitter:card': 'summary_large_image',
            'twitter:title': title,
            'twitter:description': description,
        }
        
        if image:
            tags['og:image'] = image
            tags['twitter:image'] = image
        
        return tags
    
    # ===== Status & Execution =====
    
    @property
    def status(self) -> Dict[str, Any]:
        """Get implementation status"""
        return self._data.get('status', {})
    
    @property
    def execution_strategy(self) -> Dict[str, Any]:
        """Get execution strategy"""
        return self._data.get('execution_strategy_next', {})
    
    def get_priority_order(self) -> List[str]:
        """Get priority order for implementation"""
        return self.execution_strategy.get('priority_order', [])
    
    def get_gates(self) -> Dict[str, List[str]]:
        """Get go-to-stage-2 gates"""
        return self.execution_strategy.get('gates', {})


# Global instance
_seo_matrix_service_instance: Optional[SEOMatrixService] = None


def get_seo_matrix_service() -> SEOMatrixService:
    """Get or create global SEO Matrix Service instance"""
    global _seo_matrix_service_instance
    if _seo_matrix_service_instance is None:
        _seo_matrix_service_instance = SEOMatrixService()
    return _seo_matrix_service_instance

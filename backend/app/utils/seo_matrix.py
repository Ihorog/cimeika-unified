"""
SEO Matrix Loader
Loads and provides access to SEO metadata from cimeika_seo_matrix.yaml
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class SEOMatrix:
    """
    Manages SEO metadata for different emotional states and intents.
    Provides canonical URLs, hreflang tags, and meta information.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SEO Matrix
        
        Args:
            config_path: Path to YAML config file. If None, uses default location.
        """
        if config_path is None:
            # Default to config directory
            config_dir = Path(__file__).parent.parent / "config"
            config_path = config_dir / "cimeika_seo_matrix.yaml"
        
        self.config_path = Path(config_path)
        self._data: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load SEO matrix from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"SEO matrix file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._data = yaml.safe_load(f)
    
    @property
    def seo_config(self) -> Dict[str, Any]:
        """Get SEO configuration"""
        return self._data.get('seo', {})
    
    @property
    def canonical_lang(self) -> str:
        """Get canonical language"""
        return self.seo_config.get('canonical_lang', 'en')
    
    @property
    def hreflang_patterns(self) -> Dict[str, str]:
        """Get hreflang URL patterns"""
        return self.seo_config.get('hreflang', {})
    
    @property
    def rules(self) -> Dict[str, int]:
        """Get SEO validation rules"""
        return self.seo_config.get('rules', {})
    
    def get_meta(self, state: str, intent: str) -> Optional[Dict[str, str]]:
        """
        Get meta information for a specific state and intent
        
        Args:
            state: Emotional state (e.g., 'fatigue', 'tension')
            intent: User intent (e.g., 'understand', 'capture')
        
        Returns:
            Dictionary with 'title' and 'description' keys, or None if not found
        """
        meta_entries = self._data.get('meta_entries', {})
        state_data = meta_entries.get(state, {})
        return state_data.get(intent)
    
    def get_canonical_url(self, state: str, intent: str, lang: Optional[str] = None) -> str:
        """
        Generate canonical URL for given state and intent
        
        Args:
            state: Emotional state
            intent: User intent
            lang: Language code (uses canonical_lang if not specified)
        
        Returns:
            Canonical URL path
        """
        if lang is None:
            lang = self.canonical_lang
        
        pattern = self.hreflang_patterns.get(lang, self.hreflang_patterns.get('en'))
        return pattern.format(state=state, intent=intent)
    
    def get_hreflang_tags(self, state: str, intent: str) -> Dict[str, str]:
        """
        Generate hreflang tags for all languages
        
        Args:
            state: Emotional state
            intent: User intent
        
        Returns:
            Dictionary mapping language codes to URLs
        """
        return {
            lang: pattern.format(state=state, intent=intent)
            for lang, pattern in self.hreflang_patterns.items()
        }
    
    def validate_meta(self, title: str, description: str) -> Dict[str, Any]:
        """
        Validate meta title and description against rules
        
        Args:
            title: Meta title to validate
            description: Meta description to validate
        
        Returns:
            Dictionary with validation results
        """
        title_max = self.rules.get('title_max', 60)
        description_max = self.rules.get('description_max', 155)
        
        return {
            'title': {
                'value': title,
                'length': len(title),
                'max': title_max,
                'valid': len(title) <= title_max
            },
            'description': {
                'value': description,
                'length': len(description),
                'max': description_max,
                'valid': len(description) <= description_max
            }
        }
    
    def get_all_states(self) -> list:
        """Get list of all available emotional states"""
        return list(self._data.get('meta_entries', {}).keys())
    
    def get_all_intents(self, state: str) -> list:
        """
        Get list of all available intents for a given state
        
        Args:
            state: Emotional state
        
        Returns:
            List of intent names
        """
        meta_entries = self._data.get('meta_entries', {})
        state_data = meta_entries.get(state, {})
        return list(state_data.keys())
    
    def get_full_seo_data(self, state: str, intent: str) -> Dict[str, Any]:
        """
        Get complete SEO data for a state/intent combination
        
        Args:
            state: Emotional state
            intent: User intent
        
        Returns:
            Dictionary with all SEO information
        """
        meta = self.get_meta(state, intent)
        if not meta:
            return {}
        
        return {
            'meta': meta,
            'canonical_url': self.get_canonical_url(state, intent),
            'hreflang': self.get_hreflang_tags(state, intent),
            'validation': self.validate_meta(meta.get('title', ''), meta.get('description', ''))
        }


# Global instance
_seo_matrix_instance: Optional[SEOMatrix] = None


def get_seo_matrix() -> SEOMatrix:
    """Get or create global SEO Matrix instance"""
    global _seo_matrix_instance
    if _seo_matrix_instance is None:
        _seo_matrix_instance = SEOMatrix()
    return _seo_matrix_instance

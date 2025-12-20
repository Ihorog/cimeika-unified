"""
SEO Module for Cimeika Unified
Provides SEO entry resolution, URL building, module mapping, and writes policy
"""
import os
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path


class SEOService:
    """
    SEO Service for Cimeika
    Centralizes SEO matrix, routing, module mapping, and writes policy
    """
    
    # Canonical states and intents
    STATES = ["fatigue", "tension", "anxiety", "joy", "loss", "anticipation", "change"]
    INTENTS = ["understand", "capture", "calm", "check", "preserve", "connect", "prepare"]
    LANGUAGES = ["en", "uk"]
    
    # Module mapping
    MODULE_MAPPING = {
        "fatigue": "nastrij",
        "tension": "nastrij",
        "anxiety": "nastrij",
        "joy": "nastrij",
        "loss": "kazkar",
        "anticipation": "podija",
        "change": "podija"
    }
    
    # Writes policy
    WRITES_POLICY = {
        "min": 2,
        "max": 3,
        "mandatory": [
            "calendar.time_point",
            "gallery.experience_snapshot"
        ],
        "optional_by_module": {
            "nastrij": "nastrij.state_mark",
            "kazkar": "kazkar.memory_node",
            "podija": "podija.future_link"
        }
    }
    
    def __init__(self):
        """Initialize SEO service and load matrix data"""
        self._matrix_data = None
        self._seeds_data = None
        self._load_config()
    
    def _load_config(self):
        """Load SEO configuration from YAML files"""
        config_dir = Path(__file__).parent
        
        # Load SEO matrix
        matrix_path = config_dir / "cimeikaseomatrix.yaml"
        if matrix_path.exists():
            with open(matrix_path, 'r', encoding='utf-8') as f:
                self._matrix_data = yaml.safe_load(f)
        
        # Load research seeds
        seeds_path = config_dir / "seoresearchseeds.yaml"
        if seeds_path.exists():
            with open(seeds_path, 'r', encoding='utf-8') as f:
                self._seeds_data = yaml.safe_load(f)
    
    def get_states(self) -> List[str]:
        """Get list of canonical states"""
        return self.STATES.copy()
    
    def get_intents(self) -> List[str]:
        """Get list of canonical intents"""
        return self.INTENTS.copy()
    
    def get_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.LANGUAGES.copy()
    
    def validate_routing(self, lang: str, state: str, intent: str) -> bool:
        """
        Validate routing parameters
        
        Args:
            lang: Language code (en, uk)
            state: Emotional state
            intent: User intent
            
        Returns:
            bool: True if valid, False otherwise
        """
        return (
            lang in self.LANGUAGES and
            state in self.STATES and
            intent in self.INTENTS
        )
    
    def build_url(self, lang: str, state: str, intent: str) -> str:
        """
        Build SEO-friendly URL
        
        Args:
            lang: Language code
            state: Emotional state
            intent: User intent
            
        Returns:
            str: Formatted URL path
        """
        return f"/{lang}/{state}/{intent}"
    
    def get_module(self, state: str) -> Optional[str]:
        """
        Get module name for a given state
        
        Args:
            state: Emotional state
            
        Returns:
            str: Module name or None if not found
        """
        return self.MODULE_MAPPING.get(state)
    
    def get_writes_policy(self, module: Optional[str] = None) -> Dict[str, Any]:
        """
        Get writes policy, optionally including module-specific policy
        
        Args:
            module: Optional module name to include specific policy
            
        Returns:
            Dict: Writes policy configuration
        """
        policy = {
            "min": self.WRITES_POLICY["min"],
            "max": self.WRITES_POLICY["max"],
            "mandatory": self.WRITES_POLICY["mandatory"].copy()
        }
        
        if module and module in self.WRITES_POLICY["optional_by_module"]:
            policy["optional"] = self.WRITES_POLICY["optional_by_module"][module]
        
        return policy
    
    def get_entry(self, lang: str, state: str, intent: str) -> Optional[Dict[str, Any]]:
        """
        Get complete SEO entry for given parameters
        
        Args:
            lang: Language code (en, uk)
            state: Emotional state
            intent: User intent
            
        Returns:
            Dict containing title, description, url, module, writes_policy
            or None if not found
        """
        # Validate routing
        if not self.validate_routing(lang, state, intent):
            return None
        
        # Find entry in matrix
        entry_data = self._find_matrix_entry(state, intent, lang)
        if not entry_data:
            return None
        
        # Get module and writes policy
        module = self.get_module(state)
        writes_policy = self.get_writes_policy(module)
        
        # Build complete entry
        return {
            "title": entry_data.get("title", ""),
            "description": entry_data.get("description", ""),
            "url": self.build_url(lang, state, intent),
            "module": module,
            "writes_policy": writes_policy,
            "state": state,
            "intent": intent,
            "lang": lang
        }
    
    def _find_matrix_entry(self, state: str, intent: str, lang: str) -> Optional[Dict[str, str]]:
        """
        Find entry in matrix data
        
        Args:
            state: Emotional state
            intent: User intent
            lang: Language code
            
        Returns:
            Dict with title and description or None
        """
        if not self._matrix_data or "matrix" not in self._matrix_data:
            return None
        
        for entry in self._matrix_data["matrix"]:
            if entry.get("state") == state and entry.get("intent") == intent:
                if lang in entry:
                    return entry[lang]
        
        return None
    
    def get_all_entries(self, lang: str) -> List[Dict[str, Any]]:
        """
        Get all SEO entries for a given language
        
        Args:
            lang: Language code
            
        Returns:
            List of all SEO entries
        """
        entries = []
        
        for state in self.STATES:
            for intent in self.INTENTS:
                entry = self.get_entry(lang, state, intent)
                if entry:
                    entries.append(entry)
        
        return entries
    
    def get_seeds(self, lang: Optional[str] = None) -> Dict[str, Any]:
        """
        Get semantic research seeds
        
        Args:
            lang: Optional language filter
            
        Returns:
            Dict containing seeds data
        """
        if not self._seeds_data:
            return {}
        
        if lang:
            # Filter by language if specified
            result = {}
            if "intent_generic" in self._seeds_data and lang in self._seeds_data["intent_generic"]:
                result["intent_generic"] = self._seeds_data["intent_generic"][lang]
            if "state_specific" in self._seeds_data:
                result["state_specific"] = {}
                for state, data in self._seeds_data["state_specific"].items():
                    if lang in data:
                        result["state_specific"][state] = data[lang]
            return result
        
        return self._seeds_data
    
    def generate_sitemap_entries(self, base_url: str = "") -> List[Dict[str, str]]:
        """
        Generate sitemap entries for all language/state/intent combinations
        
        Args:
            base_url: Base URL for the site (optional)
            
        Returns:
            List of sitemap entries with url and alternate URLs
        """
        entries = []
        
        for state in self.STATES:
            for intent in self.INTENTS:
                # Generate entry for each language
                urls = {}
                for lang in self.LANGUAGES:
                    urls[lang] = base_url + self.build_url(lang, state, intent)
                
                # Create entry with hreflang alternates
                entry = {
                    "loc": urls["en"],  # Primary URL (canonical)
                    "alternates": [
                        {"hreflang": lang, "href": url}
                        for lang, url in urls.items()
                    ]
                }
                entries.append(entry)
        
        return entries


# Global instance
seo_service = SEOService()

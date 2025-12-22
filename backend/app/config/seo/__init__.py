"""SEO module package initialization"""
from .seo_service import SEOService, seo_service
from .seo_matrix_service import SEOMatrixService, get_seo_matrix_service

__all__ = [
    "SEOService",
    "seo_service",
    "SEOMatrixService",
    "get_seo_matrix_service"
]

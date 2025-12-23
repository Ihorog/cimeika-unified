"""
Module initialization and registration for backend
Central setup for all Cimeika modules
"""
from app.core import registry
from app.modules.ci.service import CiService
from app.modules.kazkar.service import KazkarService
from app.modules.podija.service import PodijaService
from app.modules.nastrij.service import NastrijService
from app.modules.malya.service import MalyaService
from app.modules.gallery.service import GalleryService
from app.modules.calendar.service import CalendarService


# Global service instances
ci_service = CiService()
kazkar_service = KazkarService()
podija_service = PodijaService()
nastrij_service = NastrijService()
malya_service = MalyaService()
gallery_service = GalleryService()
calendar_service = CalendarService()


def register_modules():
    """
    Register all modules with the orchestrator
    """
    registry.register('ci', ci_service)
    registry.register('kazkar', kazkar_service)
    registry.register('podija', podija_service)
    registry.register('nastrij', nastrij_service)
    registry.register('malya', malya_service)
    registry.register('gallery', gallery_service)
    registry.register('calendar', calendar_service)


def initialize_modules():
    """
    Initialize all registered modules
    
    Returns:
        Dict mapping module names to initialization success
    """
    return registry.initialize_all()


def get_modules_status():
    """
    Get status of all modules
    
    Returns:
        Dict mapping module names to their status
    """
    return registry.get_all_statuses()


def setup_modules():
    """
    Setup and initialize all modules
    Call this on app startup
    
    Returns:
        Dict with initialization results
    """
    register_modules()
    results = initialize_modules()
    
    print('Module initialization results:', results)
    
    failed_modules = [name for name, success in results.items() if not success]
    
    if failed_modules:
        print(f'Failed to initialize modules: {failed_modules}')
    
    return results

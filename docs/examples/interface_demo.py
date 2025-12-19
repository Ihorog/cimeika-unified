#!/usr/bin/env python3
"""
Example script demonstrating interface usage in Cimeika

This script shows how to:
1. Import modules
2. Register them with the orchestrator
3. Initialize and use them
4. Query status and process data
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.core import registry
from app.modules.ci.service import CiService
from app.modules.kazkar.service import KazkarService
from app.modules.podija.service import PodijaService
from app.modules.nastrij.service import NastrijService
from app.modules.malya.service import MalyaService
from app.modules.gallery.service import GalleryService
from app.modules.calendar.service import CalendarService


def main():
    print("=" * 60)
    print("Cimeika Module Interface Demo")
    print("=" * 60)
    print()
    
    # Create all module instances
    print("📦 Creating module instances...")
    modules = {
        "ci": CiService(),
        "kazkar": KazkarService(),
        "podija": PodijaService(),
        "nastrij": NastrijService(),
        "malya": MalyaService(),
        "gallery": GalleryService(),
        "calendar": CalendarService(),
    }
    
    # Register all modules
    print("🔧 Registering modules with orchestrator...")
    for name, module in modules.items():
        registry.register(name, module)
    
    print(f"✅ Registered {len(registry.list_modules())} modules")
    print(f"   Modules: {', '.join(registry.list_modules())}")
    print()
    
    # Initialize all modules
    print("🚀 Initializing all modules...")
    init_results = registry.initialize_all()
    
    success_count = sum(1 for v in init_results.values() if v)
    print(f"✅ Initialized {success_count}/{len(init_results)} modules")
    
    for name, success in init_results.items():
        status_icon = "✅" if success else "❌"
        print(f"   {status_icon} {name}")
    print()
    
    # Get all module statuses
    print("📊 Module Statuses:")
    statuses = registry.get_all_statuses()
    for name, status in statuses.items():
        print(f"   • {name}: {status['status']} (initialized: {status['initialized']})")
    print()
    
    # Test processing with a module
    print("🔄 Testing data processing with 'ci' module...")
    ci = registry.get("ci")
    if ci:
        test_data = {"action": "test", "timestamp": "2024-01-01"}
        result = ci.process(test_data)
        print(f"   Input: {test_data}")
        print(f"   Output: {result}")
    print()
    
    # Test validation
    print("✔️  Testing data validation...")
    valid_data = {"key": "value"}
    invalid_data = "not a dict"
    
    if ci:
        print(f"   Valid data {valid_data}: {ci.validate(valid_data)}")
        print(f"   Invalid data {invalid_data}: {ci.validate(invalid_data)}")
    print()
    
    # Get metadata
    print("ℹ️  Module Metadata:")
    for name in ["ci", "kazkar", "podija"]:
        module = registry.get(name)
        if module:
            metadata = module.get_metadata()
            print(f"   • {name}: {metadata}")
    print()
    
    # Shutdown all modules
    print("🛑 Shutting down all modules...")
    shutdown_results = registry.shutdown_all()
    
    success_count = sum(1 for v in shutdown_results.values() if v)
    print(f"✅ Shutdown {success_count}/{len(shutdown_results)} modules")
    print()
    
    print("=" * 60)
    print("✅ Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()

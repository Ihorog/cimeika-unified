#!/usr/bin/env python3
"""
Script to seed Ci Legends into Kazkar module
Скрипт для популяції легенд Ci в модулі Kazkar

Usage:
    python backend/scripts/seed_ci_legends.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from backend.app.config.database import SessionLocal
    from backend.app.modules.kazkar.service import KazkarService
    from backend.app.modules.kazkar.schema import KazkarStoryCreate
    from backend.app.modules.kazkar.ci_legends_seed import get_ci_legends
    from backend.app.modules.kazkar.model import KazkarStory
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


def seed_ci_legends():
    """Seed Ci legends into the database"""
    db = SessionLocal()
    service = KazkarService()
    service.initialize()
    
    try:
        legends = get_ci_legends()
        print(f"🌱 Seeding {len(legends)} Ci legends into Kazkar...")
        print()
        
        created_count = 0
        skipped_count = 0
        
        for legend_data in legends:
            # Check if legend already exists by title
            existing = db.query(KazkarStory).filter(
                KazkarStory.title == legend_data["title"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipping '{legend_data['title']}' - already exists (ID: {existing.id})")
                skipped_count += 1
                continue
            
            # Create legend
            legend_schema = KazkarStoryCreate(**legend_data)
            created_legend = service.create_story(db, legend_schema)
            print(f"✅ Created legend: '{created_legend.title}' (ID: {created_legend.id})")
            created_count += 1
        
        print()
        print(f"🎉 Successfully seeded {created_count} new legends!")
        print(f"⏭️  Skipped {skipped_count} existing legends")
        
        # Get statistics
        all_legends = service.get_legends(db)
        print(f"📚 Total Ci legends in Kazkar: {len(all_legends)}")
        
        # Get type statistics
        stats = service.get_stories_count_by_type(db)
        print()
        print("📊 Statistics by type:")
        for story_type, count in stats.items():
            print(f"   {story_type}: {count}")
        
    except Exception as e:
        print(f"❌ Error seeding legends: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Main entry point"""
    print("=" * 60)
    print("CI LEGENDS SEEDER")
    print("=" * 60)
    print()
    
    try:
        seed_ci_legends()
        print()
        print("=" * 60)
        print("✅ Seeding completed successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Seeding failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

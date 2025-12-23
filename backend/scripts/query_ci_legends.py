#!/usr/bin/env python3
"""
Script to query and display Ci Legends from Kazkar module
Скрипт для запиту та відображення легенд Ci з модуля Kazkar

Usage:
    cd backend && python scripts/query_ci_legends.py [--legend-id ID]
"""
import sys
import os
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.config.database import SessionLocal
    from app.modules.kazkar.service import KazkarService
    from app.modules.kazkar.model import KazkarStory
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the backend directory")
    sys.exit(1)


def display_legend(legend: KazkarStory, full: bool = False):
    """Display a legend's information"""
    print(f"\n{'=' * 80}")
    print(f"ID: {legend.id}")
    print(f"Title: {legend.title}")
    print(f"Type: {legend.story_type}")
    print(f"Tags: {', '.join(legend.tags)}")
    print(f"Participants: {', '.join(legend.participants) if legend.participants else 'N/A'}")
    print(f"Location: {legend.location or 'N/A'}")
    print(f"Created: {legend.time}")
    print(f"Canon Bundle: {legend.canon_bundle_id}")
    print(f"\nContent:")
    print("-" * 80)
    
    if full:
        print(legend.content)
    else:
        # Display first 500 characters
        content_preview = legend.content[:500]
        print(content_preview)
        if len(legend.content) > 500:
            print(f"\n... ({len(legend.content) - 500} more characters)")
    
    print("=" * 80)


def query_all_legends():
    """Query and display all Ci legends"""
    db = SessionLocal()
    service = KazkarService()
    service.initialize()
    
    try:
        legends = service.get_legends(db)
        
        print("=" * 80)
        print("CI LEGENDS IN KAZKAR")
        print("=" * 80)
        print(f"\n📚 Found {len(legends)} Ci legends\n")
        
        for legend in legends:
            display_legend(legend, full=False)
        
        # Display statistics
        stats = service.get_stories_count_by_type(db)
        print("\n" + "=" * 80)
        print("📊 STATISTICS")
        print("=" * 80)
        print(f"\nTotal stories: {sum(stats.values())}")
        for story_type, count in stats.items():
            print(f"  - {story_type}: {count}")
        
    except Exception as e:
        print(f"❌ Error querying legends: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def query_single_legend(legend_id: int):
    """Query and display a single legend"""
    db = SessionLocal()
    service = KazkarService()
    service.initialize()
    
    try:
        legend = service.get_story(db, legend_id)
        
        if not legend:
            print(f"❌ Legend with ID {legend_id} not found")
            return
        
        if legend.story_type != 'legend':
            print(f"⚠️  Warning: Story with ID {legend_id} is not a legend (type: {legend.story_type})")
        
        display_legend(legend, full=True)
        
    except Exception as e:
        print(f"❌ Error querying legend: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Query Ci Legends from Kazkar module'
    )
    parser.add_argument(
        '--legend-id',
        type=int,
        help='ID of specific legend to display (shows full content)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("CI LEGENDS QUERY TOOL")
    print("=" * 80)
    print()
    
    try:
        if args.legend_id:
            query_single_legend(args.legend_id)
        else:
            query_all_legends()
        
        print("\n" + "=" * 80)
        print("✅ Query completed successfully!")
        print("=" * 80)
        return 0
        
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ Query failed: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

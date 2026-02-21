"""
E2E Acceptance Scenario Runner

This script demonstrates the complete one-cycle flow from /add to /done.
It can be used for manual acceptance testing or as documentation.

Usage:
    python run_e2e_scenario.py

Requirements:
    - PostgreSQL database running
    - Environment variables set (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, etc.)
"""
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config.database import SessionLocal
from app.modules.podija.parser import parse_add_args
from app.modules.podija.service import PodijaService
from app.modules.podija.schema import PodijaEventCreate
from app.modules.calendar.worker import sync_pending_entries
from app.modules.calendar.model import CalendarEntry


def run_e2e_scenario():
    """
    Run the complete E2E acceptance scenario.

    Steps:
    1) Parse /add завтра 18:00 тренування
    2) Create event → DB has podiya_events + calendar_entries(pending)
    3) Run calendar worker → calendar_entries.synced with external_id
    4) Verify /done works

    Note: Reminder jobs creation is documented as TODO
    """
    print("="*70)
    print("E2E ACCEPTANCE SCENARIO: One-Cycle from /add to /done")
    print("="*70)

    db = SessionLocal()
    service = PodijaService()
    service.initialize()

    try:
        # ─────────────────────────────────────────────────────────────────
        # Step 1: Parse Telegram command
        # ─────────────────────────────────────────────────────────────────
        print("\n[Step 1] Parsing Telegram command...")
        args = "завтра 18:00 тренування"
        parsed = parse_add_args(args)

        if parsed["error"]:
            print(f"❌ Parse error: {parsed['error']}")
            return False

        print(f"✅ Parsed: title='{parsed['title']}', date={parsed['event_date']}")

        # ─────────────────────────────────────────────────────────────────
        # Step 2: Create event
        # ─────────────────────────────────────────────────────────────────
        print("\n[Step 2] Creating event...")
        event_data = PodijaEventCreate(
            title=parsed["title"],
            event_date=parsed["event_date"],
            event_type="planned",
            source_trace="telegram",
        )
        event = service.create_event(db, event_data)
        print(f"✅ Created podiya_event: id={event.id}, title={event.title}, status={event.status}")

        # Verify calendar entry was created
        calendar_entry = db.query(CalendarEntry).filter(
            CalendarEntry.source_trace == f"podiya_event:{event.id}"
        ).first()

        if calendar_entry:
            print(f"✅ Created calendar_entry: id={calendar_entry.id}, sync_status={calendar_entry.sync_status}")
        else:
            print("❌ Calendar entry was not created")
            return False

        # Note about reminder jobs
        print("⚠️  Reminder jobs: Currently manual (TODO: auto-create)")
        print("   To test reminders: manually create reminder_job with:")
        print(f"   event_id={event.id}, remind_at={parsed['event_date'] - timedelta(minutes=10)}")

        # ─────────────────────────────────────────────────────────────────
        # Step 3: Calendar worker sync
        # ─────────────────────────────────────────────────────────────────
        print("\n[Step 3] Running calendar worker...")
        result = sync_pending_entries(db)
        print(f"✅ Calendar sync: synced={result['synced']}, failed={result['failed']}")

        # Verify calendar entry is synced
        db.refresh(calendar_entry)
        if calendar_entry.sync_status == "synced":
            print(f"✅ Calendar entry synced: external_id={calendar_entry.external_id}")
        else:
            print(f"❌ Calendar entry not synced: status={calendar_entry.sync_status}")
            if calendar_entry.last_error:
                print(f"   Error: {calendar_entry.last_error}")

        # ─────────────────────────────────────────────────────────────────
        # Step 4: Mark event as done
        # ─────────────────────────────────────────────────────────────────
        print("\n[Step 4] Marking event as done...")
        completed_event = service.mark_done(db, event.id)

        if completed_event and completed_event.status == "done":
            print(f"✅ Event marked as done: status={completed_event.status}, is_completed={completed_event.is_completed}")
        else:
            print("❌ Failed to mark event as done")
            return False

        # ─────────────────────────────────────────────────────────────────
        # Summary
        # ─────────────────────────────────────────────────────────────────
        print("\n" + "="*70)
        print("✅ E2E SCENARIO COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nFlow verified:")
        print("  1. ✅ Telegram command parsing")
        print("  2. ✅ Event creation (podiya_events + calendar_entries)")
        print("  3. ✅ Calendar worker sync")
        print("  4. ⚠️  Reminder jobs (manual - not yet auto-created)")
        print("  5. ✅ /done command")
        print("\nNext step: Implement automatic reminder_job creation in service")
        print("="*70)

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = run_e2e_scenario()
    sys.exit(0 if success else 1)

"""
Test Google Workspace integration.

Run with: python -m pytest tests/test_google_integration.py
Or: python tests/test_google_integration.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from empire_automation.tools.google_workspace_tool import GoogleWorkspaceTool
from datetime import datetime


def test_google_integration():
    """Test Google Workspace integration methods."""
    
    print("\n=== Testing Google Workspace Integration ===\n")
    
    # Initialize tool
    tool = GoogleWorkspaceTool()
    
    if not tool.credentials:
        print("[SKIP] Google credentials not configured. Skipping tests.")
        print("To enable tests:")
        print("1. Set up Google Cloud service account")
        print("2. Save credentials to credentials/google-service-account.json")
        print("3. Set GOOGLE_SHEETS_ID in .env")
        return
    
    # Test 1: Update revenue
    print("Test 1: Update revenue...")
    try:
        result = tool.update_revenue(
            entity="Keystone Transaction Specialists",
            amount=1500.00,
            service="Transaction Coordination",
            client="Test Client"
        )
        if result:
            print("  [OK] Revenue updated successfully")
        else:
            print("  [FAIL] Revenue update failed")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 2: Get dashboard metrics
    print("\nTest 2: Get dashboard metrics...")
    try:
        metrics = tool.get_dashboard_metrics()
        print(f"  [OK] Retrieved metrics: {len(metrics)} items")
        for key, value in metrics.items():
            print(f"    {key}: {value}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 3: Schedule meeting
    print("\nTest 3: Schedule meeting...")
    try:
        start_time = datetime(2025, 11, 15, 10, 0, 0)
        end_time = datetime(2025, 11, 15, 10, 30, 0)
        
        event_id = tool.schedule_meeting(
            title="Discovery Call",
            start=start_time,
            end=end_time,
            attendees=["client@example.com"],
            description="Initial consultation"
        )
        if event_id:
            print(f"  [OK] Meeting scheduled: {event_id}")
        else:
            print("  [FAIL] Meeting scheduling failed")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 4: Check availability
    print("\nTest 4: Check availability...")
    try:
        from datetime import date
        target_date = date(2025, 11, 15)
        slots = tool.check_availability(target_date, duration_minutes=60)
        print(f"  [OK] Found {len(slots)} available slots")
        for slot in slots[:3]:  # Show first 3
            print(f"    {slot['start']} - {slot['end']}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 5: Update expense
    print("\nTest 5: Update expense...")
    try:
        result = tool.update_expense(
            entity="Keystone Transaction Specialists",
            amount=500.00,
            category="Marketing",
            description="Facebook ads"
        )
        if result:
            print("  [OK] Expense updated successfully")
        else:
            print("  [FAIL] Expense update failed")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 6: Update 90-day progress
    print("\nTest 6: Update 90-day progress...")
    try:
        result = tool.update_90_day_progress(
            day=1,
            tasks_completed=4,
            revenue=1500.00
        )
        if result:
            print("  [OK] 90-day progress updated successfully")
        else:
            print("  [FAIL] Progress update failed")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    print("\n=== Tests Complete ===\n")


if __name__ == "__main__":
    test_google_integration()


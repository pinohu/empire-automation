"""
Setup Google Sheets with required sheet structure.

Run with: python setup_google_sheets.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from empire_automation.tools.google_workspace_tool import GoogleWorkspaceTool
from googleapiclient.errors import HttpError

# Set environment variables
os.environ['GOOGLE_CREDENTIALS_FILE'] = 'credentials/uplifted-record-477622-b7-f25455bd0df5.json'
os.environ['GOOGLE_SHEETS_ID'] = '1LnDX6u0V5ows33BJyVSohc4tZIBwmut5LnEU8mMWfWk'

def setup_sheets():
    """Check existing sheets and create missing ones."""
    print("\n=== Google Sheets Setup ===\n")
    
    # Initialize tool
    tool = GoogleWorkspaceTool()
    
    if not tool.sheets_service or not tool.spreadsheet_id:
        print("[ERROR] Sheets service not available")
        return
    
    print(f"Spreadsheet ID: {tool.spreadsheet_id}\n")
    
    # Get existing sheets
    try:
        spreadsheet = tool.sheets_service.spreadsheets().get(
            spreadsheetId=tool.spreadsheet_id
        ).execute()
        
        existing_sheets = [s['properties']['title'] for s in spreadsheet.get('sheets', [])]
        print(f"Existing sheets ({len(existing_sheets)}):")
        for sheet in existing_sheets:
            print(f"  - {sheet}")
        
        print()
        
        # Required sheets
        required_sheets = [
            'Revenue Tracking',
            'Expense Tracking',
            '90-Day Plan Progress',
            'Entity Details',
            'Credential Tracker',
            'Lead Pipeline',
            'Dashboard Metrics'
        ]
        
        # Find missing sheets
        missing_sheets = [s for s in required_sheets if s not in existing_sheets]
        
        if missing_sheets:
            print(f"Creating {len(missing_sheets)} missing sheets...")
            
            requests = [
                {'addSheet': {'properties': {'title': name}}}
                for name in missing_sheets
            ]
            
            try:
                result = tool.sheets_service.spreadsheets().batchUpdate(
                    spreadsheetId=tool.spreadsheet_id,
                    body={'requests': requests}
                ).execute()
                
                print("[OK] Sheets created successfully!")
                for sheet in result.get('replies', []):
                    if 'addSheet' in sheet:
                        print(f"  - Created: {sheet['addSheet']['properties']['title']}")
            except HttpError as e:
                print(f"[ERROR] Failed to create sheets: {e}")
        else:
            print("[OK] All required sheets already exist!")
        
        # Set up headers for each sheet
        print("\nSetting up sheet headers...")
        
        headers = {
            'Revenue Tracking': ['Date', 'Entity', 'Service', 'Amount', 'Client', 'Status'],
            'Expense Tracking': ['Date', 'Entity', 'Category', 'Amount', 'Description', 'Status'],
            '90-Day Plan Progress': ['Day', 'Date', 'Tasks', 'Completed', 'Revenue Impact', 'Notes'],
            'Entity Details': ['Entity Name', 'State', 'Type', 'Status', 'EIN', 'Annual Report Due'],
            'Credential Tracker': ['Credential', 'Status', 'Issue Date', 'Expiration', 'Renewal Due', 'Cost'],
            'Lead Pipeline': ['Date', 'Source', 'Name', 'Email', 'Score', 'Status', 'Assigned To'],
            'Dashboard Metrics': ['Metric', 'Value', 'Formula/Notes']
        }
        
        for sheet_name, header_row in headers.items():
            if sheet_name in existing_sheets or sheet_name in missing_sheets:
                try:
                    # Check if headers already exist
                    result = tool.sheets_service.spreadsheets().values().get(
                        spreadsheetId=tool.spreadsheet_id,
                        range=f"{sheet_name}!A1:Z1"
                    ).execute()
                    
                    existing_values = result.get('values', [])
                    
                    if not existing_values or not existing_values[0]:
                        # Add headers
                        tool.sheets_service.spreadsheets().values().update(
                            spreadsheetId=tool.spreadsheet_id,
                            range=f"{sheet_name}!A1",
                            valueInputOption="USER_ENTERED",
                            body={'values': [header_row]}
                        ).execute()
                        print(f"  [OK] Headers added to {sheet_name}")
                    else:
                        print(f"  [SKIP] {sheet_name} already has headers")
                except HttpError as e:
                    print(f"  [WARN] Could not set headers for {sheet_name}: {e}")
        
        print("\n=== Setup Complete ===\n")
        
        # Test a simple operation
        print("Testing revenue update...")
        result = tool.update_revenue(
            entity="Keystone Transaction Specialists",
            amount=1500.00,
            service="Transaction Coordination",
            client="Test Client"
        )
        
        if result:
            print("[OK] Revenue update test successful!")
        else:
            print("[WARN] Revenue update test failed (check sheet structure)")
        
    except HttpError as e:
        print(f"[ERROR] Failed to access spreadsheet: {e}")
        print(f"Details: {e.content.decode() if hasattr(e, 'content') else 'N/A'}")


if __name__ == "__main__":
    setup_sheets()


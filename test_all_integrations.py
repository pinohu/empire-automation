"""
Test all integration tools with configured credentials.

Run with: python test_all_integrations.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*60)
print("INTEGRATION TOOLS TEST SUITE")
print("="*60 + "\n")

# Test 1: AgenticFlow
print("[TEST 1] AgenticFlow Tool")
print("-" * 60)
try:
    from empire_automation.tools.agenticflow_tool import AgenticFlowTool
    tool = AgenticFlowTool()
    print("[OK] AgenticFlow tool initialized")
    print(f"    API Key: {tool.api_key[:20]}...")
    print(f"    Base URL: {tool.base_url}")
except ValueError as e:
    print(f"[SKIP] {e}")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 2: Google Workspace
print("\n[TEST 2] Google Workspace Tool")
print("-" * 60)
try:
    from empire_automation.tools.google_workspace_tool import GoogleWorkspaceTool
    tool = GoogleWorkspaceTool()
    if tool.credentials:
        print("[OK] Google Workspace tool initialized")
        print(f"    Service Account: {tool.credentials.service_account_email}")
        print(f"    Spreadsheet ID: {tool.spreadsheet_id}")
        print(f"    Sheets Service: {'Ready' if tool.sheets_service else 'Not available'}")
    else:
        print("[SKIP] Google credentials not configured")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 3: SuiteDash
print("\n[TEST 3] SuiteDash Tool")
print("-" * 60)
try:
    from empire_automation.tools.suitedash_tool import SuiteDashTool
    tool = SuiteDashTool()
    if tool.session:
        print("[OK] SuiteDash tool initialized")
        print(f"    API Key: {tool.api_key[:20]}...")
        print(f"    Base URL: {tool.base_url}")
        if hasattr(tool, 'api_auth_credential') and tool.api_auth_credential:
            print(f"    Auth Credential: {tool.api_auth_credential[:20]}...")
    else:
        print("[SKIP] SuiteDash API key not configured")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 4: Emailit
print("\n[TEST 4] Emailit Tool")
print("-" * 60)
try:
    from empire_automation.tools.emailit_tool import EmailitTool
    tool = EmailitTool()
    if tool.session:
        print("[OK] Emailit tool initialized")
        print(f"    API Key: {tool.api_key[:20]}...")
        print(f"    Base URL: {tool.base_url}")
    else:
        print("[SKIP] Emailit API key not configured")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 5: Brilliant Directories
print("\n[TEST 5] Brilliant Directories Tool")
print("-" * 60)
try:
    from empire_automation.tools.brilliant_directories_tool import BrilliantDirectoriesTool
    tool = BrilliantDirectoriesTool()
    if tool.session:
        print("[OK] Brilliant Directories tool initialized")
        print(f"    API Key: {tool.api_key[:20]}...")
        print(f"    Base URL: {tool.base_url}")
    else:
        print("[SKIP] Brilliant Directories API key not configured")
except Exception as e:
    print(f"[ERROR] {e}")

# Test 6: Formaloo
print("\n[TEST 6] Formaloo Tool")
print("-" * 60)
try:
    from empire_automation.tools.formaloo_tool import FormalooTool
    tool = FormalooTool()
    if tool.session:
        print("[OK] Formaloo tool initialized")
        print(f"    API Key: {tool.api_key[:30]}...")
        print(f"    Base URL: {tool.base_url}")
        if hasattr(tool, 'api_secret') and tool.api_secret:
            print(f"    API Secret: Configured")
    else:
        print("[SKIP] Formaloo API key not configured")
except Exception as e:
    print(f"[ERROR] {e}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

credentials_status = {
    "AgenticFlow": bool(os.getenv("AGENTICFLOW_API_KEY")),
    "Google Workspace": bool(os.getenv("GOOGLE_CREDENTIALS_FILE")),
    "SuiteDash": bool(os.getenv("SUITEDASH_API_KEY")),
    "Emailit": bool(os.getenv("EMAILIT_API_KEY")),
    "Brilliant Directories": bool(os.getenv("BRILLIANT_DIRECTORIES_API_KEY")),
    "Formaloo": bool(os.getenv("FORMALOO_API_KEY")),
    "Anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
}

configured_count = sum(1 for v in credentials_status.values() if v)
total_count = len(credentials_status)

print(f"\nConfigured: {configured_count}/{total_count} integrations")
print("\nStatus:")
for service, is_configured in credentials_status.items():
    status = "[OK]" if is_configured else "[ ]"
    print(f"  {status} {service}")

print("\n" + "="*60)
if configured_count == total_count:
    print("[OK] ALL INTEGRATIONS CONFIGURED!")
    print(f"    {configured_count}/{total_count} integrations ready to use")
else:
    print(f"[INFO] {configured_count}/{total_count} integrations configured")
    print(f"    {total_count - configured_count} integration(s) still need configuration")
print("="*60 + "\n")


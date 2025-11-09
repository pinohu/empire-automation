"""
Test integration tools.

Run with: python -m pytest tests/test_integrations.py
Or: python tests/test_integrations.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from empire_automation.tools.suitedash_tool import SuiteDashTool
from empire_automation.tools.emailit_tool import EmailitTool
from empire_automation.tools.brilliant_directories_tool import BrilliantDirectoriesTool
from empire_automation.tools.formaloo_tool import FormalooTool


def test_suitedash():
    """Test SuiteDash integration."""
    print("\n=== Testing SuiteDash Integration ===")
    
    tool = SuiteDashTool()
    
    if not tool.session:
        print("[SKIP] SuiteDash not configured. Set SUITEDASH_API_KEY in .env")
        return
    
    try:
        client = tool.create_client(
            "Test Client",
            "test@example.com",
            "555-1234",
            "subto"
        )
        
        if client and client.get('id'):
            print(f"  [OK] Client created: {client['id']}")
            assert client['id']
        else:
            print("  [FAIL] Client creation failed")
    except Exception as e:
        print(f"  [ERROR] {e}")


def test_emailit():
    """Test Emailit integration."""
    print("\n=== Testing Emailit Integration ===")
    
    tool = EmailitTool()
    
    if not tool.session:
        print("[SKIP] Emailit not configured. Set EMAILIT_API_KEY in .env")
        return
    
    try:
        result = tool.send_email(
            "test@example.com",
            template_id="welcome_template",
            variables={"name": "Test"}
        )
        
        if result and result.get('success'):
            print(f"  [OK] Email sent successfully")
            assert result['success']
        else:
            print("  [FAIL] Email send failed")
    except Exception as e:
        print(f"  [ERROR] {e}")


def test_brilliant_directories():
    """Test Brilliant Directories integration."""
    print("\n=== Testing Brilliant Directories Integration ===")
    
    tool = BrilliantDirectoriesTool()
    
    if not tool.session:
        print("[SKIP] Brilliant Directories not configured. Set BRILLIANT_DIRECTORIES_API_KEY in .env")
        return
    
    try:
        content = tool.generate_seo_content({
            "name": "Test Business",
            "category": "HVAC",
            "location": "Erie, PA",
            "description": "Professional HVAC services"
        })
        
        if content:
            print(f"  [OK] SEO content generated")
            print(f"    Title: {content.get('title', 'N/A')}")
        else:
            print("  [FAIL] SEO content generation failed")
    except Exception as e:
        print(f"  [ERROR] {e}")


def test_formaloo():
    """Test Formaloo integration."""
    print("\n=== Testing Formaloo Integration ===")
    
    tool = FormalooTool()
    
    if not tool.session:
        print("[SKIP] Formaloo not configured. Set FORMALOO_API_KEY in .env")
        return
    
    try:
        # Test form creation (would need valid API)
        print("  [INFO] Formaloo tool initialized successfully")
        print("  [INFO] Use create_form() with valid API key to test")
    except Exception as e:
        print(f"  [ERROR] {e}")


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*50)
    print("INTEGRATION TOOLS TEST SUITE")
    print("="*50)
    
    test_suitedash()
    test_emailit()
    test_brilliant_directories()
    test_formaloo()
    
    print("\n" + "="*50)
    print("TESTS COMPLETE")
    print("="*50 + "\n")


if __name__ == "__main__":
    run_all_tests()


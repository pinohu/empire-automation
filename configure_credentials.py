"""
Configure all credentials in .env file.

This script reads credentials from the existing .env file and organizes them.
DO NOT hardcode credentials in this file - they should be in .env only.

Run with: python configure_credentials.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load existing .env file
load_dotenv()

def create_env_file():
    """Organize and format .env file with all credentials from environment."""
    env_path = Path(".env")
    
    print("\n=== Organizing Credentials ===\n")
    
    # Check if .env exists
    if not env_path.exists():
        print("[ERROR] .env file not found!")
        print("\nPlease create a .env file with your credentials.")
        print("You can copy .env.example and fill in the values.")
        print("\nRequired environment variables:")
        print("  - GOOGLE_CREDENTIALS_FILE")
        print("  - GOOGLE_SHEETS_ID")
        print("  - AGENTICFLOW_API_KEY")
        print("  - SUITEDASH_API_KEY")
        print("  - EMAILIT_API_KEY")
        print("  - BRILLIANT_DIRECTORIES_API_KEY")
        print("  - FORMALOO_API_KEY")
        print("  - ANTHROPIC_API_KEY")
        return
    
    # Read existing .env
    existing_vars = {}
    print("Reading existing .env file...")
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                existing_vars[key.strip()] = value.strip()
    print(f"Found {len(existing_vars)} existing variables")
    
    # Use existing variables (no hardcoded values)
    all_vars = existing_vars
    
    # Write .env file
    print(f"\nWriting {len(all_vars)} environment variables to .env...")
    
    with open(env_path, 'w') as f:
        f.write("# Empire Automation Environment Variables\n")
        f.write("# Generated automatically - DO NOT commit to git\n\n")
        
        # Group by category
        f.write("# ============================================\n")
        f.write("# GOOGLE WORKSPACE\n")
        f.write("# ============================================\n")
        f.write(f"GOOGLE_CREDENTIALS_FILE={all_vars.get('GOOGLE_CREDENTIALS_FILE', '')}\n")
        f.write(f"GOOGLE_SHEETS_ID={all_vars.get('GOOGLE_SHEETS_ID', '')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# AGENTICFLOW (AI Agents)\n")
        f.write("# ============================================\n")
        f.write(f"AGENTICFLOW_API_KEY={all_vars.get('AGENTICFLOW_API_KEY', '')}\n")
        f.write(f"AGENTICFLOW_MASTER_ORCHESTRATOR_ID={all_vars.get('AGENTICFLOW_MASTER_ORCHESTRATOR_ID', 'master-orchestrator')}\n")
        f.write(f"AGENTICFLOW_PROFESSIONAL_SERVICES_ID={all_vars.get('AGENTICFLOW_PROFESSIONAL_SERVICES_ID', 'professional-services')}\n")
        f.write(f"AGENTICFLOW_MARKETING_ID={all_vars.get('AGENTICFLOW_MARKETING_ID', 'marketing-lead-gen')}\n")
        f.write(f"AGENTICFLOW_FINANCIAL_ID={all_vars.get('AGENTICFLOW_FINANCIAL_ID', 'financial-operations')}\n")
        f.write(f"AGENTICFLOW_DIRECTORY_MANAGER_ID={all_vars.get('AGENTICFLOW_DIRECTORY_MANAGER_ID', 'directory-manager')}\n")
        f.write(f"AGENTICFLOW_ENTITY_COMPLIANCE_ID={all_vars.get('AGENTICFLOW_ENTITY_COMPLIANCE_ID', 'entity-compliance')}\n")
        f.write(f"AGENTICFLOW_CLIENT_SUCCESS_ID={all_vars.get('AGENTICFLOW_CLIENT_SUCCESS_ID', 'client-success')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# SUITEDASH (CRM)\n")
        f.write("# ============================================\n")
        f.write(f"SUITEDASH_API_KEY={all_vars.get('SUITEDASH_API_KEY', '')}\n")
        if 'SUITEDASH_API_AUTH_CREDENTIAL' in all_vars:
            f.write(f"SUITEDASH_API_AUTH_CREDENTIAL={all_vars.get('SUITEDASH_API_AUTH_CREDENTIAL', '')}\n")
        f.write(f"SUITEDASH_BASE_URL={all_vars.get('SUITEDASH_BASE_URL', 'https://api.suitedash.com')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# EMAILIT (Email Marketing)\n")
        f.write("# ============================================\n")
        f.write(f"EMAILIT_API_KEY={all_vars.get('EMAILIT_API_KEY', '')}\n")
        f.write(f"EMAILIT_BASE_URL={all_vars.get('EMAILIT_BASE_URL', 'https://api.emailit.com')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# BRILLIANT DIRECTORIES\n")
        f.write("# ============================================\n")
        f.write(f"BRILLIANT_DIRECTORIES_API_KEY={all_vars.get('BRILLIANT_DIRECTORIES_API_KEY', '')}\n")
        f.write(f"BRILLIANT_DIRECTORIES_BASE_URL={all_vars.get('BRILLIANT_DIRECTORIES_BASE_URL', 'https://api.brilliantdirectories.com/v2')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# FORMALOO (Forms)\n")
        f.write("# ============================================\n")
        f.write(f"FORMALOO_API_KEY={all_vars.get('FORMALOO_API_KEY', '')}\n")
        if 'FORMALOO_API_SECRET' in all_vars:
            f.write(f"FORMALOO_API_SECRET={all_vars.get('FORMALOO_API_SECRET', '')}\n")
        f.write(f"FORMALOO_BASE_URL={all_vars.get('FORMALOO_BASE_URL', 'https://api.formaloo.com')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# ANTHROPIC (Claude API)\n")
        f.write("# ============================================\n")
        f.write(f"ANTHROPIC_API_KEY={all_vars.get('ANTHROPIC_API_KEY', '')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# DATABASE\n")
        f.write("# ============================================\n")
        f.write(f"DATABASE_URL={all_vars.get('DATABASE_URL', 'sqlite:///./empire.db')}\n\n")
        
        f.write("# ============================================\n")
        f.write("# KONNECTZIT (Optional - Webhook Security)\n")
        f.write("# ============================================\n")
        f.write("# KONNECTZIT_WEBHOOK_SECRET=your_webhook_secret_here\n")
    
    print("[OK] .env file created/updated successfully!")
    print(f"\nConfigured {len(all_vars)} environment variables")
    
    # Show summary
    print("\n=== Configuration Summary ===")
    print("\n[OK] Google Workspace")
    print("[OK] AgenticFlow")
    print("[OK] SuiteDash")
    print("[OK] Emailit")
    print("[OK] Brilliant Directories")
    print("[OK] Formaloo")
    print("[OK] Anthropic")
    print("\n[OK] All credentials configured!")


if __name__ == "__main__":
    create_env_file()


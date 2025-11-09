"""
Additional seed data for templates, service pricing, etc.
"""

import json
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from empire_automation.database.models import Base


def load_business_plan() -> dict:
    """Load business plan JSON data."""
    script_dir = Path(__file__).parent.parent.parent
    plan_path = script_dir / "knowledge" / "business_plan.json"
    
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_email_templates():
    """Seed email templates from Appendix N."""
    templates_dir = Path(__file__).parent.parent.parent / "knowledge" / "templates" / "emails"
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Placeholder - templates will be extracted from business plan
    print("[OK] Email templates directory ready")
    print("  Note: Extract templates from Appendix N of business plan")


def seed_document_templates():
    """Seed document templates from Appendix D."""
    templates_dir = Path(__file__).parent.parent.parent / "knowledge" / "templates" / "documents"
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Placeholder - templates will be extracted from business plan
    print("[OK] Document templates directory ready")
    print("  Note: Extract templates from Appendix D of business plan")


def seed_service_pricing():
    """Seed service pricing from business plan."""
    plan_data = load_business_plan()
    services = plan_data.get("services", {})
    
    # Save service pricing to JSON for reference
    pricing_file = Path(__file__).parent.parent.parent / "knowledge" / "service_pricing.json"
    with open(pricing_file, "w", encoding="utf-8") as f:
        json.dump(services, f, indent=2)
    
    print(f"[OK] Service pricing saved to {pricing_file}")


def seed_all():
    """Seed all additional data."""
    print("Seeding additional data...\n")
    
    seed_email_templates()
    seed_document_templates()
    seed_service_pricing()
    
    print("\n[OK] Additional data seeding complete!")


if __name__ == "__main__":
    seed_all()


"""
Database initialization script.
Creates all tables and seeds initial data from business_plan.json
"""

import json
import os
from pathlib import Path
from datetime import datetime
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from empire_automation.database.models import (
    Base, Entity, Credential, Task, EntityStatus, 
    CredentialStatus, CredentialType, TaskStatus
)


def load_business_plan() -> dict:
    """Load business plan JSON data."""
    script_dir = Path(__file__).parent.parent.parent
    plan_path = script_dir / "knowledge" / "business_plan.json"
    
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_database_url() -> str:
    """Get database URL from environment or default."""
    db_url = os.getenv("DATABASE_URL", "sqlite:///empire.db")
    return db_url


def create_tables(engine):
    """Create all database tables."""
    Base.metadata.create_all(engine)
    print("[OK] Database tables created")


def seed_entities(session, plan_data: dict):
    """Seed entities from business plan."""
    entities = plan_data.get("entities", [])
    
    for entity_data in entities:
        # Check if entity already exists
        existing = session.query(Entity).filter_by(name=entity_data["name"]).first()
        if existing:
            print(f"  Entity '{entity_data['name']}' already exists, skipping")
            continue
        
        entity = Entity(
            name=entity_data["name"],
            state=entity_data["state"],
            type=entity_data["type"],
            ein=entity_data.get("ein") or None,
            status=EntityStatus[entity_data.get("status", "planned").upper()],
            annual_report_due=entity_data.get("annual_report_due") or None,
            annual_report_fee=Decimal(str(entity_data.get("fee", 0))),
        )
        session.add(entity)
        print(f"  [OK] Added entity: {entity_data['name']}")
    
    session.commit()
    print(f"[OK] Seeded {len(entities)} entities")


def seed_credentials(session, plan_data: dict):
    """Seed credentials from business plan."""
    credentials = plan_data.get("credentials", [])
    
    for cred_data in credentials:
        # Check if credential already exists
        existing = session.query(Credential).filter_by(name=cred_data["name"]).first()
        if existing:
            print(f"  Credential '{cred_data['name']}' already exists, skipping")
            continue
        
        credential = Credential(
            name=cred_data["name"],
            type=CredentialType[cred_data["type"].upper()],
            status=CredentialStatus[cred_data.get("status", "planned").upper()],
            required_for=cred_data.get("required_for") or [],
            cost=Decimal(str(cred_data.get("cost", 0))),
            timeline=cred_data.get("timeline") or None,
            revenue_potential=cred_data.get("revenue_potential") or None,
        )
        session.add(credential)
        print(f"  [OK] Added credential: {cred_data['name']}")
    
    session.commit()
    print(f"[OK] Seeded {len(credentials)} credentials")


def seed_tasks(session, plan_data: dict):
    """Seed 90-day plan tasks."""
    plan = plan_data.get("ninety_day_plan", {})
    
    task_count = 0
    for week_key, week_data in plan.items():
        for day_key, day_data in week_data.items():
            tasks = day_data.get("tasks", [])
            day_number = day_data.get("date_offset", 0) + 1
            
            for task_data in tasks:
                # Check if task already exists
                existing = session.query(Task).filter_by(
                    day_number=day_number,
                    description=task_data["description"]
                ).first()
                if existing:
                    continue
                
                task = Task(
                    day_number=day_number,
                    description=task_data["description"],
                    agent_assigned=task_data.get("agent") or None,
                    status=TaskStatus[task_data.get("status", "pending").upper()],
                    owner_required=task_data.get("owner_required", False),
                    estimated_hours=Decimal(str(task_data.get("estimated_hours", 0))) if task_data.get("estimated_hours") else None,
                    cost=Decimal(str(task_data.get("cost", 0))),
                )
                session.add(task)
                task_count += 1
    
    session.commit()
    print(f"[OK] Seeded {task_count} tasks from 90-day plan")


def init_database():
    """Initialize database with tables and seed data."""
    db_url = get_database_url()
    print(f"Connecting to database: {db_url}")
    
    engine = create_engine(db_url, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create tables
        create_tables(engine)
        
        # Load business plan data
        print("\nLoading business plan data...")
        plan_data = load_business_plan()
        
        # Seed data
        print("\nSeeding entities...")
        seed_entities(session, plan_data)
        
        print("\nSeeding credentials...")
        seed_credentials(session, plan_data)
        
        print("\nSeeding tasks...")
        seed_tasks(session, plan_data)
        
        print("\n[OK] Database initialization complete!")
        
    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] Error initializing database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_database()


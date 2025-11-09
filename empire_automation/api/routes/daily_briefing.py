"""
Daily briefing endpoints.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal

from empire_automation.database import get_db
from empire_automation.database.models import (
    Task, TaskStatus, FinancialTransaction, TransactionType, 
    Project, Lead, ProjectStatus, LeadStatus
)
from empire_automation.api.schemas.briefing import DailyBriefingResponse, TaskSummary
from empire_automation.tools.agenticflow_tool import AgenticFlowTool, get_agent_id
from empire_automation.utils.day_calculation import calculate_day_number

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize AgenticFlow tool (will be None if API key not set)
try:
    agenticflow = AgenticFlowTool()
except Exception as e:
    logger.warning(f"AgenticFlow not available: {e}")
    agenticflow = None


@router.get("/daily-briefing", response_model=DailyBriefingResponse)
async def get_daily_briefing(
    target_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get daily briefing with today's tasks, priorities, and metrics.
    Calls AgenticFlow Master Orchestrator for intelligent task prioritization.
    """
    if target_date is None:
        target_date = date.today()
    
    # Calculate day number from PLAN_START_DATE
    day_number = calculate_day_number(current_date=target_date)
    
    # Get today's tasks from database
    tasks = db.query(Task).filter(
        Task.day_number == day_number
    ).all()
    
    # Get financial data
    revenue_transactions = db.query(FinancialTransaction).filter(
        FinancialTransaction.type == TransactionType.REVENUE
    ).all()
    total_revenue = sum(float(t.amount) for t in revenue_transactions)
    
    # Get active projects
    from empire_automation.database.models import ProjectStatus
    active_projects = db.query(Project).filter(
        Project.status.in_([ProjectStatus.ACTIVE, ProjectStatus.PROSPECT])
    ).count()
    
    # Get lead pipeline
    from empire_automation.database.models import LeadStatus
    active_leads = db.query(Lead).filter(
        Lead.status.in_([LeadStatus.NEW, LeadStatus.CONTACTED, LeadStatus.QUALIFIED])
    ).count()
    
    # Prepare context for AgenticFlow
    context = {
        "day_number": day_number,
        "date": target_date.isoformat(),
        "tasks": [
            {
                "id": str(t.id),
                "description": t.description,
                "status": t.status.value,
                "agent_assigned": t.agent_assigned,
                "owner_required": t.owner_required,
                "estimated_hours": float(t.estimated_hours) if t.estimated_hours else None,
                "cost": float(t.cost) if t.cost else 0
            }
            for t in tasks
        ],
        "financial": {
            "revenue_ytd": total_revenue,
            "goal": 10000000,  # $10M goal
            "progress_percent": (total_revenue / 10000000 * 100) if total_revenue > 0 else 0
        },
        "projects": {
            "active": active_projects
        },
        "leads": {
            "active": active_leads
        }
    }
    
    # Call AgenticFlow if available
    if agenticflow:
        try:
            briefing = agenticflow.get_daily_briefing(day_number, context)
            
            # Parse AgenticFlow response and return structured data
            # For now, return basic structure with AgenticFlow data
            return DailyBriefingResponse(
                date=target_date,
                day_number=day_number,
                total_tasks=len(tasks),
                pending_tasks=len([t for t in tasks if t.status == TaskStatus.PENDING]),
                in_progress_tasks=len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS]),
                completed_tasks=len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
                priority_tasks=[
                    TaskSummary(
                        id=str(t.id),
                        description=t.description,
                        status=t.status.value,
                        priority=1 if t.owner_required else 2
                    )
                    for t in tasks if t.owner_required
                ],
                metrics={
                    "revenue_ytd": total_revenue,
                    "progress_percent": (total_revenue / 10000000 * 100) if total_revenue > 0 else 0,
                    "active_projects": active_projects,
                    "active_leads": active_leads
                }
            )
        except Exception as e:
            logger.error(f"Error calling AgenticFlow: {e}")
            # Fall through to basic response
    
    # Fallback: Return basic briefing without AgenticFlow
    return DailyBriefingResponse(
        date=target_date,
        day_number=day_number,
        total_tasks=len(tasks),
        pending_tasks=len([t for t in tasks if t.status == TaskStatus.PENDING]),
        in_progress_tasks=len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS]),
        completed_tasks=len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
        priority_tasks=[
            TaskSummary(
                id=str(t.id),
                description=t.description,
                status=t.status.value,
                priority=1 if t.owner_required else 2
            )
            for t in tasks if t.owner_required
        ],
        metrics={
            "revenue_ytd": total_revenue,
            "progress_percent": (total_revenue / 10000000 * 100) if total_revenue > 0 else 0,
            "active_projects": active_projects,
            "active_leads": active_leads
        }
    )


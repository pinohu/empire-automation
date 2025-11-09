"""
90-Day Plan endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from empire_automation.database import get_db
from empire_automation.database.models import Task, TaskStatus
from empire_automation.api.schemas.plan_90_day import (
    TaskResponse, PlanProgressResponse
)
from empire_automation.utils.day_calculation import (
    calculate_day_number,
    calculate_days_remaining
)

router = APIRouter()


@router.get("/today", response_model=List[TaskResponse])
async def get_today_tasks(
    target_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get today's tasks from the 90-day plan.
    
    Calculates day number from PLAN_START_DATE environment variable.
    """
    if target_date is None:
        target_date = date.today()
    
    # Calculate day number from start date
    day_number = calculate_day_number(current_date=target_date)
    
    tasks = db.query(Task).filter(Task.day_number == day_number).all()
    return tasks


@router.get("/progress", response_model=PlanProgressResponse)
async def get_plan_progress(
    db: Session = Depends(get_db)
):
    """
    Get overall progress of the 90-day plan.
    Returns completion statistics and metrics.
    """
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(
        Task.status == TaskStatus.COMPLETED
    ).count()
    pending_tasks = db.query(Task).filter(
        Task.status == TaskStatus.PENDING
    ).count()
    in_progress_tasks = db.query(Task).filter(
        Task.status == TaskStatus.IN_PROGRESS
    ).count()
    
    completion_percentage = (
        (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    )
    
    # Calculate current day and days remaining
    current_day = calculate_day_number()
    days_remaining = calculate_days_remaining(current_day)
    
    return PlanProgressResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        in_progress_tasks=in_progress_tasks,
        completion_percentage=completion_percentage,
        current_day=current_day,
        days_remaining=days_remaining
    )


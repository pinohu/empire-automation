"""
Schemas for 90-day plan endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: UUID
    day_number: int
    description: str
    agent_assigned: Optional[str] = None
    status: str
    owner_required: bool
    estimated_hours: Optional[Decimal] = None
    cost: Decimal
    milestone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlanProgressResponse(BaseModel):
    """Schema for plan progress response."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completion_percentage: float
    current_day: int
    days_remaining: int


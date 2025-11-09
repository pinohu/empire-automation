"""
Schemas for daily briefing endpoints.
"""

from datetime import date
from typing import List, Dict, Optional
from pydantic import BaseModel


class TaskSummary(BaseModel):
    """Task summary for briefing."""
    id: str
    description: str
    status: str
    priority: Optional[int] = None
    
    class Config:
        from_attributes = True


class DailyBriefingResponse(BaseModel):
    """Daily briefing response."""
    date: date
    day_number: int
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    priority_tasks: List[TaskSummary]
    metrics: Dict[str, float]


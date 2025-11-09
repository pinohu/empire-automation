"""
Schemas for agent endpoints.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class AgentExecuteRequest(BaseModel):
    """Request to execute an agent task."""
    task_id: str
    parameters: Optional[Dict[str, Any]] = None


class AgentExecuteResponse(BaseModel):
    """Response from agent execution."""
    agent_id: str
    task_id: str
    status: str
    result: Dict[str, Any]
    message: str


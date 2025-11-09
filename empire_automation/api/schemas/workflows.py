"""
Schemas for workflow endpoints.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class WorkflowTriggerRequest(BaseModel):
    """Request to trigger a workflow."""
    workflow_id: str
    parameters: Optional[Dict[str, Any]] = None


class WorkflowTriggerResponse(BaseModel):
    """Response from workflow trigger."""
    workflow_id: str
    status: str
    execution_id: str
    result: Dict[str, Any]
    message: str


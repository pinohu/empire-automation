"""
Agent execution endpoints.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from empire_automation.database import get_db
from empire_automation.database.models import Task
from empire_automation.api.schemas.agents import AgentExecuteRequest, AgentExecuteResponse
from empire_automation.tools.agenticflow_tool import AgenticFlowTool, get_agent_id

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize AgenticFlow tool (will be None if API key not set)
try:
    agenticflow = AgenticFlowTool()
except Exception as e:
    logger.warning(f"AgenticFlow not available: {e}")
    agenticflow = None


@router.post("/{agent_id}/execute", response_model=AgentExecuteResponse)
async def execute_agent_task(
    agent_id: str,
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """
    Execute a task for a specific agent.
    
    Calls AgenticFlow agent with the task and returns the result.
    """
    # Get task from database if task_id provided
    task_data = {}
    if request.task_id:
        task = db.query(Task).filter(Task.id == request.task_id).first()
        if task:
            task_data = {
                "task_id": str(task.id),
                "description": task.description,
                "agent_assigned": task.agent_assigned,
                "owner_required": task.owner_required,
                "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
                "cost": float(task.cost) if task.cost else 0,
                "priority": "high" if task.owner_required else "normal"
            }
    
    # Merge with request parameters
    task_data.update(request.parameters or {})
    
    # Call AgenticFlow if available
    if agenticflow:
        try:
            result = agenticflow.delegate_task(agent_id, task_data)
            
            return AgentExecuteResponse(
                agent_id=agent_id,
                task_id=request.task_id or "unknown",
                status=result.get("status", "completed"),
                result=result.get("result", {}),
                message=result.get("message", f"Task executed by {agent_id}")
            )
        except Exception as e:
            logger.error(f"Error executing agent task: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error executing agent task: {str(e)}"
            )
    
    # Fallback: Return placeholder if AgenticFlow not available
    return AgentExecuteResponse(
        agent_id=agent_id,
        task_id=request.task_id or "unknown",
        status="pending",
        result={},
        message=f"AgenticFlow not configured. Task {request.task_id} would be queued for agent {agent_id}"
    )


# Convenience endpoints for each agent type
@router.post("/master-orchestrator/execute", response_model=AgentExecuteResponse)
async def execute_master_orchestrator(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Master Orchestrator agent."""
    return await execute_agent_task(get_agent_id("master_orchestrator"), request, db)


@router.post("/professional-services/execute", response_model=AgentExecuteResponse)
async def execute_professional_services(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Professional Services agent."""
    return await execute_agent_task(get_agent_id("professional_services"), request, db)


@router.post("/marketing/execute", response_model=AgentExecuteResponse)
async def execute_marketing(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Marketing & Lead Generation agent."""
    return await execute_agent_task(get_agent_id("marketing"), request, db)


@router.post("/financial/execute", response_model=AgentExecuteResponse)
async def execute_financial(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Financial Operations agent."""
    return await execute_agent_task(get_agent_id("financial"), request, db)


@router.post("/directory-manager/execute", response_model=AgentExecuteResponse)
async def execute_directory_manager(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Directory Manager agent."""
    return await execute_agent_task(get_agent_id("directory_manager"), request, db)


@router.post("/entity-compliance/execute", response_model=AgentExecuteResponse)
async def execute_entity_compliance(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Entity Compliance agent."""
    return await execute_agent_task(get_agent_id("entity_compliance"), request, db)


@router.post("/client-success/execute", response_model=AgentExecuteResponse)
async def execute_client_success(
    request: AgentExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute task with Client Success agent."""
    return await execute_agent_task(get_agent_id("client_success"), request, db)


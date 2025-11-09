"""
Workflow trigger endpoints.
"""

import os
import logging
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from empire_automation.database import get_db
from empire_automation.api.schemas.workflows import (
    WorkflowTriggerRequest, WorkflowTriggerResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/trigger", response_model=WorkflowTriggerResponse)
async def trigger_workflow(
    request: WorkflowTriggerRequest,
    db: Session = Depends(get_db)
):
    """
    Trigger a workflow in n8n.
    
    Sends webhook request to n8n workflow endpoint.
    """
    n8n_base_url = os.getenv("N8N_BASE_URL", "http://localhost:5678")
    n8n_webhook_path = os.getenv("N8N_WEBHOOK_PATH", f"/webhook/{request.workflow_id}")
    
    webhook_url = f"{n8n_base_url}{n8n_webhook_path}"
    
    try:
        # Send webhook to n8n
        response = requests.post(
            webhook_url,
            json=request.parameters or {},
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        execution_id = response.headers.get("X-Execution-Id") or f"exec_{request.workflow_id}"
        result = response.json() if response.content else {}
        
        logger.info(f"Workflow {request.workflow_id} triggered successfully: {execution_id}")
        
        return WorkflowTriggerResponse(
            workflow_id=request.workflow_id,
            status="triggered",
            execution_id=execution_id,
            result=result,
            message=f"Workflow {request.workflow_id} triggered successfully"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error triggering workflow {request.workflow_id}: {e}")
        raise HTTPException(
            status_code=502,
            detail=f"Failed to trigger workflow: {str(e)}"
        )


"""
Webhook handlers for KonnectzIT workflows.
"""

import logging
import hmac
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from uuid import uuid4

from empire_automation.database import get_db
from empire_automation.database.models import Client, Project, Lead, FinancialTransaction
from empire_automation.api.schemas.webhooks import (
    ClientOnboardingWebhook,
    LeadProcessingWebhook,
    FinancialTransactionWebhook,
    DirectoryMemberWebhook,
    ComplianceWebhook,
    WebhookResponse
)
from empire_automation.tools.google_workspace_tool import GoogleWorkspaceTool
from empire_automation.tools.agenticflow_tool import AgenticFlowTool, get_agent_id
from empire_automation.utils.entity_mapping import (
    map_service_to_entity,
    map_service_to_entity_name,
    find_client_by_name
)
from empire_automation.utils.notifications import send_owner_notification

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize tools
try:
    google_tool = GoogleWorkspaceTool()
except Exception as e:
    logger.warning(f"Google Workspace tool not available: {e}")
    google_tool = None

try:
    agenticflow = AgenticFlowTool()
except Exception as e:
    logger.warning(f"AgenticFlow not available: {e}")
    agenticflow = None


def verify_webhook_signature(
    payload: bytes,
    signature: Optional[str],
    secret: Optional[str] = None
) -> bool:
    """
    Verify webhook signature if KonnectzIT provides one.
    
    In production, signature is required if secret is configured.
    
    Args:
        payload: Request body bytes
        signature: Signature header value
        secret: Webhook secret (from env)
        
    Returns:
        True if signature is valid or verification is disabled
    """
    import os
    environment = os.getenv("ENVIRONMENT", "development")
    
    if not secret:
        # In production, require secret to be configured
        if environment == "production":
            logger.warning("Webhook secret not configured in production")
            return False
        return True  # No secret configured, allow in development
    
    if not signature:
        # In production, require signature if secret is configured
        if environment == "production":
            logger.warning("Webhook signature missing in production")
            return False
        return True  # Allow in development if no signature
    
    try:
        expected_signature = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    except Exception as e:
        logger.error(f"Error verifying signature: {e}")
        return False


@router.post("/webhooks/konnectzit/client-onboarding", response_model=WebhookResponse)
async def handle_client_onboarding(
    data: ClientOnboardingWebhook,
    request: Request,
    x_signature: Optional[str] = Header(None, alias="X-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle client onboarding webhook from KonnectzIT.
    
    Receives webhook, validates data, creates client and project in database.
    """
    # Verify signature if configured
    import os
    secret = os.getenv("KONNECTZIT_WEBHOOK_SECRET")
    if secret:
        body = await request.body()
        if not verify_webhook_signature(body, x_signature, secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        # Create client in database
        client = Client(
            name=data.client_name,
            email=data.email,
            phone=data.phone,
            source=data.source or "webhook",
            status="active"
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        
        logger.info(f"Client created via webhook: {client.name} ({client.id})")
        
        # Create project if service specified
        project = None
        if data.service:
            entity_id = map_service_to_entity(data.service, db)
            if not entity_id:
                logger.warning(f"Could not map service '{data.service}' to entity, skipping project creation")
            else:
                project = Project(
                    client_id=client.id,
                    entity_id=entity_id,
                    type=data.service,
                    status="prospect"
                )
                db.add(project)
                db.commit()
                db.refresh(project)
                
                logger.info(f"Project created: {project.id}")
        
        # Update Google Sheets if available
        if google_tool:
            try:
                entity_name = map_service_to_entity_name(data.service or "Unknown", db)
                google_tool.update_revenue(
                    entity=entity_name,
                    amount=0,  # No revenue yet
                    service=data.service or "Unknown",
                    client=data.client_name
                )
            except Exception as e:
                logger.error(f"Error updating Google Sheets: {e}")
        
        return WebhookResponse(
            success=True,
            message=f"Client {client.name} onboarded successfully",
            data={
                "client_id": str(client.id),
                "project_id": str(project.id) if project else None
            }
        )
        
    except Exception as e:
        logger.error(f"Error handling client onboarding webhook: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.post("/webhooks/konnectzit/lead-processing", response_model=WebhookResponse)
async def handle_lead_processing(
    data: LeadProcessingWebhook,
    request: Request,
    x_signature: Optional[str] = Header(None, alias="X-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle lead processing webhook from KonnectzIT.
    
    Processes lead, scores it, and creates lead record.
    """
    import os
    secret = os.getenv("KONNECTZIT_WEBHOOK_SECRET")
    if secret:
        body = await request.body()
        if not verify_webhook_signature(body, x_signature, secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        # Score lead using AgenticFlow Marketing Agent if available
        score = data.score or 0
        if agenticflow and not data.score:
            try:
                result = agenticflow.call_agent(
                    get_agent_id("marketing"),
                    f"Score this lead: {data.name}, Source: {data.source}, Notes: {data.notes or 'None'}",
                    {"lead_data": data.dict()}
                )
                # Extract score from agent response (would need parsing)
                score = 50  # Default if parsing fails
            except Exception as e:
                logger.error(f"Error scoring lead with AgenticFlow: {e}")
        
        # Create lead in database
        lead = Lead(
            name=data.name,
            email=data.email,
            phone=data.phone,
            source=data.source,
            score=score,
            status="new",
            notes=data.notes,
            assigned_to=data.assigned_to
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        logger.info(f"Lead processed: {lead.name} (Score: {score})")
        
        # Update Google Sheets if available
        if google_tool:
            try:
                google_tool.update_lead_pipeline(
                    name=lead.name,
                    source=lead.source,
                    email=lead.email,
                    phone=lead.phone,
                    score=score,
                    status=lead.status.value,
                    assigned_to=lead.assigned_to
                )
            except Exception as e:
                logger.error(f"Error updating Google Sheets: {e}")
        
        # Send notification if high score
        if score > 80:
            logger.info(f"HIGH PRIORITY LEAD: {lead.name} (Score: {score})")
            send_owner_notification(
                message=f"High priority lead received: {lead.name} (Score: {score}, Source: {lead.source})",
                priority="high",
                subject=f"High Priority Lead: {lead.name}"
            )
        
        return WebhookResponse(
            success=True,
            message=f"Lead {lead.name} processed successfully",
            data={
                "lead_id": str(lead.id),
                "score": score
            }
        )
        
    except Exception as e:
        logger.error(f"Error handling lead processing webhook: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.post("/webhooks/konnectzit/financial", response_model=WebhookResponse)
async def handle_financial_transaction(
    data: FinancialTransactionWebhook,
    request: Request,
    x_signature: Optional[str] = Header(None, alias="X-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle financial transaction webhook from KonnectzIT.
    
    Records transaction, updates Google Sheets, checks milestones.
    """
    import os
    secret = os.getenv("KONNECTZIT_WEBHOOK_SECRET")
    if secret:
        body = await request.body()
        if not verify_webhook_signature(body, x_signature, secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        # Get entity ID (would need entity lookup)
        # For now, using placeholder
        from empire_automation.database.models import Entity
        entity = db.query(Entity).filter(Entity.name == data.entity).first()
        if not entity:
            raise HTTPException(status_code=404, detail=f"Entity not found: {data.entity}")
        
        # Lookup client if provided
        client_id = None
        if data.client_name:
            client_id = find_client_by_name(data.client_name, db)
        
        # Create transaction in database
        transaction = FinancialTransaction(
            entity_id=entity.id,
            client_id=client_id,
            date=data.date,
            amount=data.amount,
            type=data.transaction_type,
            category=data.category,
            description=data.description
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Transaction recorded: {data.transaction_type} ${data.amount} for {data.entity}")
        
        # Update Google Sheets
        if google_tool:
            try:
                if data.transaction_type == "revenue":
                    google_tool.update_revenue(
                        entity=data.entity,
                        amount=float(data.amount),
                        service=data.category or "Unknown",
                        client=data.client_name or "Unknown",
                        date=data.date
                    )
                else:
                    google_tool.update_expense(
                        entity=data.entity,
                        amount=float(data.amount),
                        category=data.category or "Other",
                        description=data.description or "",
                        date=data.date
                    )
            except Exception as e:
                logger.error(f"Error updating Google Sheets: {e}")
        
        # Check milestones using AgenticFlow Financial Agent
        if agenticflow:
            try:
                agenticflow.call_agent(
                    get_agent_id("financial"),
                    f"Transaction recorded: {data.transaction_type} ${data.amount}. Check if milestone reached.",
                    {"transaction": data.dict()}
                )
            except Exception as e:
                logger.error(f"Error checking milestones: {e}")
        
        return WebhookResponse(
            success=True,
            message=f"Transaction recorded successfully",
            data={
                "transaction_id": str(transaction.id),
                "amount": float(data.amount),
                "type": data.transaction_type
            }
        )
        
    except Exception as e:
        logger.error(f"Error handling financial webhook: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.post("/webhooks/konnectzit/directory", response_model=WebhookResponse)
async def handle_directory_member(
    data: DirectoryMemberWebhook,
    request: Request,
    x_signature: Optional[str] = Header(None, alias="X-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle directory member onboarding webhook from KonnectzIT.
    
    Processes new directory member, tracks revenue, notifies agent.
    """
    import os
    secret = os.getenv("KONNECTZIT_WEBHOOK_SECRET")
    if secret:
        body = await request.body()
        if not verify_webhook_signature(body, x_signature, secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        # Record revenue transaction
        from empire_automation.database.models import Entity
        entity = db.query(Entity).filter(Entity.name == data.directory_name).first()
        if not entity:
            # Use default directory entity
            entity = db.query(Entity).filter(Entity.name.like("%Directory%")).first()
        
        if entity:
            transaction = FinancialTransaction(
                entity_id=entity.id,
                date=datetime.now(),
                amount=data.membership_fee,
                type="revenue",
                category="Directory Membership",
                description=f"Member: {data.member_name}"
            )
            db.add(transaction)
            db.commit()
            
            logger.info(f"Directory member processed: {data.member_name} (${data.membership_fee})")
        
        # Update Google Sheets
        if google_tool:
            try:
                google_tool.update_revenue(
                    entity=data.directory_name,
                    amount=float(data.membership_fee),
                    service="Directory Membership",
                    client=data.member_name
                )
            except Exception as e:
                logger.error(f"Error updating Google Sheets: {e}")
        
        # Notify Directory Manager Agent
        if agenticflow:
            try:
                agenticflow.call_agent(
                    get_agent_id("directory_manager"),
                    f"New directory member: {data.member_name} for {data.directory_name}",
                    {"member_data": data.dict()}
                )
            except Exception as e:
                logger.error(f"Error notifying agent: {e}")
        
        return WebhookResponse(
            success=True,
            message=f"Directory member {data.member_name} processed",
            data={
                "member_name": data.member_name,
                "directory": data.directory_name,
                "fee": float(data.membership_fee)
            }
        )
        
    except Exception as e:
        logger.error(f"Error handling directory webhook: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


@router.post("/webhooks/konnectzit/compliance", response_model=WebhookResponse)
async def handle_compliance_check(
    data: ComplianceWebhook,
    request: Request,
    x_signature: Optional[str] = Header(None, alias="X-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle compliance check webhook from KonnectzIT.
    
    Processes compliance deadlines and creates reminders.
    """
    import os
    secret = os.getenv("KONNECTZIT_WEBHOOK_SECRET")
    if secret:
        body = await request.body()
        if not verify_webhook_signature(body, x_signature, secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        # Process compliance deadlines
        # This would typically create tasks or send notifications
        
        logger.info(f"Compliance check processed: {len(data.deadlines)} deadlines")
        
        # Notify Entity Compliance Agent
        if agenticflow:
            try:
                agenticflow.call_agent(
                    get_agent_id("entity_compliance"),
                    f"Compliance check: {len(data.deadlines)} deadlines found",
                    {"deadlines": data.deadlines}
                )
            except Exception as e:
                logger.error(f"Error notifying agent: {e}")
        
        return WebhookResponse(
            success=True,
            message=f"Compliance check processed: {len(data.deadlines)} deadlines",
            data={
                "deadlines_count": len(data.deadlines),
                "deadlines": data.deadlines
            }
        )
        
    except Exception as e:
        logger.error(f"Error handling compliance webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")


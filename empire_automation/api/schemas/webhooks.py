"""
Pydantic schemas for webhook requests.
"""

from datetime import date, datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
from pydantic import BaseModel, EmailStr


class ClientOnboardingWebhook(BaseModel):
    """Schema for client onboarding webhook."""
    client_name: str
    email: EmailStr
    phone: Optional[str] = None
    service: Optional[str] = None
    source: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class LeadProcessingWebhook(BaseModel):
    """Schema for lead processing webhook."""
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: str
    score: Optional[int] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class FinancialTransactionWebhook(BaseModel):
    """Schema for financial transaction webhook."""
    entity: str
    amount: Decimal
    transaction_type: str  # "revenue" or "expense"
    category: Optional[str] = None
    description: Optional[str] = None
    date: date
    client_name: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class DirectoryMemberWebhook(BaseModel):
    """Schema for directory member webhook."""
    member_name: str
    member_email: Optional[EmailStr] = None
    directory_name: str
    membership_fee: Decimal
    membership_tier: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


class ComplianceDeadline(BaseModel):
    """Schema for compliance deadline."""
    entity_name: str
    deadline_type: str  # "annual_report", "license_renewal", etc.
    due_date: date
    days_remaining: int
    fee: Optional[Decimal] = None


class ComplianceWebhook(BaseModel):
    """Schema for compliance check webhook."""
    check_date: date
    deadlines: List[ComplianceDeadline]
    additional_data: Optional[Dict[str, Any]] = None


class WebhookResponse(BaseModel):
    """Schema for webhook response."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.utcnow()


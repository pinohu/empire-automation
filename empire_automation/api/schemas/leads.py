"""
Schemas for lead endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class LeadBase(BaseModel):
    """Base lead schema."""
    source: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    score: Optional[int] = 0
    status: Optional[str] = "new"
    notes: Optional[str] = None
    assigned_to: Optional[str] = None
    client_id: Optional[UUID] = None


class LeadCreate(LeadBase):
    """Schema for creating a lead."""
    pass


class LeadUpdate(BaseModel):
    """Schema for updating a lead."""
    source: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    score: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None
    client_id: Optional[UUID] = None


class LeadResponse(LeadBase):
    """Schema for lead response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


"""
Schemas for client endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    """Base client schema."""
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: str  # Client status as string


class ClientCreate(ClientBase):
    """Schema for creating a client."""
    pass


class ClientUpdate(BaseModel):
    """Schema for updating a client."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    lifetime_value: Optional[float] = None


class ClientResponse(ClientBase):
    """Schema for client response."""
    id: UUID
    lifetime_value: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


"""
Schemas for project endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, model_serializer


class ProjectBase(BaseModel):
    """Base project schema."""
    client_id: UUID
    entity_id: UUID
    type: str  # ProjectType enum value as string
    status: str  # ProjectStatus enum value as string
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    revenue: Decimal
    margin: Optional[Decimal] = None
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    client_id: Optional[UUID] = None
    entity_id: Optional[UUID] = None
    type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    revenue: Optional[Decimal] = None
    margin: Optional[Decimal] = None
    notes: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    @model_serializer
    def serialize_model(self):
        """Serialize model, converting enum values to strings."""
        data = self.model_dump()
        # Convert enum values to strings if they exist
        if hasattr(self, 'type') and hasattr(self.type, 'value'):
            data['type'] = self.type.value
        if hasattr(self, 'status') and hasattr(self.status, 'value'):
            data['status'] = self.status.value
        return data

    class Config:
        from_attributes = True


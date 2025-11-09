"""
Schemas for financial endpoints.
"""

from datetime import datetime
from typing import Dict, Optional
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, model_serializer


class TransactionBase(BaseModel):
    """Base transaction schema."""
    entity_id: UUID
    client_id: Optional[UUID] = None
    date: datetime
    amount: Decimal
    type: str  # "revenue" or "expense"
    category: Optional[str] = None
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
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
        return data

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    """Schema for dashboard response."""
    period_start: datetime
    period_end: datetime
    total_revenue: float
    total_expenses: float
    net_profit: float
    transaction_count: int
    revenue_by_entity: Dict[str, float]
    expense_by_category: Dict[str, float]


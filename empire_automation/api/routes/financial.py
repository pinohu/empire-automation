"""
Financial transaction and dashboard endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

from empire_automation.database import get_db
from empire_automation.database.models import FinancialTransaction, TransactionType
from empire_automation.api.schemas.financial import (
    TransactionCreate, TransactionResponse, DashboardResponse
)

router = APIRouter()


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Record a financial transaction."""
    # Convert type string to enum
    transaction_dict = transaction_data.dict()
    if "type" in transaction_dict and isinstance(transaction_dict["type"], str):
        transaction_dict["type"] = TransactionType[transaction_dict["type"].upper()]
    
    transaction = FinancialTransaction(**transaction_dict)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/transactions", response_model=List[TransactionResponse])
async def list_transactions(
    entity_id: UUID = None,
    start_date: date = None,
    end_date: date = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List financial transactions with optional filters."""
    query = db.query(FinancialTransaction)
    
    if entity_id:
        query = query.filter(FinancialTransaction.entity_id == entity_id)
    if start_date:
        query = query.filter(FinancialTransaction.date >= start_date)
    if end_date:
        query = query.filter(FinancialTransaction.date <= end_date)
    
    transactions = query.offset(skip).limit(limit).all()
    return transactions


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get financial dashboard data.
    Returns revenue, expenses, profit, and other key metrics.
    """
    query = db.query(FinancialTransaction)
    
    if start_date:
        # Convert date to datetime if needed
        if isinstance(start_date, date) and not isinstance(start_date, datetime):
            start_date = datetime.combine(start_date, datetime.min.time())
        query = query.filter(FinancialTransaction.date >= start_date)
    if end_date:
        # Convert date to datetime if needed
        if isinstance(end_date, date) and not isinstance(end_date, datetime):
            end_date = datetime.combine(end_date, datetime.max.time())
        query = query.filter(FinancialTransaction.date <= end_date)
    
    transactions = query.all()
    
    # Calculate metrics
    total_revenue = sum(
        float(t.amount) for t in transactions 
        if t.type == TransactionType.REVENUE
    )
    total_expenses = sum(
        float(t.amount) for t in transactions 
        if t.type == TransactionType.EXPENSE
    )
    net_profit = total_revenue - total_expenses
    
    # Aggregate revenue by entity
    revenue_by_entity = {}
    for t in transactions:
        if t.type == TransactionType.REVENUE:
            entity_id_str = str(t.entity_id)
            if entity_id_str not in revenue_by_entity:
                revenue_by_entity[entity_id_str] = 0.0
            revenue_by_entity[entity_id_str] += float(t.amount)
    
    # Aggregate expenses by category
    expense_by_category = {}
    for t in transactions:
        if t.type == TransactionType.EXPENSE:
            category = t.category or "Other"
            if category not in expense_by_category:
                expense_by_category[category] = 0.0
            expense_by_category[category] += float(t.amount)
    
    # Default to current month if no dates provided
    if start_date is None:
        from datetime import date as date_type
        start_date = datetime.combine(date_type.today().replace(day=1), datetime.min.time())
    if end_date is None:
        from datetime import date as date_type
        from calendar import monthrange
        last_day = monthrange(date_type.today().year, date_type.today().month)[1]
        end_date = datetime.combine(date_type.today().replace(day=last_day), datetime.max.time())
    
    return DashboardResponse(
        period_start=start_date,
        period_end=end_date,
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        net_profit=net_profit,
        transaction_count=len(transactions),
        revenue_by_entity=revenue_by_entity,
        expense_by_category=expense_by_category
    )


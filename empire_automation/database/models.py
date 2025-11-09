"""
Database models for Empire Automation system.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, 
    Text, Numeric, JSON, Enum as SQLEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class EntityStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELINQUENT = "delinquent"
    PLANNED = "planned"


class CredentialStatus(str, enum.Enum):
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    PLANNED = "planned"
    EXPIRED = "expired"


class CredentialType(str, enum.Enum):
    LICENSE = "license"
    CERTIFICATION = "certification"
    MEMBERSHIP = "membership"
    POSITION = "position"


class ProjectStatus(str, enum.Enum):
    PROSPECT = "prospect"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectType(str, enum.Enum):
    TRANSACTION_COORDINATION = "TC"
    MORTGAGE = "mortgage"
    TAX = "tax"
    NOTARY = "notary"
    UX_CONSULTING = "ux_consulting"
    OTHER = "other"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    DEFERRED = "deferred"


class TransactionType(str, enum.Enum):
    REVENUE = "revenue"
    EXPENSE = "expense"


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATING = "negotiating"
    WON = "won"
    LOST = "lost"


class Entity(Base):
    """Business entity model."""
    __tablename__ = "entities"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True)
    state = Column(String(50), nullable=False)
    type = Column(String(100), nullable=False)
    ein = Column(String(20), nullable=True)
    status = Column(SQLEnum(EntityStatus), nullable=False, default=EntityStatus.PLANNED)
    annual_report_due = Column(String(10), nullable=True)  # MM/DD format
    annual_report_fee = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", back_populates="entity")
    transactions = relationship("FinancialTransaction", back_populates="entity")
    
    __table_args__ = (
        Index("idx_entity_status", "status"),
        Index("idx_entity_state", "state"),
    )


class Credential(Base):
    """Professional credential model."""
    __tablename__ = "credentials"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    type = Column(SQLEnum(CredentialType), nullable=False)
    status = Column(SQLEnum(CredentialStatus), nullable=False, default=CredentialStatus.PLANNED)
    issue_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    renewal_due = Column(DateTime, nullable=True)
    required_for = Column(JSON, nullable=True)  # Array of entity names
    cost = Column(Numeric(10, 2), nullable=False, default=0)
    timeline = Column(String(100), nullable=True)
    revenue_potential = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_credential_status", "status"),
        Index("idx_credential_type", "type"),
    )


class Client(Base):
    """Client model."""
    __tablename__ = "clients"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    source = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="active")
    lifetime_value = Column(Numeric(12, 2), nullable=False, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", back_populates="client")
    transactions = relationship("FinancialTransaction", back_populates="client")
    leads = relationship("Lead", back_populates="client")
    
    __table_args__ = (
        Index("idx_client_email", "email"),
        Index("idx_client_status", "status"),
    )


class Project(Base):
    """Project model."""
    __tablename__ = "projects"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(PGUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    entity_id = Column(PGUUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    type = Column(SQLEnum(ProjectType), nullable=False)
    status = Column(SQLEnum(ProjectStatus), nullable=False, default=ProjectStatus.PROSPECT)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    revenue = Column(Numeric(12, 2), nullable=False, default=0)
    margin = Column(Numeric(5, 2), nullable=True)  # Percentage
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="projects")
    entity = relationship("Entity", back_populates="projects")
    
    __table_args__ = (
        Index("idx_project_status", "status"),
        Index("idx_project_type", "type"),
        Index("idx_project_client", "client_id"),
        Index("idx_project_entity", "entity_id"),
    )


class Task(Base):
    """90-day plan task model."""
    __tablename__ = "tasks"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    day_number = Column(Integer, nullable=False)  # 1-90
    description = Column(Text, nullable=False)
    agent_assigned = Column(String(100), nullable=True)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    owner_required = Column(Boolean, nullable=False, default=False)
    estimated_hours = Column(Numeric(5, 2), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    cost = Column(Numeric(10, 2), nullable=False, default=0)
    financial_impact = Column(Numeric(12, 2), nullable=True)
    downstream_dependencies = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_task_day", "day_number"),
        Index("idx_task_status", "status"),
        Index("idx_task_agent", "agent_assigned"),
    )


class FinancialTransaction(Base):
    """Financial transaction model."""
    __tablename__ = "financial_transactions"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    entity_id = Column(PGUUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    client_id = Column(PGUUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    entity = relationship("Entity", back_populates="transactions")
    client = relationship("Client", back_populates="transactions")
    
    __table_args__ = (
        Index("idx_transaction_date", "date"),
        Index("idx_transaction_type", "type"),
        Index("idx_transaction_entity", "entity_id"),
    )


class Lead(Base):
    """Lead model."""
    __tablename__ = "leads"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = Column(PGUUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)
    source = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    score = Column(Integer, nullable=True)  # 1-100
    status = Column(SQLEnum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    assigned_to = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="leads")
    
    __table_args__ = (
        Index("idx_lead_status", "status"),
        Index("idx_lead_source", "source"),
        Index("idx_lead_score", "score"),
    )


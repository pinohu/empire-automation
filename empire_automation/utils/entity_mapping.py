"""
Utility functions for entity and client mapping.

Used by webhook handlers to map services to entities and find clients by name.
"""

import logging
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from empire_automation.database.models import Entity, Client

logger = logging.getLogger(__name__)


def map_service_to_entity(service: str, db: Session) -> Optional[UUID]:
    """
    Map a service type to an entity ID.
    
    Args:
        service: Service type (e.g., "TC", "mortgage", "tax", "notary")
        db: Database session
        
    Returns:
        Entity UUID if found, None otherwise
    """
    if not service:
        return None
    
    # Service to entity name mapping
    service_entity_map = {
        "TC": "Keystone Transaction Specialists",
        "transaction_coordination": "Keystone Transaction Specialists",
        "mortgage": "Keystone Transaction Specialists",
        "tax": "Keystone Tax Services",
        "notary": "Keystone Notary Services",
        "ux_consulting": "Keystone UX Consulting",
    }
    
    # Try to find entity by mapped name
    entity_name = service_entity_map.get(service)
    if entity_name:
        entity = db.query(Entity).filter(Entity.name == entity_name).first()
        if entity:
            logger.info(f"Mapped service '{service}' to entity '{entity_name}' ({entity.id})")
            return entity.id
    
    # Try to find entity by service type in entity name
    entity = db.query(Entity).filter(
        Entity.name.ilike(f"%{service}%")
    ).first()
    
    if entity:
        logger.info(f"Mapped service '{service}' to entity '{entity.name}' ({entity.id})")
        return entity.id
    
    # Default to first active entity if no match found
    default_entity = db.query(Entity).filter(
        Entity.status == "active"
    ).first()
    
    if default_entity:
        logger.warning(f"No entity match for service '{service}', using default: {default_entity.name}")
        return default_entity.id
    
    logger.error(f"No entity found for service '{service}' and no default entity available")
    return None


def map_service_to_entity_name(service: str, db: Session) -> str:
    """
    Map a service type to an entity name for display purposes.
    
    Args:
        service: Service type
        db: Database session
        
    Returns:
        Entity name string
    """
    entity_id = map_service_to_entity(service, db)
    if entity_id:
        entity = db.query(Entity).filter(Entity.id == entity_id).first()
        if entity:
            return entity.name
    
    # Fallback to service-based name
    service_entity_map = {
        "TC": "Keystone Transaction Specialists",
        "transaction_coordination": "Keystone Transaction Specialists",
        "mortgage": "Keystone Transaction Specialists",
        "tax": "Keystone Tax Services",
        "notary": "Keystone Notary Services",
        "ux_consulting": "Keystone UX Consulting",
    }
    
    return service_entity_map.get(service, "Unknown Entity")


def find_client_by_name(name: str, db: Session) -> Optional[UUID]:
    """
    Find a client by name (case-insensitive partial match).
    
    Args:
        name: Client name to search for
        db: Database session
        
    Returns:
        Client UUID if found, None otherwise
    """
    if not name:
        return None
    
    client = db.query(Client).filter(
        Client.name.ilike(f"%{name}%")
    ).first()
    
    if client:
        logger.info(f"Found client '{name}' -> {client.id}")
        return client.id
    
    logger.warning(f"Client not found: {name}")
    return None


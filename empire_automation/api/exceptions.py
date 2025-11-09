"""
Custom exceptions for the API.
"""

from fastapi import HTTPException, status


class EntityNotFoundError(HTTPException):
    """Entity not found exception."""
    def __init__(self, entity_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entity not found: {entity_id}"
        )


class ClientNotFoundError(HTTPException):
    """Client not found exception."""
    def __init__(self, client_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client not found: {client_id}"
        )


class ValidationError(HTTPException):
    """Validation error exception."""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {message}"
        )


class ServiceUnavailableError(HTTPException):
    """External service unavailable exception."""
    def __init__(self, service_name: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {service_name}"
        )


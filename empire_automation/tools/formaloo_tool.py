"""
Formaloo API integration tool.

Provides methods to interact with Formaloo for form creation,
sending forms, retrieving responses, and workflow management.
"""

import os
import logging
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class FormalooTool:
    """
    Tool for interacting with Formaloo API.
    
    Handles forms, responses, and workflows.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Formaloo tool.
        
        Args:
            api_key: Formaloo API key (from env if not provided)
            base_url: Base URL for Formaloo API (from env if not provided)
        """
        self.api_key = api_key or os.getenv("FORMALOO_API_KEY")
        self.api_secret = os.getenv("FORMALOO_API_SECRET")
        self.base_url = base_url or os.getenv(
            "FORMALOO_BASE_URL",
            "https://api.formaloo.com/v1"
        )
        
        if not self.api_key:
            logger.warning("FORMALOO_API_KEY not set. Formaloo features will be disabled.")
            self.session = None
        else:
            self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Formaloo may use API key + secret for authentication
        if self.api_secret:
            session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "X-API-Secret": self.api_secret,
                "Content-Type": "application/json"
            })
        else:
            session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
        
        return session
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make API request to Formaloo."""
        if not self.session:
            logger.warning("Formaloo not configured")
            return None
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Formaloo API error: {e}")
            return None
    
    def create_form(self, form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new form in Formaloo.
        
        Args:
            form_data: Form configuration (title, fields, settings, etc.)
            
        Returns:
            Form data if successful
        """
        result = self._make_request("POST", "/forms", data=form_data)
        if result:
            logger.info(f"Form created: {form_data.get('title')}")
        return result
    
    def send_form(
        self,
        email: str,
        form_id: str,
        custom_message: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Send a form to an email address.
        
        Args:
            email: Recipient email address
            form_id: Form ID to send
            custom_message: Custom message to include
            
        Returns:
            Send confirmation if successful
        """
        data = {
            "email": email,
            "form_id": form_id,
            "message": custom_message
        }
        
        result = self._make_request("POST", "/forms/send", data=data)
        if result:
            logger.info(f"Form {form_id} sent to {email}")
        return result
    
    def get_responses(
        self,
        form_id: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get form responses.
        
        Args:
            form_id: Form ID
            filters: Filter parameters (date_range, status, etc.)
            
        Returns:
            List of form responses
        """
        params = {"form_id": form_id}
        if filters:
            params.update(filters)
        
        result = self._make_request("GET", "/responses", params=params)
        return result.get("data", []) if result else []
    
    def create_workflow(self, workflow_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a workflow in Formaloo.
        
        Args:
            workflow_data: Workflow configuration (triggers, actions, etc.)
            
        Returns:
            Workflow data if successful
        """
        result = self._make_request("POST", "/workflows", data=workflow_data)
        if result:
            logger.info(f"Workflow created: {workflow_data.get('name')}")
        return result


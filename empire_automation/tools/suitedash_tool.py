"""
SuiteDash API integration tool.

Provides methods to interact with SuiteDash for client management,
project tracking, invoicing, and task management.
"""

import os
import logging
import time
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class SuiteDashTool:
    """
    Tool for interacting with SuiteDash API.
    
    Handles clients, projects, tasks, invoices, and more.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize SuiteDash tool.
        
        Args:
            api_key: SuiteDash API key (from env if not provided)
            base_url: Base URL for SuiteDash API (from env if not provided)
        """
        self.api_key = api_key or os.getenv("SUITEDASH_API_KEY")
        self.api_auth_credential = os.getenv("SUITEDASH_API_AUTH_CREDENTIAL")
        self.base_url = base_url or os.getenv(
            "SUITEDASH_BASE_URL",
            "https://api.suitedash.com/v1"
        )
        
        if not self.api_key:
            logger.warning("SUITEDASH_API_KEY not set. SuiteDash features will be disabled.")
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
        
        # SuiteDash may use different auth methods
        if self.api_auth_credential:
            session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "X-API-Auth-Credential": self.api_auth_credential,
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
        """Make API request to SuiteDash."""
        if not self.session:
            logger.warning("SuiteDash not configured")
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
            logger.error(f"SuiteDash API error: {e}")
            return None
    
    def create_client(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        source: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new client in SuiteDash.
        
        Args:
            name: Client name
            email: Client email
            phone: Client phone
            source: Lead source
            
        Returns:
            Client data if successful
        """
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "source": source
        }
        
        result = self._make_request("POST", "/clients", data=data)
        if result:
            logger.info(f"Client created in SuiteDash: {name}")
        return result
    
    def get_clients(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get clients from SuiteDash with optional filters.
        
        Args:
            filters: Filter parameters
            
        Returns:
            List of clients
        """
        result = self._make_request("GET", "/clients", params=filters)
        return result.get("data", []) if result else []
    
    def create_project(
        self,
        client_id: str,
        name: str,
        project_type: Optional[str] = None,
        budget: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new project in SuiteDash.
        
        Args:
            client_id: SuiteDash client ID
            name: Project name
            project_type: Type of project
            budget: Project budget
            
        Returns:
            Project data if successful
        """
        data = {
            "client_id": client_id,
            "name": name,
            "type": project_type,
            "budget": budget
        }
        
        result = self._make_request("POST", "/projects", data=data)
        if result:
            logger.info(f"Project created in SuiteDash: {name}")
        return result
    
    def add_task_to_project(
        self,
        project_id: str,
        task_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Add a task to a project.
        
        Args:
            project_id: SuiteDash project ID
            task_data: Task information (title, description, due_date, etc.)
            
        Returns:
            Task data if successful
        """
        data = {
            "project_id": project_id,
            **task_data
        }
        
        result = self._make_request("POST", "/tasks", data=data)
        if result:
            logger.info(f"Task added to project {project_id}")
        return result
    
    def create_invoice(
        self,
        client_id: str,
        items: List[Dict[str, Any]],
        due_date: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create an invoice in SuiteDash.
        
        Args:
            client_id: SuiteDash client ID
            items: List of invoice items (description, quantity, price)
            due_date: Invoice due date (ISO format)
            
        Returns:
            Invoice data if successful
        """
        data = {
            "client_id": client_id,
            "items": items,
            "due_date": due_date
        }
        
        result = self._make_request("POST", "/invoices", data=data)
        if result:
            logger.info(f"Invoice created for client {client_id}")
        return result
    
    def get_projects(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get projects from SuiteDash.
        
        Args:
            status: Filter by status (active, completed, etc.)
            
        Returns:
            List of projects
        """
        params = {}
        if status:
            params["status"] = status
        
        result = self._make_request("GET", "/projects", params=params)
        return result.get("data", []) if result else []
    
    def update_project_status(
        self,
        project_id: str,
        status: str
    ) -> Optional[Dict[str, Any]]:
        """
        Update project status.
        
        Args:
            project_id: SuiteDash project ID
            status: New status
            
        Returns:
            Updated project data if successful
        """
        data = {"status": status}
        
        result = self._make_request("PUT", f"/projects/{project_id}", data=data)
        if result:
            logger.info(f"Project {project_id} status updated to {status}")
        return result


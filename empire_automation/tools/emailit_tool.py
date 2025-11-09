"""
Emailit API integration tool.

Provides methods to interact with Emailit for email sending,
sequence management, and email statistics.
"""

import os
import logging
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class EmailitTool:
    """
    Tool for interacting with Emailit API.
    
    Handles email sending, sequences, and statistics.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Emailit tool.
        
        Args:
            api_key: Emailit API key (from env if not provided)
            base_url: Base URL for Emailit API (from env if not provided)
        """
        self.api_key = api_key or os.getenv("EMAILIT_API_KEY")
        self.base_url = base_url or os.getenv(
            "EMAILIT_BASE_URL",
            "https://api.emailit.com/v1"
        )
        
        if not self.api_key:
            logger.warning("EMAILIT_API_KEY not set. Emailit features will be disabled.")
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
        """Make API request to Emailit."""
        if not self.session:
            logger.warning("Emailit not configured")
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
            logger.error(f"Emailit API error: {e}")
            return None
    
    def send_email(
        self,
        to: str,
        template_id: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        subject: Optional[str] = None,
        body: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Send email via Emailit.
        
        Args:
            to: Recipient email address
            template_id: Template ID to use
            variables: Template variables
            subject: Email subject (if not using template)
            body: Email body (if not using template)
            
        Returns:
            Email send confirmation if successful
        """
        data = {
            "to": to,
            "template_id": template_id,
            "variables": variables or {},
            "subject": subject,
            "body": body
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        result = self._make_request("POST", "/send", data=data)
        if result:
            logger.info(f"Email sent to {to}")
        return result
    
    def create_sequence(self, sequence_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create an email sequence.
        
        Args:
            sequence_data: Sequence information (name, emails, delays, etc.)
            
        Returns:
            Sequence data if successful
        """
        result = self._make_request("POST", "/sequences", data=sequence_data)
        if result:
            logger.info(f"Email sequence created: {sequence_data.get('name')}")
        return result
    
    def add_to_sequence(
        self,
        email: str,
        sequence_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Add an email address to a sequence.
        
        Args:
            email: Email address to add
            sequence_id: Sequence ID
            
        Returns:
            Confirmation if successful
        """
        data = {
            "email": email,
            "sequence_id": sequence_id
        }
        
        result = self._make_request("POST", "/sequences/add", data=data)
        if result:
            logger.info(f"Added {email} to sequence {sequence_id}")
        return result
    
    def remove_from_sequence(
        self,
        email: str,
        sequence_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Remove an email address from a sequence.
        
        Args:
            email: Email address to remove
            sequence_id: Sequence ID
            
        Returns:
            Confirmation if successful
        """
        data = {
            "email": email,
            "sequence_id": sequence_id
        }
        
        result = self._make_request("POST", "/sequences/remove", data=data)
        if result:
            logger.info(f"Removed {email} from sequence {sequence_id}")
        return result
    
    def get_email_stats(self, email_id: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a sent email.
        
        Args:
            email_id: Email ID
            
        Returns:
            Email statistics (opens, clicks, bounces, etc.)
        """
        result = self._make_request("GET", f"/emails/{email_id}/stats")
        return result


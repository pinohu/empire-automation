"""
Brilliant Directories API integration tool.

Provides methods to interact with Brilliant Directories for
member management, listing updates, and SEO content generation.
"""

import os
import logging
from typing import Dict, Any, Optional, List
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class BrilliantDirectoriesTool:
    """
    Tool for interacting with Brilliant Directories API.
    
    Handles members, listings, SEO content, and payments.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize Brilliant Directories tool.
        
        Args:
            api_key: Brilliant Directories API key (from env if not provided)
            base_url: Base URL for API (from env if not provided)
        """
        self.api_key = api_key or os.getenv("BRILLIANT_DIRECTORIES_API_KEY")
        self.base_url = base_url or os.getenv(
            "BRILLIANT_DIRECTORIES_BASE_URL",
            "https://api.brilliantdirectories.com/v1"
        )
        
        if not self.api_key:
            logger.warning("BRILLIANT_DIRECTORIES_API_KEY not set. Brilliant Directories features will be disabled.")
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
        """Make API request to Brilliant Directories."""
        if not self.session:
            logger.warning("Brilliant Directories not configured")
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
            logger.error(f"Brilliant Directories API error: {e}")
            return None
    
    def add_member(
        self,
        directory_id: str,
        member_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Add a new member to a directory.
        
        Args:
            directory_id: Directory ID
            member_data: Member information (name, email, phone, etc.)
            
        Returns:
            Member data if successful
        """
        data = {
            "directory_id": directory_id,
            **member_data
        }
        
        result = self._make_request("POST", "/members", data=data)
        if result:
            logger.info(f"Member added to directory {directory_id}")
        return result
    
    def update_listing(
        self,
        listing_id: str,
        content: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update a directory listing.
        
        Args:
            listing_id: Listing ID
            content: Updated content (title, description, images, etc.)
            
        Returns:
            Updated listing data if successful
        """
        result = self._make_request("PUT", f"/listings/{listing_id}", data=content)
        if result:
            logger.info(f"Listing {listing_id} updated")
        return result
    
    def generate_seo_content(
        self,
        business_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate SEO-optimized content for a business listing.
        
        Args:
            business_data: Business information (name, category, location, etc.)
            
        Returns:
            Generated SEO content (title, description, keywords, etc.)
        """
        # This would typically call an AI service or use templates
        # For now, returns structured content
        
        content = {
            "title": f"{business_data.get('name', 'Business')} - {business_data.get('category', 'Service')}",
            "description": f"Find {business_data.get('name', 'business')} in {business_data.get('location', 'your area')}. {business_data.get('description', '')}",
            "keywords": f"{business_data.get('name')}, {business_data.get('category')}, {business_data.get('location')}",
            "meta_description": f"{business_data.get('description', '')[:160]}"
        }
        
        logger.info(f"SEO content generated for {business_data.get('name')}")
        return content
    
    def get_members(
        self,
        directory_id: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get members from a directory.
        
        Args:
            directory_id: Directory ID
            filters: Filter parameters (status, tier, etc.)
            
        Returns:
            List of members
        """
        params = {"directory_id": directory_id}
        if filters:
            params.update(filters)
        
        result = self._make_request("GET", "/members", params=params)
        return result.get("data", []) if result else []
    
    def process_payment(
        self,
        member_id: str,
        amount: float,
        payment_method: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Process payment for a directory member.
        
        Args:
            member_id: Member ID
            amount: Payment amount
            payment_method: Payment method (credit_card, paypal, etc.)
            
        Returns:
            Payment confirmation if successful
        """
        data = {
            "member_id": member_id,
            "amount": amount,
            "payment_method": payment_method or "credit_card"
        }
        
        result = self._make_request("POST", "/payments", data=data)
        if result:
            logger.info(f"Payment processed for member {member_id}: ${amount}")
        return result


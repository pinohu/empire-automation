"""
AgenticFlow API integration tool.

Provides methods to interact with AgenticFlow agents for task execution,
daily briefings, and task delegation.
"""

import os
import logging
import time
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class AgenticFlowTool:
    """
    Tool for interacting with AgenticFlow API.
    
    Handles agent calls, daily briefings, task delegation, and status checks.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.agenticflow.com/v1"):
        """
        Initialize AgenticFlow tool.
        
        Args:
            api_key: AgenticFlow API key (from env if not provided)
            base_url: Base URL for AgenticFlow API
        """
        self.api_key = api_key or os.getenv("AGENTICFLOW_API_KEY")
        if not self.api_key:
            raise ValueError("AGENTICFLOW_API_KEY environment variable is required")
        
        self.base_url = base_url
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        
        return session
    
    def call_agent(
        self,
        agent_id: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make API call to AgenticFlow agent.
        
        Args:
            agent_id: ID of the agent to call
            prompt: Prompt/question for the agent
            context: Additional context data to pass
            
        Returns:
            Agent response dictionary
            
        Raises:
            requests.RequestException: If API call fails
        """
        url = f"{self.base_url}/agents/{agent_id}/execute"
        
        payload = {
            "prompt": prompt,
            "context": context or {}
        }
        
        try:
            logger.info(f"Calling agent {agent_id} with prompt: {prompt[:100]}...")
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Agent {agent_id} responded successfully")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling agent {agent_id}: {e}")
            raise
    
    def get_daily_briefing(self, day_number: int, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get daily briefing from Master Orchestrator agent.
        
        Args:
            day_number: Current day in 90-day plan
            context: Additional context (financial data, tasks, etc.)
            
        Returns:
            Formatted daily briefing
        """
        master_orchestrator_id = os.getenv("AGENTICFLOW_MASTER_ORCHESTRATOR_ID", "master-orchestrator")
        
        prompt = f"""Generate daily briefing for Day {day_number} of 90-day plan.

Include:
- Completed yesterday
- Today's plan with agent assignments
- Action required from owner
- Financial snapshot
- Progress toward $10M goal
- Bottlenecks/decisions

Current context:
{self._format_context(context or {})}
"""
        
        try:
            result = self.call_agent(master_orchestrator_id, prompt, context)
            return result
        except Exception as e:
            logger.error(f"Error getting daily briefing: {e}")
            # Return fallback briefing
            return {
                "day_number": day_number,
                "status": "error",
                "message": f"Could not generate briefing: {str(e)}",
                "fallback": True
            }
    
    def delegate_task(
        self,
        agent_id: str,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Delegate specific task to an agent.
        
        Args:
            agent_id: ID of agent to delegate to
            task_data: Task information (description, priority, etc.)
            
        Returns:
            Task execution result
        """
        prompt = f"""Execute the following task:

Task: {task_data.get('description', 'No description')}
Priority: {task_data.get('priority', 'normal')}
Deadline: {task_data.get('deadline', 'Not specified')}
Additional context: {task_data.get('context', {})}

Please execute this task and provide status updates.
"""
        
        try:
            result = self.call_agent(agent_id, prompt, task_data)
            
            # Log task delegation
            logger.info(f"Task delegated to {agent_id}: {task_data.get('description', 'Unknown')}")
            
            return {
                "agent_id": agent_id,
                "task_id": task_data.get("task_id"),
                "status": "delegated",
                "result": result,
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Error delegating task to {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "status": "error",
                "error": str(e)
            }
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get current status of an agent.
        
        Args:
            agent_id: ID of agent to check
            
        Returns:
            Agent status information
        """
        url = f"{self.base_url}/agents/{agent_id}/status"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting agent status for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "status": "unknown",
                "error": str(e)
            }
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary for prompt."""
        if not context:
            return "No additional context provided."
        
        formatted = []
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                formatted.append(f"{key}: {str(value)}")
            else:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)


# Agent ID constants - all must be explicitly configured
def get_agent_ids() -> dict:
    """Get agent IDs from environment variables. Raises ValueError if any are missing."""
    agent_ids = {
        "master_orchestrator": os.getenv("AGENTICFLOW_MASTER_ORCHESTRATOR_ID"),
        "professional_services": os.getenv("AGENTICFLOW_PROFESSIONAL_SERVICES_ID"),
        "marketing": os.getenv("AGENTICFLOW_MARKETING_ID"),
        "financial": os.getenv("AGENTICFLOW_FINANCIAL_ID"),
        "directory_manager": os.getenv("AGENTICFLOW_DIRECTORY_MANAGER_ID"),
        "entity_compliance": os.getenv("AGENTICFLOW_ENTITY_COMPLIANCE_ID"),
        "client_success": os.getenv("AGENTICFLOW_CLIENT_SUCCESS_ID"),
    }
    
    missing = [key for key, value in agent_ids.items() if not value]
    if missing:
        raise ValueError(
            f"Missing required AgenticFlow agent IDs: {', '.join(missing)}. "
            "Please set all AGENTICFLOW_*_ID environment variables."
        )
    
    return agent_ids

# Lazy-loaded agent IDs
AGENT_IDS = None

def get_agent_id(agent_name: str) -> str:
    """Get a specific agent ID, loading them if needed."""
    global AGENT_IDS
    if AGENT_IDS is None:
        AGENT_IDS = get_agent_ids()
    return AGENT_IDS.get(agent_name)


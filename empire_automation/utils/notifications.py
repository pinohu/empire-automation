"""
Notification utilities for sending alerts to owners.

Supports multiple notification channels: email, logging, and future integrations.
"""

import logging
import os
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def send_owner_notification(
    message: str,
    priority: str = "normal",
    subject: Optional[str] = None,
    channel: Optional[str] = None
) -> bool:
    """
    Send notification to owner.
    
    Args:
        message: Notification message
        priority: Priority level ("low", "normal", "high", "urgent")
        subject: Optional subject line
        channel: Notification channel ("email", "log", "slack", etc.)
        
    Returns:
        True if notification sent successfully, False otherwise
    """
    if not message:
        logger.warning("Empty notification message")
        return False
    
    # Determine channel
    if not channel:
        channel = os.getenv("NOTIFICATION_CHANNEL", "log")
    
    timestamp = datetime.utcnow().isoformat()
    
    # Log notification (always)
    log_level = logging.INFO
    if priority in ["high", "urgent"]:
        log_level = logging.WARNING
    logger.log(log_level, f"[NOTIFICATION] [{priority.upper()}] {message}")
    
    # Send via configured channel
    if channel == "email":
        return _send_email_notification(message, subject or f"Alert: {priority}", priority)
    elif channel == "slack":
        return _send_slack_notification(message, priority)
    elif channel == "log":
        # Already logged above
        return True
    else:
        logger.warning(f"Unknown notification channel: {channel}")
        return False


def _send_email_notification(message: str, subject: str, priority: str) -> bool:
    """Send email notification via Gmail API."""
    try:
        from empire_automation.tools.google_workspace_tool import GoogleWorkspaceTool
        
        google_tool = GoogleWorkspaceTool()
        if not google_tool.gmail_service:
            logger.warning("Gmail service not available for notifications")
            return False
        
        owner_email = os.getenv("OWNER_EMAIL")
        if not owner_email:
            logger.warning("OWNER_EMAIL not configured")
            return False
        
        # Send email via Gmail API
        # Format message with priority indicator
        formatted_message = f"""
        <html>
        <body>
            <h2>Empire Automation Alert</h2>
            <p><strong>Priority:</strong> {priority.upper()}</p>
            <p><strong>Time:</strong> {datetime.utcnow().isoformat()}</p>
            <hr>
            <p>{message}</p>
        </body>
        </html>
        """
        
        success = google_tool.send_email(
            to=owner_email,
            subject=subject,
            body=formatted_message
        )
        
        if success:
            logger.info(f"Email notification sent to {owner_email}: {subject}")
        else:
            logger.warning(f"Failed to send email notification to {owner_email}")
        
        return success
    except Exception as e:
        logger.error(f"Error sending email notification: {e}")
        return False


def _send_slack_notification(message: str, priority: str) -> bool:
    """Send Slack notification via webhook."""
    try:
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not slack_webhook_url:
            logger.warning("SLACK_WEBHOOK_URL not configured")
            return False
        
        import requests
        
        payload = {
            "text": f"[{priority.upper()}] {message}",
            "username": "Empire Automation",
            "icon_emoji": ":robot_face:"
        }
        
        response = requests.post(slack_webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Slack notification sent successfully")
        return True
    except Exception as e:
        logger.error(f"Error sending Slack notification: {e}")
        return False


"""
Google Workspace API integration tool.

Provides methods to interact with Google Sheets, Calendar, Gmail, and Drive.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

logger = logging.getLogger(__name__)


class GoogleWorkspaceTool:
    """
    Tool for interacting with Google Workspace APIs.
    
    Supports Sheets, Calendar, Gmail, and Drive.
    """
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/drive.file'
    ]
    
    def __init__(
        self,
        credentials_file: Optional[str] = None,
        spreadsheet_id: Optional[str] = None
    ):
        """
        Initialize Google Workspace tool.
        
        Args:
            credentials_file: Path to service account JSON file
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        credentials_path_str = credentials_file or os.getenv(
            "GOOGLE_CREDENTIALS_FILE",
            "credentials/google-service-account.json"
        )
        
        # Validate and resolve credentials file path
        try:
            credentials_path = Path(credentials_path_str).resolve()
            # Prevent path traversal attacks - ensure path is within project directory
            project_root = Path(__file__).parent.parent.parent.resolve()
            if not str(credentials_path).startswith(str(project_root)):
                raise ValueError(f"Credentials file path must be within project directory: {project_root}")
            
            if not credentials_path.exists():
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
            
            self.credentials_file = str(credentials_path)
        except (ValueError, FileNotFoundError) as e:
            logger.warning(f"Invalid credentials file path: {e}")
            logger.warning("Google Workspace features will be disabled")
            self.credentials_file = None
            self.credentials = None
            self.sheets_service = None
            self.calendar_service = None
            self.gmail_service = None
            self.drive_service = None
            return
        
        self.spreadsheet_id = spreadsheet_id or os.getenv("GOOGLE_SHEETS_ID")
        
        if not os.path.exists(self.credentials_file):
            logger.warning(f"Credentials file not found: {self.credentials_file}")
            logger.warning("Google Workspace features will be disabled")
            self.credentials = None
            self.sheets_service = None
            self.calendar_service = None
            self.gmail_service = None
            self.drive_service = None
        else:
            self.credentials = self._load_credentials()
            self.sheets_service = self._build_sheets_service()
            self.calendar_service = self._build_calendar_service()
            self.gmail_service = self._build_gmail_service()
            self.drive_service = self._build_drive_service()
    
    def _load_credentials(self):
        """Load service account credentials."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            logger.info("Google Workspace credentials loaded successfully")
            return credentials
        except Exception as e:
            logger.error(f"Error loading credentials: {e}")
            return None
    
    def _build_sheets_service(self):
        """Build Google Sheets API service."""
        if not self.credentials:
            return None
        try:
            return build('sheets', 'v4', credentials=self.credentials)
        except Exception as e:
            logger.error(f"Error building Sheets service: {e}")
            return None
    
    def _build_calendar_service(self):
        """Build Google Calendar API service."""
        if not self.credentials:
            return None
        try:
            return build('calendar', 'v3', credentials=self.credentials)
        except Exception as e:
            logger.error(f"Error building Calendar service: {e}")
            return None
    
    def _build_gmail_service(self):
        """Build Gmail API service."""
        if not self.credentials:
            return None
        try:
            return build('gmail', 'v1', credentials=self.credentials)
        except Exception as e:
            logger.error(f"Error building Gmail service: {e}")
            return None
    
    def _build_drive_service(self):
        """Build Google Drive API service."""
        if not self.credentials:
            return None
        try:
            return build('drive', 'v3', credentials=self.credentials)
        except Exception as e:
            logger.error(f"Error building Drive service: {e}")
            return None
    
    # ==================== GOOGLE SHEETS METHODS ====================
    
    def update_revenue(
        self,
        entity: str,
        amount: float,
        service: str,
        client: str,
        date: Optional[date] = None
    ) -> bool:
        """
        Append revenue transaction to Revenue Tracking sheet.
        
        Args:
            entity: Entity name
            amount: Revenue amount
            service: Service type
            client: Client name
            date: Transaction date (defaults to today)
            
        Returns:
            True if successful
        """
        if not self.sheets_service or not self.spreadsheet_id:
            logger.warning("Sheets service not available")
            return False
        
        if date is None:
            date = datetime.now().date()
        
        sheet_name = "Revenue Tracking"
        values = [[
            date.strftime("%Y-%m-%d"),
            entity,
            service,
            amount,
            client,
            "recorded"
        ]]
        
        try:
            body = {"values": values}
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:F",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            
            logger.info(f"Revenue updated: ${amount} for {entity}")
            
            # Update dashboard metrics
            self._update_dashboard_metrics()
            
            return True
        except HttpError as e:
            logger.error(f"Error updating revenue: {e}")
            return False
    
    def update_expense(
        self,
        entity: str,
        amount: float,
        category: str,
        description: str,
        date: Optional[date] = None
    ) -> bool:
        """
        Append expense transaction to Expense Tracking sheet.
        
        Args:
            entity: Entity name
            amount: Expense amount
            category: Expense category
            description: Expense description
            date: Transaction date (defaults to today)
            
        Returns:
            True if successful
        """
        if not self.sheets_service or not self.spreadsheet_id:
            logger.warning("Sheets service not available")
            return False
        
        if date is None:
            date = datetime.now().date()
        
        sheet_name = "Expense Tracking"
        values = [[
            date.strftime("%Y-%m-%d"),
            entity,
            category,
            amount,
            description,
            "recorded"
        ]]
        
        try:
            body = {"values": values}
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:F",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            
            logger.info(f"Expense updated: ${amount} for {entity}")
            
            # Update dashboard metrics
            self._update_dashboard_metrics()
            
            return True
        except HttpError as e:
            logger.error(f"Error updating expense: {e}")
            return False
    
    def update_90_day_progress(
        self,
        day: int,
        tasks_completed: int,
        revenue: float
    ) -> bool:
        """
        Update 90-Day Plan Progress sheet.
        
        Args:
            day: Day number (1-90)
            tasks_completed: Number of tasks completed
            revenue: Revenue impact for the day
            
        Returns:
            True if successful
        """
        if not self.sheets_service or not self.spreadsheet_id:
            logger.warning("Sheets service not available")
            return False
        
        sheet_name = "90-Day Plan Progress"
        today = datetime.now().date()
        
        # Calculate completion percentage (assuming 4 tasks per day average)
        total_tasks = day * 4  # Rough estimate
        completion_pct = (tasks_completed / total_tasks * 100) if total_tasks > 0 else 0
        
        values = [[
            day,
            today.strftime("%Y-%m-%d"),
            tasks_completed,
            "Yes" if tasks_completed > 0 else "No",
            revenue,
            f"{completion_pct:.1f}% complete"
        ]]
        
        try:
            body = {"values": values}
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:F",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            
            logger.info(f"90-day progress updated: Day {day}")
            return True
        except HttpError as e:
            logger.error(f"Error updating 90-day progress: {e}")
            return False
    
    def update_lead_pipeline(
        self,
        name: str,
        source: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        score: int = 0,
        status: str = "new",
        assigned_to: Optional[str] = None,
        date: Optional[date] = None
    ) -> bool:
        """
        Append lead to Lead Pipeline sheet.
        
        Args:
            name: Lead name
            source: Lead source
            email: Lead email (optional)
            phone: Lead phone (optional)
            score: Lead score (0-100)
            status: Lead status
            assigned_to: Assigned to (optional)
            date: Lead date (defaults to today)
            
        Returns:
            True if successful
        """
        if not self.sheets_service or not self.spreadsheet_id:
            logger.warning("Sheets service not available")
            return False
        
        if date is None:
            date = datetime.now().date()
        
        sheet_name = "Lead Pipeline"
        values = [[
            date.strftime("%Y-%m-%d"),
            source,
            name,
            email or "",
            phone or "",
            score,
            status,
            assigned_to or "",
            "active"
        ]]
        
        try:
            body = {"values": values}
            result = self.sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:I",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            
            logger.info(f"Lead added to pipeline: {name} (Score: {score})")
            return True
        except HttpError as e:
            logger.error(f"Error updating lead pipeline: {e}")
            return False
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """
        Get all dashboard metrics from Dashboard Metrics sheet.
        
        Returns:
            Dictionary with dashboard metrics
        """
        if not self.sheets_service or not self.spreadsheet_id:
            logger.warning("Sheets service not available")
            return {}
        
        sheet_name = "Dashboard Metrics"
        
        try:
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:B"
            ).execute()
            
            values = result.get('values', [])
            metrics = {}
            
            for row in values:
                if len(row) >= 2:
                    key = row[0].strip()
                    value = row[1].strip()
                    metrics[key] = value
            
            return metrics
        except HttpError as e:
            logger.error(f"Error getting dashboard metrics: {e}")
            return {}
    
    def _update_dashboard_metrics(self):
        """Update dashboard metrics calculations."""
        # This would recalculate totals, percentages, etc.
        # Implementation depends on specific formulas in the sheet
        pass
    
    # ==================== GOOGLE CALENDAR METHODS ====================
    
    def schedule_meeting(
        self,
        title: str,
        start: datetime,
        end: datetime,
        attendees: List[str],
        description: str = "",
        calendar_id: str = "primary"
    ) -> Optional[str]:
        """
        Create calendar event and send invites.
        
        Args:
            title: Meeting title
            start: Start datetime
            end: End datetime
            attendees: List of email addresses
            description: Meeting description
            calendar_id: Calendar ID (default: primary)
            
        Returns:
            Event ID if successful, None otherwise
        """
        if not self.calendar_service:
            logger.warning("Calendar service not available")
            return None
        
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'America/New_York',
            },
            'attendees': [{'email': email} for email in attendees],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 15},
                ],
            },
        }
        
        try:
            event = self.calendar_service.events().insert(
                calendarId=calendar_id,
                body=event,
                sendUpdates='all'
            ).execute()
            
            logger.info(f"Meeting scheduled: {title}")
            return event.get('id')
        except HttpError as e:
            logger.error(f"Error scheduling meeting: {e}")
            return None
    
    def check_availability(
        self,
        target_date: date,
        duration_minutes: int = 60,
        calendar_id: str = "primary"
    ) -> List[Dict[str, datetime]]:
        """
        Check available time slots for a given date.
        
        Args:
            target_date: Date to check
            duration_minutes: Duration of meeting in minutes
            calendar_id: Calendar ID to check
            
        Returns:
            List of available time slots
        """
        if not self.calendar_service:
            logger.warning("Calendar service not available")
            return []
        
        # Define business hours (9 AM - 5 PM)
        start_time = datetime.combine(target_date, datetime.min.time().replace(hour=9))
        end_time = datetime.combine(target_date, datetime.min.time().replace(hour=17))
        
        try:
            # Get existing events for the day
            events_result = self.calendar_service.events().list(
                calendarId=calendar_id,
                timeMin=start_time.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Calculate available slots
            available_slots = []
            current_time = start_time
            
            for event in events:
                event_start = datetime.fromisoformat(
                    event['start']['dateTime'].replace('Z', '+00:00')
                ).replace(tzinfo=None)
                
                if current_time + timedelta(minutes=duration_minutes) <= event_start:
                    available_slots.append({
                        'start': current_time,
                        'end': current_time + timedelta(minutes=duration_minutes)
                    })
                
                event_end = datetime.fromisoformat(
                    event['end']['dateTime'].replace('Z', '+00:00')
                ).replace(tzinfo=None)
                current_time = max(current_time, event_end)
            
            # Add remaining time if available
            if current_time + timedelta(minutes=duration_minutes) <= end_time:
                available_slots.append({
                    'start': current_time,
                    'end': current_time + timedelta(minutes=duration_minutes)
                })
            
            return available_slots
        except HttpError as e:
            logger.error(f"Error checking availability: {e}")
            return []
    
    # ==================== GMAIL METHODS ====================
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        template_id: Optional[str] = None
    ) -> bool:
        """
        Send email via Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (HTML or plain text)
            template_id: Optional template ID to use
            
        Returns:
            True if successful
        """
        if not self.gmail_service:
            logger.warning("Gmail service not available")
            return False
        
        # Load template if template_id provided
        if template_id:
            template_body = self._load_email_template(template_id, body)
            if template_body:
                body = template_body
        
        message = self._create_message(to, subject, body)
        
        try:
            message = self.gmail_service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            logger.info(f"Email sent to {to}: {subject}")
            return True
        except HttpError as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def create_draft(
        self,
        to: str,
        subject: str,
        body: str
    ) -> Optional[str]:
        """
        Create email draft for owner review.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            
        Returns:
            Draft ID if successful
        """
        if not self.gmail_service:
            logger.warning("Gmail service not available")
            return None
        
        message = self._create_message(to, subject, body)
        
        try:
            draft = self.gmail_service.users().drafts().create(
                userId='me',
                body={'message': message}
            ).execute()
            
            logger.info(f"Draft created for {to}: {subject}")
            return draft.get('id')
        except HttpError as e:
            logger.error(f"Error creating draft: {e}")
            return None
    
    def _create_message(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Create Gmail message object."""
        import base64
        from email.mime.text import MIMEText
        
        message = MIMEText(body, 'html')
        message['to'] = to
        message['subject'] = subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw_message}
    
    def _load_email_template(self, template_id: str, default_body: str) -> Optional[str]:
        """
        Load email template from knowledge/templates/emails directory or Drive.
        
        Args:
            template_id: Template identifier (filename without extension)
            default_body: Default body to use if template not found
            
        Returns:
            Template body with placeholders replaced, or None if not found
        """
        # First try to load from local templates directory
        try:
            project_root = Path(__file__).parent.parent.parent.resolve()
            templates_dir = project_root / "knowledge" / "templates" / "emails"
            
            # Try common extensions
            for ext in [".md", ".html", ".txt"]:
                template_path = templates_dir / f"{template_id}{ext}"
                if template_path.exists():
                    with open(template_path, "r", encoding="utf-8") as f:
                        template_content = f.read()
                    logger.info(f"Loaded email template: {template_id}")
                    return template_content
        except Exception as e:
            logger.warning(f"Error loading local template {template_id}: {e}")
        
        # Try to load from Google Drive if available
        if self.drive_service:
            try:
                # Search for template file in Drive
                # This would require Drive API implementation
                logger.info(f"Template {template_id} not found locally, would check Drive")
            except Exception as e:
                logger.warning(f"Error loading template from Drive: {e}")
        
        logger.warning(f"Email template {template_id} not found, using default body")
        return None


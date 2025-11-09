# Integration Setup Guide

## ✅ API Server Status

**API is running successfully!**
- Health check: ✅ http://localhost:8000/api/health
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 AgenticFlow Integration

### Created Files:
- ✅ `empire_automation/tools/agenticflow_tool.py` - AgenticFlow API integration
- ✅ Updated `api/routes/daily_briefing.py` - Integrated with AgenticFlow
- ✅ Updated `api/routes/agents.py` - Integrated with AgenticFlow

### Setup Required:

1. **Get AgenticFlow API Key:**
   - Login to AgenticFlow.com
   - Navigate to API settings
   - Generate API key

2. **Set Environment Variable:**
   ```bash
   # In .env file
   AGENTICFLOW_API_KEY=your_api_key_here
   AGENTICFLOW_MASTER_ORCHESTRATOR_ID=master-orchestrator
   AGENTICFLOW_PROFESSIONAL_SERVICES_ID=professional-services
   AGENTICFLOW_MARKETING_ID=marketing-lead-gen
   AGENTICFLOW_FINANCIAL_ID=financial-operations
   AGENTICFLOW_DIRECTORY_MANAGER_ID=directory-manager
   AGENTICFLOW_ENTITY_COMPLIANCE_ID=entity-compliance
   AGENTICFLOW_CLIENT_SUCCESS_ID=client-success
   ```

3. **Create Agents in AgenticFlow:**
   - Follow instructions in Day 3 setup
   - Create all 7 agents with provided configurations
   - Note the agent IDs and update environment variables

### Features:
- ✅ `call_agent()` - Call any AgenticFlow agent
- ✅ `get_daily_briefing()` - Get intelligent daily briefing
- ✅ `delegate_task()` - Delegate tasks to agents
- ✅ `get_agent_status()` - Check agent status
- ✅ Retry logic for API calls
- ✅ Comprehensive error handling
- ✅ Logging for all interactions

## 📊 Google Workspace Integration

### Created Files:
- ✅ `empire_automation/tools/google_workspace_tool.py` - Google Workspace integration

### Setup Required:

1. **Google Cloud Console Setup:**
   - Go to https://console.cloud.google.com
   - Create project: "Empire Automation"
   - Enable APIs:
     - Google Sheets API
     - Google Calendar API
     - Gmail API
     - Google Drive API

2. **Create Service Account:**
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Grant necessary permissions
   - Download JSON credentials
   - Save as `credentials/google-service-account.json`

3. **Share Google Sheet:**
   - Open your "Empire Automation - Financial Tracker" sheet
   - Share with service account email (from JSON file)
   - Give "Editor" permissions

4. **Set Environment Variables:**
   ```bash
   # In .env file
   GOOGLE_CREDENTIALS_FILE=credentials/google-service-account.json
   GOOGLE_SHEETS_ID=your_spreadsheet_id_here
   ```

5. **Install Google Libraries:**
   ```bash
   pip install google-auth google-auth-oauthlib google-api-python-client
   ```

### Features:
- ✅ **Google Sheets:**
  - `update_revenue()` - Record revenue transactions
  - `update_expense()` - Record expenses
  - `update_90_day_progress()` - Update plan progress
  - `get_dashboard_metrics()` - Get dashboard data

- ✅ **Google Calendar:**
  - `schedule_meeting()` - Create calendar events
  - `check_availability()` - Check available time slots

- ✅ **Gmail:**
  - `send_email()` - Send emails via Gmail API
  - `create_draft()` - Create drafts for review

## 🚀 Next Steps

1. **Complete AgenticFlow Setup:**
   - Create agents in AgenticFlow web interface
   - Configure agent IDs in environment variables
   - Test agent communication

2. **Complete Google Workspace Setup:**
   - Set up service account
   - Share spreadsheet
   - Test Google Sheets integration

3. **Test Integrations:**
   ```bash
   # Test daily briefing with AgenticFlow
   curl http://localhost:8000/api/daily-briefing
   
   # Test agent execution
   curl -X POST http://localhost:8000/api/agents/master-orchestrator/execute \
     -H "Content-Type: application/json" \
     -d '{"task_id": "test", "parameters": {"description": "Test task"}}'
   ```

4. **Update API Routes:**
   - Integrate Google Workspace tool into financial routes
   - Add calendar integration to client routes
   - Add email sending to lead routes

## 📝 Notes

- Both integrations gracefully handle missing credentials
- Logging is comprehensive for debugging
- Error handling prevents API crashes
- Fallback responses when services unavailable


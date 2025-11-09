# Empire Automation Setup Guide

## Prerequisites

1. **Docker Desktop** - Must be running before starting services
2. **Python 3.10+** - Already installed
3. **Poetry** - Already installed

## Step 1: Start Docker Services

**IMPORTANT:** Ensure Docker Desktop is running before proceeding.

```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

You should see:
- ✅ n8n running on port 5678
- ✅ PostgreSQL on port 5432  
- ✅ Redis on port 6379

**Access n8n:** http://localhost:5678
- Username: `admin`
- Password: `empire_admin_2024`

## Step 2: Initialize Database

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m empire_automation.database.init_db

# Seed additional data
python -m empire_automation.database.seed_data
```

## Step 3: Google Sheets Setup

Create a Google Sheet named **"Empire Automation - Financial Tracker"** with these sheets:

### Sheet 1: "Revenue Tracking"
Columns: Date | Entity | Service | Amount | Client | Status

### Sheet 2: "Expense Tracking"
Columns: Date | Entity | Category | Amount | Description | Status

### Sheet 3: "90-Day Plan Progress"
Columns: Day | Date | Tasks | Completed | Revenue Impact | Notes

### Sheet 4: "Entity Details"
Rows:
- Empire Holdings LLC (Wyoming)
- Keystone Transaction Specialists LLC
- Commonwealth Mortgage Solutions LLC
- TaxEar LLC
- SubTo TC Directory LLC
- Keystones Capital LLC
- Empire Ventures LLC

### Sheet 5: "Credential Tracker"
Columns: Credential | Status | Issue Date | Expiration | Renewal Due

### Sheet 6: "Lead Pipeline"
Columns: Date | Source | Name | Email | Score | Status | Assigned To

### Sheet 7: "Dashboard Metrics"
Cells:
- Revenue YTD
- Revenue Goal ($10M)
- % to Goal
- Active Projects
- Active Leads
- Day of 90-Day Plan

**Get Google Sheets ID:**
Copy the spreadsheet ID from URL:
```
https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
```

Save this ID in your `.env` file as `GOOGLE_SHEETS_ID`.

## Step 4: Environment Configuration

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Required variables:
- `ANTHROPIC_API_KEY` - Your Anthropic/Claude API key
- `GOOGLE_CLIENT_ID` - Google API OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google API OAuth client secret
- `GOOGLE_SHEETS_ID` - Your Google Sheets spreadsheet ID
- `SUITEDASH_API_KEY` - SuiteDash API key (if available)
- `QUICKBOOKS_API_KEY` - QuickBooks API key (if available)
- `DATABASE_URL` - Default: `sqlite:///empire.db` (or PostgreSQL: `postgresql://empire:empire_dev_password@localhost:5432/empire_automation`)

## Step 5: Verify Setup

```bash
# Check database
python -c "from empire_automation.database.models import Entity, Credential; from empire_automation.database.init_db import get_database_url; from sqlalchemy import create_engine; from sqlalchemy.orm import sessionmaker; engine = create_engine(get_database_url()); Session = sessionmaker(bind=engine); session = Session(); print(f'Entities: {session.query(Entity).count()}'); print(f'Credentials: {session.query(Credential).count()}')"

# Check services
docker-compose ps
```

## Troubleshooting

### Docker Desktop Not Running
Error: `The system cannot find the file specified`
**Solution:** Start Docker Desktop application, then retry `docker-compose up -d`

### Database Connection Issues
If using PostgreSQL, ensure:
1. Docker services are running (`docker-compose ps`)
2. Database URL is correct in `.env`
3. Wait 10-15 seconds after starting services for database to initialize

### Poetry Installation Issues
If Poetry fails due to Rust requirements (tiktoken), use pip instead:
```bash
pip install -r requirements.txt
```

## Next Steps

1. Extract business plan data (use Cursor AI with `@THE_COMPLETE_EMPIRE_NARRATIVE.md`)
2. Build domain agents
3. Configure n8n workflows
4. Set up API endpoints
5. Create Streamlit dashboard


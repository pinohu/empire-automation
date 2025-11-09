# Google Sheets Structure Guide

## Spreadsheet: "Empire Automation - Financial Tracker"

### Sheet 1: Revenue Tracking

| Date | Entity | Service | Amount | Client | Status |
|------|--------|---------|--------|--------|--------|
| 2024-11-11 | Keystone Transaction Specialists | Transaction Coordination | $1,200 | John Doe | Completed |
| 2024-11-12 | TaxEar | Tax Preparation | $1,500 | Jane Smith | In Progress |

**Purpose:** Track all revenue by entity, service type, and client.

### Sheet 2: Expense Tracking

| Date | Entity | Category | Amount | Description | Status |
|------|--------|----------|--------|-------------|--------|
| 2024-11-11 | Empire Holdings | Compliance | $1,456 | Wyoming annual reports | Paid |
| 2024-11-12 | Keystone Transaction Specialists | Software | $99 | Notary Rotary membership | Paid |

**Purpose:** Track all expenses by entity and category.

### Sheet 3: 90-Day Plan Progress

| Day | Date | Tasks | Completed | Revenue Impact | Notes |
|-----|------|-------|-----------|----------------|-------|
| 1 | 2024-11-11 | File Wyoming reports, Start TC cert | 2/4 | $0 | On track |
| 2 | 2024-11-12 | Continue TC modules | 3/5 | $0 | Making progress |

**Purpose:** Track daily progress through the 90-day plan.

### Sheet 4: Entity Details

| Entity Name | State | Type | Status | EIN | Annual Report Due |
|-------------|-------|------|--------|-----|------------------|
| Empire Holdings LLC | Wyoming | Master Holding | Active | | 01/15 |
| Keystone Transaction Specialists LLC | Pennsylvania | Operating | Planned | | |
| Commonwealth Mortgage Solutions LLC | Pennsylvania | Operating | Planned | | |
| TaxEar LLC | Pennsylvania | Operating | Planned | | |
| SubTo TC Directory LLC | Pennsylvania | Operating | Planned | | |
| Keystones Capital LLC | Pennsylvania | Operating | Planned | | |
| Empire Ventures LLC | Pennsylvania | Operating | Planned | | |

**Purpose:** Centralized entity information and compliance tracking.

### Sheet 5: Credential Tracker

| Credential | Status | Issue Date | Expiration | Renewal Due | Cost |
|------------|--------|------------|------------|-------------|------|
| PA Notary Public | Active | 2020-01-15 | 2025-01-15 | 2024-12-15 | $0 |
| SubTo TC Certification | In Progress | | | | $0 |
| PA RE License | Planned | | | | $500 |
| MLO License | Planned | | | | $1,000 |
| EA License | Planned | | | | $1,500 |

**Purpose:** Track all credentials, renewal dates, and costs.

### Sheet 6: Lead Pipeline

| Date | Source | Name | Email | Score | Status | Assigned To |
|------|--------|------|-------|-------|--------|-------------|
| 2024-11-11 | SubTo Community | John Investor | john@email.com | 85 | Qualified | Owner |
| 2024-11-12 | Referral | Jane Buyer | jane@email.com | 70 | Contacted | VA |

**Purpose:** Track leads from all sources with scoring and assignment.

### Sheet 7: Dashboard Metrics

| Metric | Value | Formula/Notes |
|--------|-------|--------------|
| Revenue YTD | $0 | SUM(Revenue Tracking!Amount) |
| Revenue Goal | $10,000,000 | Year 3 target |
| % to Goal | 0.00% | (Revenue YTD / Revenue Goal) * 100 |
| Active Projects | 0 | COUNTIF(Projects!Status, "Active") |
| Active Leads | 0 | COUNTIF(Lead Pipeline!Status, "New") + COUNTIF(Lead Pipeline!Status, "Qualified") |
| Day of 90-Day Plan | 1 | Current day number (1-90) |

**Purpose:** High-level dashboard with key metrics.

## Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create OAuth 2.0 credentials
5. Download credentials JSON
6. Add to `.env`:
   - `GOOGLE_CLIENT_ID` - From credentials JSON
   - `GOOGLE_CLIENT_SECRET` - From credentials JSON
   - `GOOGLE_SHEETS_ID` - From spreadsheet URL

## Spreadsheet ID Location

The spreadsheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
```

Copy the ID between `/d/` and `/edit` and save it as `GOOGLE_SHEETS_ID` in your `.env` file.


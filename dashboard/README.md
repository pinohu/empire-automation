# Empire Automation Dashboard

Streamlit dashboard for monitoring and managing the business empire.

## 🚀 Quick Start

```bash
cd empire-automation
streamlit run dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📊 Pages

### 1. Overview
- Revenue YTD vs $10M goal (progress bar)
- Day X of 90-day plan
- Today's tasks from AgenticFlow
- Active projects count
- Lead pipeline count
- Financial snapshot cards

### 2. 90-Day Plan
- Calendar view of 90 days
- Tasks by day with completion status
- Ahead/behind schedule indicator
- Revenue impact by week

### 3. Financial Dashboard
- Revenue by entity (bar charts)
- P&L table by month
- Cash flow chart
- Margin tracking
- YTD vs goals

### 4. Clients & Projects
- Client list from SuiteDash
- Active project timeline
- Revenue per client
- Project completion rates

### 5. Lead Pipeline
- Funnel visualization
- Conversion rates
- Source performance
- Weekly lead metrics

### 6. Agent Status
- Each agent's current task
- Tasks completed today
- Escalated items
- Agent performance metrics

## 🔧 Features

- ✅ Auto-refresh every 5 minutes
- ✅ Export buttons (CSV)
- ✅ Date range selectors
- ✅ Filters and search
- ✅ Mobile-responsive
- ✅ Real-time data from FastAPI

## 📡 Data Sources

- FastAPI backend: `http://localhost:8000`
- Google Sheets (via API)
- AgenticFlow (for agent status)

## 🎨 Components Used

- `st.metric()` - KPIs
- `st.progress()` - Goal progress bars
- `st.bar_chart()` - Visualizations
- `st.dataframe()` - Data tables
- `st.cache_data()` - Performance optimization

## 🔄 Auto-Refresh

The dashboard automatically refreshes data every 5 minutes. You can also manually refresh using the sidebar button.

## 📥 Export Features

- Export clients to CSV
- Export leads to CSV
- Export transactions to CSV
- Export 90-day plan tasks to CSV


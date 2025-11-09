"""
Overview Dashboard Page

Shows high-level metrics, today's tasks, and key KPIs.
"""

import streamlit as st
import requests
from datetime import date, datetime

API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_daily_briefing():
    """Get daily briefing from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/daily-briefing", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Error fetching briefing: {e}")
    return None


@st.cache_data(ttl=300)
def get_financial_dashboard():
    """Get financial dashboard data."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/financial/dashboard", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def show():
    """Display overview page."""
    st.title("📊 Dashboard Overview")
    
    # Auto-refresh indicator
    placeholder = st.empty()
    with placeholder.container():
        st.info("🔄 Auto-refreshing every 5 minutes...")
    
    # Get data
    briefing = get_daily_briefing()
    financial_data = get_financial_dashboard()
    
    # Header metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if briefing:
            st.metric(
                "Day of 90-Day Plan",
                f"Day {briefing.get('day_number', 0)}",
                delta=f"{90 - briefing.get('day_number', 0)} days remaining"
            )
        else:
            st.metric("Day of 90-Day Plan", "Day 1", delta="89 days remaining")
    
    with col2:
        if financial_data:
            revenue = financial_data.get('total_revenue', 0)
            goal = 10000000
            progress = (revenue / goal * 100) if goal > 0 else 0
            st.metric(
                "Revenue YTD",
                f"${revenue:,.0f}",
                delta=f"{progress:.1f}% to $10M goal"
            )
        else:
            st.metric("Revenue YTD", "$0", delta="0% to $10M goal")
    
    with col3:
        if briefing:
            st.metric(
                "Active Projects",
                briefing.get('metrics', {}).get('active_projects', 0)
            )
        else:
            st.metric("Active Projects", 0)
    
    with col4:
        if briefing:
            st.metric(
                "Active Leads",
                briefing.get('metrics', {}).get('active_leads', 0)
            )
        else:
            st.metric("Active Leads", 0)
    
    st.markdown("---")
    
    # Revenue Progress Bar
    st.subheader("🎯 Progress Toward $10M Goal")
    if financial_data:
        revenue = financial_data.get('total_revenue', 0)
        goal = 10000000
        progress = min((revenue / goal * 100), 100) if goal > 0 else 0
        
        st.progress(progress / 100)
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Current:** ${revenue:,.0f}")
        with col2:
            st.write(f"**Goal:** ${goal:,.0f}")
    else:
        st.progress(0)
        st.write("**Current:** $0 | **Goal:** $10,000,000")
    
    st.markdown("---")
    
    # Today's Tasks
    st.subheader("📋 Today's Tasks")
    
    if briefing:
        tasks_col1, tasks_col2, tasks_col3 = st.columns(3)
        
        with tasks_col1:
            st.metric("Total Tasks", briefing.get('total_tasks', 0))
        with tasks_col2:
            st.metric("Pending", briefing.get('pending_tasks', 0))
        with tasks_col3:
            st.metric("Completed", briefing.get('completed_tasks', 0))
        
        # Priority tasks
        priority_tasks = briefing.get('priority_tasks', [])
        if priority_tasks:
            st.write("**Priority Tasks:**")
            for task in priority_tasks[:5]:  # Show top 5
                st.write(f"- {task.get('description', 'Unknown')} (Priority: {task.get('priority', 'N/A')})")
        else:
            st.info("No priority tasks for today")
    else:
        st.info("Loading tasks...")
    
    st.markdown("---")
    
    # Financial Snapshot
    st.subheader("💰 Financial Snapshot")
    
    if financial_data:
        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        
        with fin_col1:
            st.metric(
                "Total Revenue",
                f"${financial_data.get('total_revenue', 0):,.0f}"
            )
        with fin_col2:
            st.metric(
                "Total Expenses",
                f"${financial_data.get('total_expenses', 0):,.0f}"
            )
        with fin_col3:
            st.metric(
                "Net Profit",
                f"${financial_data.get('net_profit', 0):,.0f}"
            )
        with fin_col4:
            st.metric(
                "Transactions",
                financial_data.get('transaction_count', 0)
            )
    else:
        st.info("No financial data available")
    
    # Note: Auto-refresh is handled by cache TTL (5 minutes)
    # Users can manually refresh using the sidebar button


"""
Streamlit Dashboard - Main Application

Run with: streamlit run dashboard/app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="Empire Automation Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import pages
from dashboard.pages import overview, ninety_day_plan, financial, clients, leads, agents

# Sidebar navigation
st.sidebar.title("🚀 Empire Automation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Overview",
        "📅 90-Day Plan",
        "💰 Financial",
        "👥 Clients & Projects",
        "🎯 Lead Pipeline",
        "🤖 Agent Status"
    ]
)

# Route to selected page
if page == "📊 Overview":
    overview.show()
elif page == "📅 90-Day Plan":
    ninety_day_plan.show()
elif page == "💰 Financial":
    financial.show()
elif page == "👥 Clients & Projects":
    clients.show()
elif page == "🎯 Lead Pipeline":
    leads.show()
elif page == "🤖 Agent Status":
    agents.show()

# Auto-refresh
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Empire Automation v0.1.0**")
st.sidebar.markdown("Dashboard auto-refreshes every 5 minutes")


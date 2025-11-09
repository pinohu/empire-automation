"""
90-Day Plan Dashboard Page

Shows calendar view, task completion, and progress tracking.
"""

import streamlit as st
import requests
from datetime import date, datetime, timedelta
import pandas as pd

API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=300)
def get_plan_progress():
    """Get 90-day plan progress."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/90-day-plan/progress", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


@st.cache_data(ttl=300)
def get_today_tasks():
    """Get today's tasks."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/90-day-plan/today", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []


def show():
    """Display 90-day plan page."""
    st.title("📅 90-Day Plan Progress")
    
    # Get data
    progress = get_plan_progress()
    tasks = get_today_tasks()
    
    # Progress Overview
    col1, col2, col3, col4 = st.columns(4)
    
    if progress:
        with col1:
            st.metric("Total Tasks", progress.get('total_tasks', 0))
        with col2:
            st.metric("Completed", progress.get('completed_tasks', 0))
        with col3:
            st.metric("In Progress", progress.get('in_progress_tasks', 0))
        with col4:
            st.metric("Pending", progress.get('pending_tasks', 0))
        
        # Completion percentage
        completion = progress.get('completion_percentage', 0)
        st.progress(completion / 100)
        st.write(f"**Overall Completion:** {completion:.1f}%")
        
        # Day tracking
        st.markdown("---")
        day_col1, day_col2 = st.columns(2)
        with day_col1:
            st.metric("Current Day", progress.get('current_day', 1))
        with day_col2:
            st.metric("Days Remaining", progress.get('days_remaining', 90))
    else:
        st.info("Loading plan progress...")
    
    st.markdown("---")
    
    # Today's Tasks
    st.subheader("📋 Today's Tasks")
    
    if tasks:
        # Create DataFrame for display
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "Description": task.get('description', 'Unknown'),
                "Status": task.get('status', 'pending'),
                "Agent": task.get('agent_assigned', 'N/A'),
                "Hours": task.get('estimated_hours', 0),
                "Cost": f"${task.get('cost', 0):,.2f}"
            })
        
        df = pd.DataFrame(tasks_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Task status breakdown
        if len(tasks) > 0:
            status_counts = df['Status'].value_counts()
            st.bar_chart(status_counts)
    else:
        st.info("No tasks found for today")
    
    st.markdown("---")
    
    # Calendar View (Simplified)
    st.subheader("📆 Plan Calendar")
    
    # Calculate weeks
    weeks = []
    current_day = 1
    while current_day <= 90:
        week_num = (current_day - 1) // 7 + 1
        week_days = list(range(current_day, min(current_day + 7, 91)))
        weeks.append({
            "Week": week_num,
            "Days": week_days,
            "Tasks": len(week_days) * 4  # Estimate
        })
        current_day += 7
    
    # Display weeks
    for week in weeks[:4]:  # Show first 4 weeks
        with st.expander(f"Week {week['Week']} - Days {week['Days'][0]}-{week['Days'][-1]}"):
            st.write(f"**Days:** {', '.join(map(str, week['Days']))}")
            st.write(f"**Estimated Tasks:** {week['Tasks']}")
    
    # Export button
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export to CSV"):
            if tasks:
                df = pd.DataFrame(tasks)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"90_day_plan_day_{progress.get('current_day', 1) if progress else 1}.csv",
                    mime="text/csv"
                )


"""
Agent Status Dashboard Page

Shows agent activity, tasks, and performance metrics.
"""

import streamlit as st
import requests
from datetime import date, datetime
import pandas as pd

API_BASE_URL = "http://localhost:8000"

# Agent definitions
AGENTS = [
    {"id": "master-orchestrator", "name": "Master Orchestrator", "icon": "🎯"},
    {"id": "professional-services", "name": "Professional Services", "icon": "💼"},
    {"id": "marketing", "name": "Marketing & Lead Gen", "icon": "📢"},
    {"id": "financial", "name": "Financial Operations", "icon": "💰"},
    {"id": "directory-manager", "name": "Directory Manager", "icon": "📁"},
    {"id": "entity-compliance", "name": "Entity Compliance", "icon": "📋"},
    {"id": "client-success", "name": "Client Success", "icon": "✅"},
]


@st.cache_data(ttl=300)
def get_agent_status(agent_id):
    """Get agent status from API."""
    try:
        # This would call AgenticFlow API
        # For now, return placeholder
        return {
            "agent_id": agent_id,
            "status": "active",
            "current_task": "No active task",
            "tasks_completed_today": 0
        }
    except Exception:
        return None


@st.cache_data(ttl=300)
def get_today_tasks():
    """Get today's tasks grouped by agent."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/90-day-plan/today", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []


def show():
    """Display agent status page."""
    st.title("🤖 Agent Status")
    
    # Get data
    tasks = get_today_tasks()
    
    # Group tasks by agent
    tasks_by_agent = {}
    for task in tasks:
        agent = task.get('agent_assigned', 'unassigned')
        if agent not in tasks_by_agent:
            tasks_by_agent[agent] = []
        tasks_by_agent[agent].append(task)
    
    # Agent Cards
    st.subheader("🤖 Agent Overview")
    
    cols = st.columns(3)
    for idx, agent in enumerate(AGENTS):
        col = cols[idx % 3]
        
        with col:
            agent_tasks = tasks_by_agent.get(agent['id'], [])
            completed = len([t for t in agent_tasks if t.get('status') == 'completed'])
            total = len(agent_tasks)
            
            st.metric(
                f"{agent['icon']} {agent['name']}",
                f"{completed}/{total} tasks",
                delta=f"{completed/total*100:.0f}% complete" if total > 0 else "0%"
            )
    
    st.markdown("---")
    
    # Agent Details
    selected_agent = st.selectbox(
        "Select Agent",
        [a['name'] for a in AGENTS]
    )
    
    agent_info = next((a for a in AGENTS if a['name'] == selected_agent), None)
    
    if agent_info:
        st.subheader(f"{agent_info['icon']} {agent_info['name']} Details")
        
        # Get agent status
        status = get_agent_status(agent_info['id'])
        
        if status:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Status:** {status.get('status', 'unknown').upper()}")
            with col2:
                st.write(f"**Tasks Today:** {status.get('tasks_completed_today', 0)}")
            with col3:
                st.write(f"**Current Task:** {status.get('current_task', 'None')}")
        
        # Agent's tasks
        agent_tasks = tasks_by_agent.get(agent_info['id'], [])
        
        if agent_tasks:
            st.write(f"**Assigned Tasks:** {len(agent_tasks)}")
            
            tasks_data = []
            for task in agent_tasks:
                tasks_data.append({
                    "Description": task.get('description', 'Unknown'),
                    "Status": task.get('status', 'pending'),
                    "Hours": task.get('estimated_hours', 0),
                    "Cost": f"${float(task.get('cost', 0)):,.2f}",
                    "Owner Required": "Yes" if task.get('owner_required') else "No"
                })
            
            df_tasks = pd.DataFrame(tasks_data)
            st.dataframe(df_tasks, use_container_width=True, hide_index=True)
        else:
            st.info(f"No tasks assigned to {agent_info['name']}")
    
    st.markdown("---")
    
    # Escalated Items
    st.subheader("⚠️ Escalated Items")
    
    escalated_tasks = [t for t in tasks if t.get('owner_required')]
    
    if escalated_tasks:
        st.warning(f"{len(escalated_tasks)} tasks require owner attention")
        
        escalated_data = []
        for task in escalated_tasks:
            escalated_data.append({
                "Agent": task.get('agent_assigned', 'Unknown'),
                "Description": task.get('description', 'Unknown'),
                "Reason": "Owner action required"
            })
        
        df_escalated = pd.DataFrame(escalated_data)
        st.dataframe(df_escalated, use_container_width=True, hide_index=True)
    else:
        st.success("No escalated items - all agents operating smoothly!")
    
    st.markdown("---")
    
    # Agent Performance Metrics
    st.subheader("📊 Agent Performance")
    
    performance_data = []
    for agent in AGENTS:
        agent_tasks = tasks_by_agent.get(agent['id'], [])
        completed = len([t for t in agent_tasks if t.get('status') == 'completed'])
        total = len(agent_tasks)
        
        performance_data.append({
            "Agent": agent['name'],
            "Total Tasks": total,
            "Completed": completed,
            "Completion Rate": f"{(completed/total*100) if total > 0 else 0:.1f}%"
        })
    
    df_performance = pd.DataFrame(performance_data)
    st.dataframe(df_performance, use_container_width=True, hide_index=True)
    
    # Performance chart
    if performance_data:
        st.bar_chart(df_performance.set_index('Agent')['Completed'])


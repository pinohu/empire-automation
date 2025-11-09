"""
Clients & Projects Dashboard Page

Shows client list, active projects, and project metrics.
"""

import streamlit as st
import requests
from datetime import date, datetime
import pandas as pd

API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=300)
def get_clients():
    """Get clients from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/clients", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []


@st.cache_data(ttl=300)
def get_projects():
    """Get projects from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/projects", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []


def show():
    """Display clients & projects page."""
    st.title("👥 Clients & Projects")
    
    # Get data
    clients = get_clients()
    projects = get_projects()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clients", len(clients))
    with col2:
        active_projects = [p for p in projects if p.get('status') in ['in_progress', 'pending']]
        st.metric("Active Projects", len(active_projects))
    with col3:
        total_revenue = sum(float(p.get('revenue', 0)) for p in projects)
        st.metric("Total Project Revenue", f"${total_revenue:,.0f}")
    with col4:
        if clients:
            avg_ltv = sum(float(c.get('lifetime_value', 0)) for c in clients) / len(clients)
            st.metric("Avg Lifetime Value", f"${avg_ltv:,.0f}")
        else:
            st.metric("Avg Lifetime Value", "$0")
    
    st.markdown("---")
    
    # Clients Table
    st.subheader("👥 Clients")
    
    if clients:
        # Filter and search
        search_term = st.text_input("🔍 Search clients", "")
        
        filtered_clients = clients
        if search_term:
            filtered_clients = [
                c for c in clients
                if search_term.lower() in c.get('name', '').lower()
                or search_term.lower() in c.get('email', '').lower()
            ]
        
        # Status filter
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "lead", "active", "inactive", "churned"]
        )
        
        if status_filter != "All":
            filtered_clients = [c for c in filtered_clients if c.get('status') == status_filter]
        
        # Display clients
        if filtered_clients:
            clients_data = []
            for client in filtered_clients:
                clients_data.append({
                    "Name": client.get('name', 'Unknown'),
                    "Email": client.get('email', 'N/A'),
                    "Phone": client.get('phone', 'N/A'),
                    "Status": client.get('status', 'unknown'),
                    "Source": client.get('source', 'N/A'),
                    "LTV": f"${float(client.get('lifetime_value', 0)):,.2f}"
                })
            
            df_clients = pd.DataFrame(clients_data)
            st.dataframe(df_clients, use_container_width=True, hide_index=True)
            
            # Export
            csv = df_clients.to_csv(index=False)
            st.download_button(
                label="📥 Download Clients CSV",
                data=csv,
                file_name="clients.csv",
                mime="text/csv"
            )
        else:
            st.info("No clients match your filters")
    else:
        st.info("No clients found")
    
    st.markdown("---")
    
    # Projects Table
    st.subheader("📁 Active Projects")
    
    if projects:
        # Filter by status
        project_status = st.selectbox(
            "Filter Projects by Status",
            ["All", "prospect", "pending", "in_progress", "completed", "cancelled"]
        )
        
        filtered_projects = projects
        if project_status != "All":
            filtered_projects = [p for p in projects if p.get('status') == project_status]
        
        if filtered_projects:
            projects_data = []
            for project in filtered_projects:
                projects_data.append({
                    "Type": project.get('type', 'Unknown'),
                    "Status": project.get('status', 'unknown'),
                    "Revenue": f"${float(project.get('revenue', 0)):,.2f}",
                    "Margin": f"{float(project.get('margin', 0)):.1f}%" if project.get('margin') else "N/A",
                    "Start Date": project.get('start_date', 'N/A'),
                    "End Date": project.get('end_date', 'N/A')
                })
            
            df_projects = pd.DataFrame(projects_data)
            st.dataframe(df_projects, use_container_width=True, hide_index=True)
            
            # Project completion rate
            completed = len([p for p in projects if p.get('status') == 'completed'])
            total = len(projects)
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            st.metric("Project Completion Rate", f"{completion_rate:.1f}%")
        else:
            st.info("No projects match your filters")
    else:
        st.info("No projects found")
    
    st.markdown("---")
    
    # Revenue per Client Chart
    st.subheader("💰 Revenue per Client")
    
    if clients and projects:
        # Calculate revenue per client
        client_revenue = {}
        for project in projects:
            # Would need client_id mapping
            pass
        
        st.info("Revenue per client chart will display when client-project mapping is available")
    else:
        st.info("No data available for revenue per client")


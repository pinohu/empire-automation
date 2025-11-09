"""
Lead Pipeline Dashboard Page

Shows lead funnel, conversion rates, and source performance.
"""

import streamlit as st
import requests
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px

API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=300)
def get_leads(status=None):
    """Get leads from API."""
    try:
        params = {}
        if status:
            params['status'] = status
        
        response = requests.get(f"{API_BASE_URL}/api/v1/leads", params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []


def show():
    """Display lead pipeline page."""
    st.title("🎯 Lead Pipeline")
    
    # Get data
    all_leads = get_leads()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_leads = len(all_leads)
    new_leads = len([l for l in all_leads if l.get('status') == 'new'])
    qualified_leads = len([l for l in all_leads if l.get('status') == 'qualified'])
    converted_leads = len([l for l in all_leads if l.get('status') == 'converted'])
    
    with col1:
        st.metric("Total Leads", total_leads)
    with col2:
        st.metric("New Leads", new_leads)
    with col3:
        st.metric("Qualified", qualified_leads)
    with col4:
        st.metric("Converted", converted_leads)
    
    st.markdown("---")
    
    # Lead Funnel
    st.subheader("📊 Lead Funnel")
    
    if all_leads:
        funnel_data = {
            "Stage": ["New", "Contacted", "Qualified", "Converted"],
            "Count": [
                len([l for l in all_leads if l.get('status') == 'new']),
                len([l for l in all_leads if l.get('status') == 'contacted']),
                len([l for l in all_leads if l.get('status') == 'qualified']),
                len([l for l in all_leads if l.get('status') == 'converted'])
            ]
        }
        
        df_funnel = pd.DataFrame(funnel_data)
        st.bar_chart(df_funnel.set_index('Stage'))
        
        # Conversion rates
        st.write("**Conversion Rates:**")
        if new_leads > 0:
            contacted_rate = len([l for l in all_leads if l.get('status') == 'contacted']) / new_leads * 100
            qualified_rate = qualified_leads / new_leads * 100 if new_leads > 0 else 0
            converted_rate = converted_leads / new_leads * 100 if new_leads > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("New → Contacted", f"{contacted_rate:.1f}%")
            with col2:
                st.metric("New → Qualified", f"{qualified_rate:.1f}%")
            with col3:
                st.metric("New → Converted", f"{converted_rate:.1f}%")
    else:
        st.info("No leads found")
    
    st.markdown("---")
    
    # Source Performance
    st.subheader("📈 Lead Sources")
    
    if all_leads:
        # Group by source
        source_counts = {}
        source_scores = {}
        
        for lead in all_leads:
            source = lead.get('source', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
            if source not in source_scores:
                source_scores[source] = []
            source_scores[source].append(lead.get('score', 0))
        
        # Average score per source
        source_avg_score = {
            k: sum(v) / len(v) if v else 0
            for k, v in source_scores.items()
        }
        
        df_sources = pd.DataFrame([
            {
                "Source": k,
                "Count": v,
                "Avg Score": source_avg_score.get(k, 0)
            }
            for k, v in source_counts.items()
        ])
        
        st.bar_chart(df_sources.set_index('Source')['Count'])
        
        # Source table
        st.dataframe(df_sources, use_container_width=True, hide_index=True)
    else:
        st.info("No lead source data available")
    
    st.markdown("---")
    
    # Leads Table
    st.subheader("📋 All Leads")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "new", "contacted", "qualified", "converted", "lost"]
        )
    with col2:
        min_score = st.slider("Minimum Score", 0, 100, 0)
    
    filtered_leads = all_leads
    if status_filter != "All":
        filtered_leads = [l for l in all_leads if l.get('status') == status_filter]
    
    filtered_leads = [l for l in filtered_leads if l.get('score', 0) >= min_score]
    
    if filtered_leads:
        leads_data = []
        for lead in filtered_leads:
            leads_data.append({
                "Name": lead.get('name', 'Unknown'),
                "Email": lead.get('email', 'N/A'),
                "Phone": lead.get('phone', 'N/A'),
                "Source": lead.get('source', 'Unknown'),
                "Score": lead.get('score', 0),
                "Status": lead.get('status', 'unknown'),
                "Assigned To": lead.get('assigned_to', 'N/A')
            })
        
        df_leads = pd.DataFrame(leads_data)
        st.dataframe(df_leads, use_container_width=True, hide_index=True)
        
        # Export
        csv = df_leads.to_csv(index=False)
        st.download_button(
            label="📥 Download Leads CSV",
            data=csv,
            file_name="leads.csv",
            mime="text/csv"
        )
    else:
        st.info("No leads match your filters")


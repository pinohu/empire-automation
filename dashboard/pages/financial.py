"""
Financial Dashboard Page

Shows revenue, expenses, P&L, and financial metrics.
"""

import streamlit as st
import requests
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=300)
def get_financial_dashboard(start_date=None, end_date=None):
    """Get financial dashboard data."""
    try:
        params = {}
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        response = requests.get(
            f"{API_BASE_URL}/api/v1/financial/dashboard",
            params=params,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


@st.cache_data(ttl=300)
def get_transactions(entity_id=None, start_date=None, end_date=None):
    """Get financial transactions."""
    try:
        params = {}
        if entity_id:
            params['entity_id'] = entity_id
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        response = requests.get(
            f"{API_BASE_URL}/api/v1/financial/transactions",
            params=params,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []


def show():
    """Display financial dashboard page."""
    st.title("💰 Financial Dashboard")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    # Get data
    financial_data = get_financial_dashboard(start_date, end_date)
    transactions = get_transactions(start_date=start_date, end_date=end_date)
    
    # Key Metrics
    st.subheader("📊 Key Metrics")
    
    if financial_data:
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(
                "Total Revenue",
                f"${financial_data.get('total_revenue', 0):,.0f}"
            )
        with metric_col2:
            st.metric(
                "Total Expenses",
                f"${financial_data.get('total_expenses', 0):,.0f}"
            )
        with metric_col3:
            net_profit = financial_data.get('net_profit', 0)
            st.metric(
                "Net Profit",
                f"${net_profit:,.0f}",
                delta=f"{(net_profit/financial_data.get('total_revenue', 1)*100) if financial_data.get('total_revenue', 0) > 0 else 0:.1f}% margin"
            )
        with metric_col4:
            st.metric(
                "Transactions",
                financial_data.get('transaction_count', 0)
            )
    else:
        st.info("No financial data available")
    
    st.markdown("---")
    
    # Revenue by Entity
    st.subheader("📈 Revenue by Entity")
    
    if financial_data and financial_data.get('revenue_by_entity'):
        entity_revenue = financial_data['revenue_by_entity']
        if entity_revenue:
            df_entities = pd.DataFrame([
                {"Entity": k, "Revenue": v}
                for k, v in entity_revenue.items()
            ])
            st.bar_chart(df_entities.set_index('Entity'))
        else:
            st.info("No entity revenue data available")
    else:
        st.info("Loading entity revenue data...")
    
    # Expense by Category
    st.subheader("💸 Expenses by Category")
    
    if financial_data and financial_data.get('expense_by_category'):
        category_expenses = financial_data['expense_by_category']
        if category_expenses:
            df_categories = pd.DataFrame([
                {"Category": k, "Amount": v}
                for k, v in category_expenses.items()
            ])
            st.bar_chart(df_categories.set_index('Category'))
        else:
            st.info("No category expense data available")
    else:
        st.info("Loading expense data...")
    
    st.markdown("---")
    
    # Transactions Table
    st.subheader("📋 Recent Transactions")
    
    if transactions:
        # Prepare transaction data
        trans_data = []
        for trans in transactions[:50]:  # Show last 50
            trans_data.append({
                "Date": trans.get('date', ''),
                "Entity": "Unknown",  # Would need entity lookup
                "Type": trans.get('type', ''),
                "Amount": f"${float(trans.get('amount', 0)):,.2f}",
                "Category": trans.get('category', 'N/A'),
                "Description": trans.get('description', '')[:50]
            })
        
        df_trans = pd.DataFrame(trans_data)
        st.dataframe(df_trans, use_container_width=True, hide_index=True)
        
        # Export button
        csv = df_trans.to_csv(index=False)
        st.download_button(
            label="📥 Download Transactions CSV",
            data=csv,
            file_name=f"transactions_{start_date}_{end_date}.csv",
            mime="text/csv"
        )
    else:
        st.info("No transactions found")
    
    # P&L Chart
    st.markdown("---")
    st.subheader("📊 Profit & Loss Trend")
    
    # This would show monthly P&L if we had historical data
    st.info("P&L trend chart will display when historical data is available")


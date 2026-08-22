"""
Personal Expense Tracker - Professional Streamlit Application
A clean, intuitive expense tracking solution with powerful analytics.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import uuid

# Page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional color scheme
COLORS = {
    'primary': '#2563EB',
    'secondary': '#64748B',
    'background': '#F8FAFC',
    'card': '#FFFFFF',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'text': '#1E293B',
    'muted': '#64748B',
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# Custom CSS for professional look
st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Compact Header styles */
    .compact-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .compact-header .title-section h1 {
        color: white;
        font-size: 1.6rem;
        margin: 0;
        font-weight: 700;
    }
    
    .compact-header .title-section p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.9rem;
        margin: 0;
    }
    
    .compact-header .date-section {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
        text-align: right;
    }
    
    /* Card styles */
    .metric-card {
        background: white;
        padding: 1.25rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
        transition: all 0.2s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .metric-label {
        font-size: 0.8rem;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1E293B;
        line-height: 1.2;
    }
    
    .metric-sub {
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 0.25rem;
    }
    
    .metric-positive {
        color: #10B981;
    }
    
    .metric-negative {
        color: #EF4444;
    }
    
    /* Navigation styles */
    .nav-container {
        background: white;
        border-radius: 0.75rem;
        padding: 0.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
        display: flex;
        gap: 0.25rem;
        border: 1px solid #f0f0f0;
    }
    
    .nav-item {
        flex: 1;
        padding: 0.6rem 0.5rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 500;
        color: #64748B;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        background: transparent;
        white-space: nowrap;
    }
    
    .nav-item:hover {
        background: #F1F5F9;
        color: #1E293B;
    }
    
    .nav-item.active {
        background: #2563EB;
        color: white;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.75rem;
    }
    
    .section-subheader {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 1rem;
    }
    
    /* Table styles */
    .stDataFrame {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Button styles */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Form styles */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {
        border-color: #2563EB;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Alert styles */
    .stAlert {
        border-radius: 0.5rem;
        border-left: 4px solid;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #F1F5F9;
    }
    
    /* Budget progress */
    .budget-progress {
        background: #F1F5F9;
        border-radius: 99px;
        height: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .budget-progress-bar {
        height: 100%;
        border-radius: 99px;
        transition: width 0.6s ease;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 2rem;
        color: #94A3B8;
    }
    
    .empty-state .empty-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .empty-state .empty-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .compact-header {
            flex-direction: column;
            text-align: center;
            padding: 1rem;
        }
        
        .compact-header .date-section {
            text-align: center;
            margin-top: 0.5rem;
        }
        
        .nav-item {
            font-size: 0.7rem;
            padding: 0.4rem 0.25rem;
        }
        
        .metric-value {
            font-size: 1.25rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


class ExpenseManager:
    """Core expense management logic."""
    
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.categories = [
            "Food & Dining", "Transportation", "Shopping", 
            "Entertainment", "Utilities", "Healthcare", 
            "Education", "Other"
        ]
        self.budget = 10000  # Default monthly budget
        self.load_expenses()
        self.load_budget()
    
    def load_expenses(self):
        """Load expenses from JSON file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.expenses = data.get('expenses', [])
                    # Ensure all expenses have unique IDs
                    for exp in self.expenses:
                        if 'id' not in exp:
                            exp['id'] = str(uuid.uuid4())[:8]
        except Exception:
            self.expenses = []
    
    def save_expenses(self):
        """Save expenses to JSON file."""
        try:
            data = {
                'expenses': self.expenses,
                'budget': self.budget
            }
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4, default=str)
            return True
        except Exception as e:
            st.error(f"Failed to save: {str(e)}")
            return False
    
    def load_budget(self):
        """Load budget from file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.budget = data.get('budget', 10000)
        except Exception:
            self.budget = 10000
    
    def add_expense(self, amount, category, description, date):
        """Add a new expense record."""
        expense = {
            "id": str(uuid.uuid4())[:8],
            "amount": round(float(amount), 2),
            "category": category,
            "description": description or "No description",
            "date": date.strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat()
        }
        self.expenses.append(expense)
        return self.save_expenses()
    
    def update_expense(self, expense_id, amount, category, description, date):
        """Update an existing expense."""
        for expense in self.expenses:
            if expense['id'] == expense_id:
                expense['amount'] = round(float(amount), 2)
                expense['category'] = category
                expense['description'] = description or "No description"
                expense['date'] = date.strftime("%Y-%m-%d")
                return self.save_expenses()
        return False
    
    def delete_expense(self, expense_id):
        """Delete an expense by ID."""
        self.expenses = [e for e in self.expenses if e['id'] != expense_id]
        return self.save_expenses()
    
    def get_dataframe(self):
        """Convert expenses to pandas DataFrame."""
        if not self.expenses:
            return pd.DataFrame(columns=['id', 'amount', 'category', 'description', 'date'])
        
        df = pd.DataFrame(self.expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        df = df.sort_values('date', ascending=False)
        return df
    
    def get_monthly_spending(self, year=None, month=None):
        """Get spending for a specific month."""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        df = self.get_dataframe()
        if df.empty:
            return 0
        
        mask = (df['date'].dt.year == year) & (df['date'].dt.month == month)
        return df[mask]['amount'].sum()
    
    def get_previous_month_spending(self):
        """Get spending for previous month."""
        now = datetime.now()
        if now.month == 1:
            prev_month = 12
            prev_year = now.year - 1
        else:
            prev_month = now.month - 1
            prev_year = now.year
        return self.get_monthly_spending(prev_year, prev_month)
    
    def get_category_breakdown(self):
        """Get spending breakdown by category."""
        df = self.get_dataframe()
        if df.empty:
            return {}
        return df.groupby('category')['amount'].sum().to_dict()
    
    def get_top_category(self):
        """Get the top spending category."""
        breakdown = self.get_category_breakdown()
        if not breakdown:
            return None, 0
        top = max(breakdown.items(), key=lambda x: x[1])
        return top[0], top[1]
    
    def get_budget_usage(self):
        """Get budget usage metrics."""
        current_month = self.get_monthly_spending()
        return {
            'budget': self.budget,
            'spent': current_month,
            'remaining': max(0, self.budget - current_month),
            'percentage': min(100, (current_month / self.budget * 100)) if self.budget > 0 else 0
        }
    
    def set_budget(self, amount):
        """Set monthly budget."""
        self.budget = float(amount)
        return self.save_expenses()
    
    def export_csv(self):
        """Export expenses as CSV string."""
        df = self.get_dataframe()
        if df.empty:
            return None
        return df.to_csv(index=False)
    
    def clear_all_data(self):
        """Clear all expenses."""
        self.expenses = []
        return self.save_expenses()


def render_compact_header():
    """Render the compact header."""
    today = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"""
        <div class="compact-header">
            <div class="title-section">
                <h1>📊 Expense Tracker</h1>
                <p>Track expenses, understand spending, and manage your budget.</p>
            </div>
            <div class="date-section">
                {today}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, sub_text=None, sub_positive=None, sub_negative=None, icon=None):
    """Render a single metric card."""
    sub_html = ""
    if sub_text:
        sub_html = f'<div class="metric-sub">{sub_text}</div>'
    elif sub_positive:
        sub_html = f'<div class="metric-sub metric-positive">↑ {sub_positive}</div>'
    elif sub_negative:
        sub_html = f'<div class="metric-sub metric-negative">↓ {sub_negative}</div>'
    
    icon_html = f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ''
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{icon_html}{label}</div>
            <div class="metric-value">{value}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


def render_navigation():
    """Render the navigation bar."""
    nav_items = {
        "Dashboard": "📊",
        "Add Expense": "➕",
        "History": "📋",
        "Analytics": "📈",
        "Manage": "⚙️"
    }
    
    if 'navigation' not in st.session_state:
        st.session_state.navigation = "Dashboard"
    
    cols = st.columns(len(nav_items))
    for col, (label, icon) in zip(cols, nav_items.items()):
        with col:
            is_active = st.session_state.navigation == label
            button_label = f"{icon} {label}" if is_active else f"{icon} {label}"
            if st.button(
                button_label,
                key=f"nav_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.navigation = label
                st.rerun()


def render_dashboard(df, manager):
    """Render the dashboard page."""
    st.markdown('<div class="section-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📝</div>
                <div class="empty-title">No expenses recorded yet.</div>
                <p style="color: #94A3B8;">Add your first expense to start tracking your spending.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("➕ Add Your First Expense", use_container_width=True, type="primary"):
                st.session_state.navigation = "Add Expense"
                st.rerun()
        return
    
    # KPI Cards
    total_spent = df['amount'].sum()
    num_expenses = len(df)
    current_month_spent = df[df['date'].dt.month == datetime.now().month]['amount'].sum()
    avg_expense = df['amount'].mean()
    
    # Previous month comparison
    prev_month_spent = manager.get_previous_month_spending()
    month_change = None
    if prev_month_spent > 0:
        change_pct = ((current_month_spent - prev_month_spent) / prev_month_spent) * 100
        month_change = f"{change_pct:+.1f}% vs last month"
    
    # Top category
    top_cat, top_cat_amount = manager.get_top_category()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            "Total Spent",
            f"₹{total_spent:,.0f}",
            sub_text=f"{num_expenses} transactions",
            icon="💰"
        )
    
    with col2:
        change_text = None
        if month_change:
            if current_month_spent >= prev_month_spent:
                change_text = month_change
            else:
                change_text = month_change
        render_metric_card(
            "This Month",
            f"₹{current_month_spent:,.0f}",
            sub_positive=month_change if month_change and current_month_spent >= prev_month_spent else None,
            sub_negative=month_change if month_change and current_month_spent < prev_month_spent else None,
            icon="📅"
        )
    
    with col3:
        render_metric_card(
            "Average Expense",
            f"₹{avg_expense:,.0f}",
            sub_text="per transaction",
            icon="📊"
        )
    
    with col4:
        if top_cat:
            render_metric_card(
                "Top Category",
                top_cat,
                sub_text=f"₹{top_cat_amount:,.0f}",
                icon="🏷️"
            )
        else:
            render_metric_card(
                "Top Category",
                "—",
                sub_text="No data",
                icon="🏷️"
            )
    
    st.divider()
    
    # Charts Section - Two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📈 Monthly Spending</div>', unsafe_allow_html=True)
        
        # Monthly spending chart
        monthly_data = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        monthly_data['date'] = monthly_data['date'].astype(str)
        
        if not monthly_data.empty:
            fig = px.bar(
                monthly_data,
                x='date',
                y='amount',
                labels={'date': 'Month', 'amount': 'Spent (₹)'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(
                showlegend=False,
                height=280,
                margin=dict(t=20, b=0, l=0, r=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_xaxes(gridcolor='#F1F5F9')
            fig.update_yaxes(gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No monthly data available")
    
    with col2:
        st.markdown('<div class="section-header">🏷️ Category Breakdown</div>', unsafe_allow_html=True)
        
        category_data = df.groupby('category')['amount'].sum().reset_index()
        
        if not category_data.empty:
            fig = px.pie(
                category_data,
                values='amount',
                names='category',
                hole=0.55,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="v", y=0.5, font=dict(size=10)),
                height=280,
                margin=dict(t=20, b=0, l=0, r=0)
            )
            fig.update_traces(textposition='inside', textinfo='percent')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No category data available")
    
    st.divider()
    
    # Budget Tracking Section
    st.markdown('<div class="section-header">💰 Monthly Budget</div>', unsafe_allow_html=True)
    
    budget_info = manager.get_budget_usage()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Budget", f"₹{budget_info['budget']:,.0f}")
    with col2:
        st.metric("Spent", f"₹{budget_info['spent']:,.0f}")
    with col3:
        st.metric("Remaining", f"₹{budget_info['remaining']:,.0f}")
    with col4:
        st.metric("Used", f"{budget_info['percentage']:.0f}%")
    
    # Progress bar
    pct = budget_info['percentage'] / 100
    bar_color = '#10B981' if pct < 0.7 else '#F59E0B' if pct < 0.9 else '#EF4444'
    
    st.markdown(f"""
        <div class="budget-progress">
            <div class="budget-progress-bar" style="width: {min(pct * 100, 100)}%; background: {bar_color};"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Budget edit
    with st.expander("✏️ Edit Budget", expanded=False):
        col1, col2 = st.columns([2, 1])
        with col1:
            new_budget = st.number_input(
                "Set monthly budget",
                min_value=0.0,
                value=float(budget_info['budget']),
                step=500.0,
                format="%.0f"
            )
        with col2:
            if st.button("Update Budget", use_container_width=True):
                if manager.set_budget(new_budget):
                    st.success(f"✅ Budget updated to ₹{new_budget:,.0f}")
                    st.rerun()
    
    st.divider()
    
    # Recent Transactions
    st.markdown('<div class="section-header">📋 Recent Transactions</div>', unsafe_allow_html=True)
    
    recent = df.head(5)[['date', 'category', 'description', 'amount']]
    recent['date'] = recent['date'].dt.strftime('%d %b')
    
    st.dataframe(
        recent,
        column_config={
            "date": st.column_config.TextColumn("Date", width="small"),
            "category": st.column_config.TextColumn("Category", width="medium"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "amount": st.column_config.NumberColumn(
                "Amount",
                format="₹%.2f",
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("📋 View All", use_container_width=True):
        st.session_state.navigation = "History"
        st.rerun()


def render_add_expense(manager):
    """Render the add expense page."""
    st.markdown('<div class="section-header">➕ Add Expense</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Record your spending in seconds</div>', unsafe_allow_html=True)
    
    with st.form("add_expense", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                step=50.0,
                value=100.0,
                format="%.2f",
                help="Enter the expense amount"
            )
            
            category = st.selectbox(
                "Category",
                manager.categories,
                help="Select a category"
            )
        
        with col2:
            date = st.date_input(
                "Date",
                value=datetime.now(),
                max_value=datetime.now(),
                help="Select the expense date"
            )
            
            description = st.text_input(
                "Description",
                placeholder="What was this expense for?",
                help="Optional description"
            )
        
        submitted = st.form_submit_button(
            "➕ Add Expense",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validation
            if amount <= 0:
                st.error("❌ Amount must be greater than 0")
            elif not description or description.strip() == "":
                st.error("❌ Please provide a description")
            else:
                if manager.add_expense(amount, category, description, date):
                    st.success(f"✅ Added ₹{amount:,.2f} to {category}")
                    st.balloons()
                    # Refresh to show updated data
                    st.rerun()
                else:
                    st.error("❌ Failed to save expense")


def render_history(df, manager):
    """Render the history page with edit/delete functionality."""
    st.markdown('<div class="section-header">📋 Transaction History</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-title">No transactions recorded yet.</div>
                <p style="color: #94A3B8;">Add your first expense to start tracking.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Filters
    with st.expander("🔍 Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ['All'] + sorted(df['category'].unique().tolist())
            selected_category = st.selectbox("Category", categories, key="history_category")
        
        with col2:
            min_date = df['date'].min().date()
            max_date = df['date'].max().date()
            date_range = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="history_date_range"
            )
        
        with col3:
            sort_options = {
                "Newest First": ('date', False),
                "Oldest First": ('date', True),
                "Highest Amount": ('amount', False),
                "Lowest Amount": ('amount', True)
            }
            sort_by = st.selectbox("Sort By", list(sort_options.keys()), key="history_sort")
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= date_range[0]) &
            (filtered_df['date'].dt.date <= date_range[1])
        ]
    
    sort_col, sort_asc = sort_options[sort_by]
    filtered_df = filtered_df.sort_values(sort_col, ascending=sort_asc)
    
    # Summary
    if not filtered_df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Transactions", len(filtered_df))
        with col2:
            st.metric("Total Amount", f"₹{filtered_df['amount'].sum():,.2f}")
        with col3:
            st.metric("Average", f"₹{filtered_df['amount'].mean():,.2f}")
    
    st.divider()
    
    # Show transactions with actions
    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1.5, 2, 1.5, 0.8, 0.8])
            
            with col1:
                st.write(row['date'].strftime('%d %b %Y'))
            with col2:
                st.write(row['category'])
            with col3:
                st.write(row['description'])
            with col4:
                st.write(f"₹{row['amount']:.2f}")
            with col5:
                edit_key = f"edit_{row['id']}"
                if st.button("✏️", key=edit_key, help="Edit expense"):
                    st.session_state.edit_expense_id = row['id']
                    st.rerun()
            with col6:
                delete_key = f"delete_{row['id']}"
                if st.button("🗑️", key=delete_key, help="Delete expense"):
                    st.session_state.delete_expense_id = row['id']
                    st.rerun()
            
            # Edit form
            if st.session_state.get('edit_expense_id') == row['id']:
                st.info("✏️ Edit Expense")
                with st.form(key=f"edit_form_{row['id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_amount = st.number_input(
                            "Amount",
                            min_value=0.01,
                            value=float(row['amount']),
                            step=50.0,
                            format="%.2f",
                            key=f"edit_amount_{row['id']}"
                        )
                        new_category = st.selectbox(
                            "Category",
                            manager.categories,
                            index=manager.categories.index(row['category']),
                            key=f"edit_category_{row['id']}"
                        )
                    with col2:
                        new_date = st.date_input(
                            "Date",
                            value=row['date'].date(),
                            max_value=datetime.now().date(),
                            key=f"edit_date_{row['id']}"
                        )
                        new_description = st.text_input(
                            "Description",
                            value=row['description'],
                            key=f"edit_desc_{row['id']}"
                        )
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.form_submit_button("💾 Save", type="primary"):
                            if manager.update_expense(row['id'], new_amount, new_category, new_description, new_date):
                                st.success("✅ Expense updated")
                                del st.session_state.edit_expense_id
                                st.rerun()
                    with col3:
                        if st.form_submit_button("❌ Cancel"):
                            del st.session_state.edit_expense_id
                            st.rerun()
    
    # Delete confirmation
    if st.session_state.get('delete_expense_id'):
        expense_id = st.session_state.delete_expense_id
        expense = df[df['id'] == expense_id].iloc[0]
        
        st.warning(f"⚠️ Are you sure you want to delete this expense?\n\n**{expense['description']}** - ₹{expense['amount']:.2f} ({expense['category']})")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete", type="primary"):
                if manager.delete_expense(expense_id):
                    st.success("✅ Expense deleted")
                    del st.session_state.delete_expense_id
                    st.rerun()
        with col2:
            if st.button("❌ Cancel"):
                del st.session_state.delete_expense_id
                st.rerun()
    
    # Export CSV
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📥 Export CSV", use_container_width=True):
            csv_data = manager.export_csv()
            if csv_data:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No data to export")


def render_analytics(df, manager):
    """Render the analytics page."""
    st.markdown('<div class="section-header">📈 Analytics</div>', unsafe_allow_html=True)
    
    if df.empty:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <div class="empty-title">No data to analyze.</div>
                <p style="color: #94A3B8;">Add expenses to see detailed analytics and insights.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Time period selector
    period = st.selectbox(
        "Time Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Month", "This Year", "All Time"],
        key="analytics_period"
    )
    
    # Filter data based on period
    now = datetime.now()
    if period == "Last 7 Days":
        filtered = df[df['date'] >= now - timedelta(days=7)]
    elif period == "Last 30 Days":
        filtered = df[df['date'] >= now - timedelta(days=30)]
    elif period == "Last 90 Days":
        filtered = df[df['date'] >= now - timedelta(days=90)]
    elif period == "This Month":
        filtered = df[df['date'].dt.month == now.month]
    elif period == "This Year":
        filtered = df[df['date'].dt.year == now.year]
    else:
        filtered = df
    
    if filtered.empty:
        st.warning(f"No data available for {period}")
        return
    
    # Statistics Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Spending", f"₹{filtered['amount'].sum():,.0f}")
    with col2:
        st.metric("Average Expense", f"₹{filtered['amount'].mean():,.0f}")
    with col3:
        st.metric("Highest Expense", f"₹{filtered['amount'].max():,.0f}")
    with col4:
        st.metric("Lowest Expense", f"₹{filtered['amount'].min():,.0f}")
    
    st.divider()
    
    # Charts
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🏷️ Category Analysis", "💡 Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Daily spending trend
            daily = filtered.groupby(filtered['date'].dt.date)['amount'].sum().reset_index()
            fig = px.line(
                daily,
                x='date',
                y='amount',
                title="Daily Spending Trend",
                labels={'date': 'Date', 'amount': 'Amount (₹)'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(
                height=300,
                margin=dict(t=40, b=0, l=0, r=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_xaxes(gridcolor='#F1F5F9')
            fig.update_yaxes(gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Monthly comparison
            monthly = filtered.groupby(filtered['date'].dt.to_period('M'))['amount'].sum().reset_index()
            monthly['date'] = monthly['date'].astype(str)
            fig = px.bar(
                monthly,
                x='date',
                y='amount',
                title="Monthly Spending",
                labels={'date': 'Month', 'amount': 'Amount (₹)'},
                color_discrete_sequence=['#764ba2']
            )
            fig.update_layout(
                height=300,
                margin=dict(t=40, b=0, l=0, r=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_xaxes(gridcolor='#F1F5F9')
            fig.update_yaxes(gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Category breakdown
            cat_data = filtered.groupby('category')['amount'].sum().reset_index().sort_values('amount', ascending=True)
            fig = px.bar(
                cat_data,
                x='amount',
                y='category',
                title="Spending by Category",
                labels={'amount': 'Amount (₹)', 'category': ''},
                orientation='h',
                color='amount',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=350,
                margin=dict(t=40, b=0, l=0, r=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            fig.update_xaxes(gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category donut
            fig = px.pie(
                cat_data,
                values='amount',
                names='category',
                title="Category Distribution",
                hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                height=350,
                margin=dict(t=40, b=0, l=0, r=0),
                showlegend=True,
                legend=dict(orientation="v", y=0.5, font=dict(size=10))
            )
            fig.update_traces(textposition='inside', textinfo='percent')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="section-header">💡 Spending Insights</div>', unsafe_allow_html=True)
        
        insights = []
        
        # Category insight
        top_cat, top_cat_amount = manager.get_top_category()
        if top_cat:
            insights.append(f"🏷️ **{top_cat}** is your highest spending category (₹{top_cat_amount:,.0f}).")
        
        # Monthly comparison
        current_month = manager.get_monthly_spending()
        prev_month = manager.get_previous_month_spending()
        if prev_month > 0:
            change_pct = ((current_month - prev_month) / prev_month) * 100
            if abs(change_pct) > 5:
                if change_pct > 0:
                    insights.append(f"📈 You spent **{change_pct:.0f}% more** this month than last month.")
                else:
                    insights.append(f"📉 You spent **{abs(change_pct):.0f}% less** this month than last month.")
        
        # Average expense
        avg_exp = filtered['amount'].mean()
        insights.append(f"📊 Your average expense is ₹{avg_exp:,.0f}.")
        
        # Highest expense
        max_exp = filtered['amount'].max()
        if max_exp > 0:
            max_desc = filtered[filtered['amount'] == max_exp]['description'].iloc[0]
            insights.append(f"💎 Your highest expense was ₹{max_exp:,.0f} for '{max_desc}'.")
        
        # Number of transactions
        num_trans = len(filtered)
        insights.append(f"📝 You have recorded **{num_trans} transactions** in this period.")
        
        # Budget insight
        budget_info = manager.get_budget_usage()
        if budget_info['budget'] > 0:
            pct = budget_info['percentage']
            if pct > 90:
                insights.append(f"⚠️ You have used **{pct:.0f}%** of your monthly budget. Consider reducing spending.")
            elif pct > 70:
                insights.append(f"💡 You have used **{pct:.0f}%** of your monthly budget. Keep an eye on spending.")
            else:
                insights.append(f"✅ You are on track with **{pct:.0f}%** of your monthly budget used.")
        
        # Display insights
        for insight in insights:
            st.info(insight)


def render_manage(df, manager):
    """Render the manage page."""
    st.markdown('<div class="section-header">⚙️ Manage</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏷️ Categories", "💾 Data Management"])
    
    with tab1:
        st.markdown('<div class="section-subheader">Manage your expense categories</div>', unsafe_allow_html=True)
        
        # Display current categories
        st.write("**Current Categories:**")
        for i, cat in enumerate(manager.categories):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"{i+1}. {cat}")
            with col2:
                # Rename
                if st.button(f"✏️ Rename", key=f"rename_btn_{i}"):
                    st.session_state.rename_category_index = i
            with col3:
                # Delete (prevent deletion of 'Other')
                if cat != "Other":
                    if st.button(f"🗑️ Delete", key=f"delete_cat_{i}"):
                        # Check if category is in use
                        if cat in df['category'].values:
                            st.error(f"Cannot delete '{cat}' - it has existing expenses")
                        else:
                            manager.categories.pop(i)
                            manager.save_expenses()
                            st.success(f"Deleted category: {cat}")
                            st.rerun()
                else:
                    st.caption("Required")
            
            # Rename form
            if st.session_state.get('rename_category_index') == i:
                with st.form(key=f"rename_form_{i}"):
                    new_name = st.text_input("New category name", value=cat)
                    if st.form_submit_button("Save"):
                        if new_name and new_name not in manager.categories:
                            manager.categories[i] = new_name
                            manager.save_expenses()
                            del st.session_state.rename_category_index
                            st.success(f"Renamed to: {new_name}")
                            st.rerun()
                        else:
                            st.error("Invalid name or duplicate")
        
        # Add new category
        st.divider()
        with st.form("add_category"):
            col1, col2 = st.columns([2, 1])
            with col1:
                new_category = st.text_input("New category name", placeholder="e.g., Groceries")
            with col2:
                if st.form_submit_button("➕ Add Category", use_container_width=True):
                    if new_category and new_category not in manager.categories:
                        manager.categories.append(new_category)
                        manager.save_expenses()
                        st.success(f"Added category: {new_category}")
                        st.rerun()
                    else:
                        st.error("Invalid or duplicate category")
    
    with tab2:
        st.markdown('<div class="section-subheader">Export, import, or clear your data</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Export Data**")
            if st.button("📥 Export CSV", use_container_width=True):
                csv_data = manager.export_csv()
                if csv_data:
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv_data,
                        file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.warning("No data to export")
            
            st.write("**Import Data**")
            uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
            if uploaded_file:
                try:
                    imported_df = pd.read_csv(uploaded_file)
                    # Validate columns
                    required_cols = ['amount', 'category', 'description', 'date']
                    if all(col in imported_df.columns for col in required_cols):
                        count = 0
                        for _, row in imported_df.iterrows():
                            try:
                                manager.add_expense(
                                    float(row['amount']),
                                    str(row['category']),
                                    str(row['description']),
                                    pd.to_datetime(row['date'])
                                )
                                count += 1
                            except Exception:
                                continue
                        st.success(f"✅ Imported {count} expenses")
                        st.rerun()
                    else:
                        st.error("Invalid CSV format. Required columns: amount, category, description, date")
                except Exception as e:
                    st.error(f"Error importing: {str(e)}")
        
        with col2:
            st.write("**Danger Zone**")
            with st.expander("⚠️ Clear All Data", expanded=False):
                st.warning("⚠️ This action is permanent and cannot be undone!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Clear All Data", use_container_width=True, type="primary"):
                        st.session_state.confirm_clear = True
                with col2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.confirm_clear = False
                
                if st.session_state.get('confirm_clear', False):
                    st.error("⚠️ Are you absolutely sure?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Yes, Delete Everything", use_container_width=True):
                            if manager.clear_all_data():
                                st.success("All data cleared")
                                st.session_state.confirm_clear = False
                                st.rerun()
                    with col2:
                        if st.button("❌ No, Cancel", use_container_width=True):
                            st.session_state.confirm_clear = False
                            st.rerun()


def main():
    """Main application."""
    # Initialize manager
    if 'manager' not in st.session_state:
        st.session_state.manager = ExpenseManager()
    
    manager = st.session_state.manager
    
    # Initialize navigation
    if 'navigation' not in st.session_state:
        st.session_state.navigation = "Dashboard"
    
    # Render compact header
    render_compact_header()
    
    # Render navigation
    render_navigation()
    
    # Render selected page
    current_page = st.session_state.navigation
    df = manager.get_dataframe()
    
    # Page handlers with correct signatures
    page_handlers = {
        "Dashboard": render_dashboard,
        "Add Expense": render_add_expense,
        "History": render_history,
        "Analytics": render_analytics,
        "Manage": render_manage
    }
    
    if current_page in page_handlers:
        handler = page_handlers[current_page]
        # Call the handler with the appropriate arguments
        if current_page == "Add Expense":
            handler(manager)  # Only manager needed
        else:
            handler(df, manager)  # Both df and manager needed
    else:
        render_dashboard(df, manager)


if __name__ == "__main__":
    main()
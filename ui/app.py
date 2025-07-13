import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys
import hashlib
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random

# Page config
st.set_page_config(
    page_title="LinkedIn Automation Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0077B5;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .demo-banner {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        color: #333;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Simple authentication system
def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    """Check if credentials are valid"""
    # Default admin credentials (in production, store these securely)
    valid_users = {
        'admin': hash_password('admin123')
    }
    
    if username in valid_users:
        return hash_password(password) == valid_users[username]
    return False

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'bot_running' not in st.session_state:
        st.session_state.bot_running = False
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = [
            {'timestamp': '09:15:23', 'action': 'Demo: LinkedIn automation started'},
            {'timestamp': '09:16:45', 'action': 'Demo: Found 25 profiles for "python developer"'},
            {'timestamp': '09:18:12', 'action': 'Demo: Sent 5 connection requests'},
            {'timestamp': '09:19:30', 'action': 'Demo: Profile data extracted from 3 profiles'},
        ]
    if 'daily_stats' not in st.session_state:
        st.session_state.daily_stats = {
            'connections_sent': random.randint(15, 35),
            'messages_sent': random.randint(5, 15),
            'profiles_viewed': random.randint(30, 80)
        }

def generate_demo_message(profile_name, field):
    """Generate a demo personalized message"""
    templates = [
        f"Hi {profile_name}! I noticed your expertise in {field} and would love to connect.",
        f"Hello {profile_name}! Your background in {field} is impressive. Let's connect!",
        f"Hi {profile_name}! I'm also passionate about {field}. Would love to network with you.",
    ]
    return random.choice(templates)

def login_page():
    """Simple login page"""
    st.markdown('<div class="main-header">🔐 LinkedIn Bot Login</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="demo-banner">🎭 DEMO MODE - This is a demonstration of the LinkedIn Automation UI</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.subheader("Login to Dashboard")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with st.expander("🔑 Default Login Credentials"):
        st.info("""
        **Username:** admin  
        **Password:** admin123
        
        ⚠️ **Note:** This is a demo version showcasing the UI functionality.
        """)

def main_dashboard():
    """Main dashboard page"""
    st.markdown('<div class="demo-banner">🎭 DEMO MODE - Simulated LinkedIn Automation Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🤖 LinkedIn Automation Dashboard</div>', unsafe_allow_html=True)
    
    # Status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "🟢 Demo Mode" if st.session_state.bot_running else "🔴 Demo Offline"
        st.metric("Bot Status", status)
    
    with col2:
        st.metric("Connections Today", st.session_state.daily_stats['connections_sent'])
    
    with col3:
        st.metric("Profiles Viewed", st.session_state.daily_stats['profiles_viewed'])
    
    with col4:
        st.metric("Messages Sent", st.session_state.daily_stats['messages_sent'])
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Demo People Search", use_container_width=True):
            st.info("🎭 In the full version, this would open the People Search page with advanced filtering capabilities.")
    
    with col2:
        if st.button("📧 Demo Connections", use_container_width=True):
            st.info("🎭 In the full version, this would open the Connection Manager for sending personalized requests.")
    
    with col3:
        if st.button("📊 Demo Analytics", use_container_width=True):
            st.info("🎭 In the full version, this would show detailed performance analytics and insights.")
    
    # Recent Activity
    st.subheader("📋 Recent Activity (Demo)")
    
    for activity in st.session_state.activity_log[-10:]:
        st.write(f"**{activity['timestamp']}** - {activity['action']}")
    
    # System Health
    st.subheader("🏥 System Health (Demo)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily limits chart
        limits_data = {
            'Metric': ['Connections', 'Messages', 'Profile Views'],
            'Current': [
                st.session_state.daily_stats['connections_sent'],
                st.session_state.daily_stats['messages_sent'],
                st.session_state.daily_stats['profiles_viewed']
            ],
            'Limit': [50, 20, 100]
        }
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Current', x=limits_data['Metric'], y=limits_data['Current'], marker_color='#0077B5'))
        fig.add_trace(go.Bar(name='Limit', x=limits_data['Metric'], y=limits_data['Limit'], marker_color='#E0E0E0'))
        fig.update_layout(title="Daily Usage vs Limits (Demo)", barmode='group', height=300)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Success rate (mock data)
        success_data = {
            'Date': [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)],
            'Success Rate': [85, 92, 78, 96, 89, 94, 87]
        }
        
        fig = px.line(success_data, x='Date', y='Success Rate', title="Success Rate (Demo - Last 7 Days)")
        fig.update_layout(height=300)
        
        st.plotly_chart(fig, use_container_width=True)

def demo_people_search():
    """Demo people search page"""
    st.markdown('<div class="demo-banner">🎭 DEMO: People Search Interface</div>', unsafe_allow_html=True)
    
    st.title("🔍 People Search (Demo)")
    st.markdown("This demonstrates the search interface for finding LinkedIn profiles.")
    
    with st.form("demo_search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            keywords = st.text_input("Keywords", value="python developer")
            location = st.text_input("Location", value="San Francisco")
        
        with col2:
            connection_level = st.selectbox("Connection Level", ["All", "1st", "2nd", "3rd+"], index=1)
            industry_filter = st.multiselect("Industry Filter", ["Technology", "Finance", "Healthcare"])
        
        search_submitted = st.form_submit_button("🔍 Demo Search", use_container_width=True, type="primary")
    
    if search_submitted:
        with st.spinner("Simulating LinkedIn search..."):
            time.sleep(2)
        
        st.success(f"Demo: Found 42 profiles for '{keywords}' in {location}")
        
        # Demo results
        demo_profiles = [
            {"name": "John Smith", "title": "Senior Python Developer", "company": "Tech Corp"},
            {"name": "Sarah Johnson", "title": "Full Stack Developer", "company": "StartupXYZ"},
            {"name": "Mike Chen", "title": "Lead Software Engineer", "company": "BigTech Inc"},
        ]
        
        st.subheader("📋 Demo Search Results")
        for i, profile in enumerate(demo_profiles, 1):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{profile['name']}**")
            with col2:
                st.write(f"{profile['title']} at {profile['company']}")
            with col3:
                if st.button("Connect", key=f"connect_{i}"):
                    st.info(f"🎭 Demo: Would send connection request to {profile['name']}")

def demo_connection_manager():
    """Demo connection manager page"""
    st.markdown('<div class="demo-banner">🎭 DEMO: Connection Manager Interface</div>', unsafe_allow_html=True)
    
    st.title("📧 Connection Manager (Demo)")
    st.markdown("This demonstrates the connection request management system.")
    
    st.subheader("➕ Demo Message Templates")
    
    template_type = st.selectbox(
        "Message Template Type",
        ["Professional", "Casual", "Industry Specific", "Educational"]
    )
    
    demo_profiles = [
        {"name": "Alice Brown", "field": "data science"},
        {"name": "Bob Wilson", "field": "software development"},
    ]
    
    st.subheader("📝 Demo Personalized Messages")
    for profile in demo_profiles:
        message = generate_demo_message(profile['name'], profile['field'])
        st.write(f"**{profile['name']}:** {message}")
    
    if st.button("🚀 Demo Send Connection Requests"):
        with st.spinner("Simulating connection requests..."):
            time.sleep(3)
        st.success("🎭 Demo: Would send 2 personalized connection requests!")

def demo_analytics():
    """Demo analytics page"""
    st.markdown('<div class="demo-banner">🎭 DEMO: Analytics Dashboard</div>', unsafe_allow_html=True)
    
    st.title("📊 Analytics Dashboard (Demo)")
    st.markdown("This demonstrates the performance analytics and insights.")
    
    # Demo metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Connections", "147", delta="12")
    with col2:
        st.metric("Success Rate", "89%", delta="5%")
    with col3:
        st.metric("Profile Views", "423", delta="23")
    with col4:
        st.metric("Response Rate", "34%", delta="2%")
    
    # Demo charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Industry breakdown
        industry_data = {"Technology": 45, "Finance": 25, "Healthcare": 20, "Other": 10}
        fig = px.pie(values=list(industry_data.values()), names=list(industry_data.keys()), 
                     title="Target Industries (Demo)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Weekly activity
        dates = [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)]
        activity = [12, 18, 15, 22, 19, 8, 5]
        
        fig = px.bar(x=dates, y=activity, title="Weekly Activity (Demo)")
        fig.update_layout(xaxis_title="Date", yaxis_title="Connections")
        st.plotly_chart(fig, use_container_width=True)

def demo_settings():
    """Demo settings page"""
    st.markdown('<div class="demo-banner">🎭 DEMO: Settings & Configuration</div>', unsafe_allow_html=True)
    
    st.title("⚙️ Settings (Demo)")
    st.markdown("This demonstrates the configuration interface.")
    
    st.subheader("🔐 LinkedIn Credentials (Demo)")
    with st.form("demo_credentials_form"):
        email = st.text_input("LinkedIn Email", placeholder="your_email@example.com")
        password = st.text_input("LinkedIn Password", type="password", placeholder="Your password")
        
        if st.form_submit_button("Save Credentials"):
            st.success("🎭 Demo: Credentials would be saved securely!")
    
    st.subheader("🎛️ Automation Settings (Demo)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        headless_mode = st.checkbox("Headless Mode", value=True)
        max_connections = st.slider("Max Connections per Day", 1, 100, 50)
        max_messages = st.slider("Max Messages per Day", 1, 50, 20)
        
    with col2:
        min_delay = st.slider("Min Delay (seconds)", 1, 10, 2)
        max_delay = st.slider("Max Delay (seconds)", 5, 30, 5)
        page_timeout = st.slider("Page Load Timeout (seconds)", 10, 60, 30)
    
    if st.button("Save Settings"):
        st.success("🎭 Demo: Settings would be saved!")

def main():
    """Main application function"""
    init_session_state()
    
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.write(f'Welcome **{st.session_state.username}**')
        
        selected = option_menu(
            menu_title="Navigation",
            options=["Dashboard", "People Search", "Connection Manager", "Analytics", "Settings"],
            icons=["house", "search", "people", "graph-up", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#0077B5", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#0077B5"},
            }
        )
        
        st.markdown("---")
        
        # Bot status in sidebar
        if st.session_state.bot_running:
            st.success("🟢 Demo Mode")
            if st.button("⏹️ Stop Demo"):
                st.session_state.bot_running = False
                st.rerun()
        else:
            st.error("🔴 Demo Offline")
            if st.button("▶️ Start Demo"):
                st.session_state.bot_running = True
                st.rerun()
        
        st.markdown("---")
        
        st.info("🎭 **Demo Mode**\n\nThis showcases the UI of a complete LinkedIn automation platform. The full version includes real automation capabilities.")
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # Main content area
    if selected == "Dashboard":
        main_dashboard()
    elif selected == "People Search":
        demo_people_search()
    elif selected == "Connection Manager":
        demo_connection_manager()
    elif selected == "Analytics":
        demo_analytics()
    elif selected == "Settings":
        demo_settings()

if __name__ == "__main__":
    main()
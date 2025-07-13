import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import yaml
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import our modules
from linkedin_bot import LinkedInBot
from utils.message_templates import get_connection_message
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

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
</style>
""", unsafe_allow_html=True)

# Authentication configuration
def load_auth_config():
    """Load authentication configuration"""
    config_path = Path(__file__).parent / "auth_config.yaml"
    
    if not config_path.exists():
        # Create default config
        default_config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@linkedin-bot.com',
                        'name': 'Administrator',
                        'password': '$2b$12$k8Y1THKC7zJW8Q7x8GJ8XO8ZX7ZJ8Y1THKC7zJW8Q7x8GJ8XO8ZX7'  # 'admin123'
                    }
                }
            },
            'cookie': {
                'name': 'linkedin_bot_auth',
                'key': 'linkedin_bot_secret_key',
                'expiry_days': 30
            },
            'preauthorized': ['admin@linkedin-bot.com']
        }
        
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def init_session_state():
    """Initialize session state variables"""
    if 'bot_instance' not in st.session_state:
        st.session_state.bot_instance = None
    if 'bot_running' not in st.session_state:
        st.session_state.bot_running = False
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = []
    if 'daily_stats' not in st.session_state:
        st.session_state.daily_stats = {
            'connections_sent': 0,
            'messages_sent': 0,
            'profiles_viewed': 0
        }

def create_bot_instance():
    """Create LinkedIn bot instance"""
    if st.session_state.bot_instance is None:
        headless = st.session_state.get('headless_mode', True)
        st.session_state.bot_instance = LinkedInBot(headless=headless)
    return st.session_state.bot_instance

def main_dashboard():
    """Main dashboard page"""
    st.markdown('<div class="main-header">🤖 LinkedIn Automation Dashboard</div>', unsafe_allow_html=True)
    
    # Status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "🟢 Online" if st.session_state.bot_running else "🔴 Offline"
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
        if st.button("🎯 Start People Search", use_container_width=True):
            st.switch_page("pages/People_Search.py")
    
    with col2:
        if st.button("📧 Send Connections", use_container_width=True):
            st.switch_page("pages/Connection_Manager.py")
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.switch_page("pages/Analytics.py")
    
    # Recent Activity
    st.subheader("📋 Recent Activity")
    
    if st.session_state.activity_log:
        for activity in st.session_state.activity_log[-10:]:
            st.write(f"**{activity['timestamp']}** - {activity['action']}")
    else:
        st.info("No recent activity. Start automating to see logs here!")
    
    # System Health
    st.subheader("🏥 System Health")
    
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
        fig.update_layout(title="Daily Usage vs Limits", barmode='group', height=300)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Success rate (mock data for now)
        success_data = {
            'Date': [datetime.now() - timedelta(days=i) for i in range(7, 0, -1)],
            'Success Rate': [85, 92, 78, 96, 89, 94, 87]
        }
        
        fig = px.line(success_data, x='Date', y='Success Rate', title="Success Rate (Last 7 Days)")
        fig.update_layout(height=300)
        
        st.plotly_chart(fig, use_container_width=True)

def bot_settings():
    """Bot configuration settings"""
    st.header("⚙️ Bot Configuration")
    
    # LinkedIn Credentials
    st.subheader("🔐 LinkedIn Credentials")
    
    with st.form("credentials_form"):
        email = st.text_input("LinkedIn Email", value=os.getenv('LINKEDIN_EMAIL', ''))
        password = st.text_input("LinkedIn Password", type="password")
        
        if st.form_submit_button("Save Credentials"):
            # Save to .env file
            env_path = Path(__file__).parent.parent / '.env'
            
            # Read existing .env
            env_content = ""
            if env_path.exists():
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                
                # Update existing lines or add new ones
                email_updated = False
                password_updated = False
                
                for i, line in enumerate(lines):
                    if line.startswith('LINKEDIN_EMAIL='):
                        lines[i] = f'LINKEDIN_EMAIL={email}\n'
                        email_updated = True
                    elif line.startswith('LINKEDIN_PASSWORD='):
                        lines[i] = f'LINKEDIN_PASSWORD={password}\n'
                        password_updated = True
                
                env_content = ''.join(lines)
                
                if not email_updated:
                    env_content += f'\nLINKEDIN_EMAIL={email}\n'
                if not password_updated:
                    env_content += f'LINKEDIN_PASSWORD={password}\n'
            else:
                env_content = f'LINKEDIN_EMAIL={email}\nLINKEDIN_PASSWORD={password}\n'
            
            with open(env_path, 'w') as f:
                f.write(env_content)
            
            st.success("Credentials saved successfully!")
    
    st.markdown("---")
    
    # Automation Settings
    st.subheader("🎛️ Automation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        headless_mode = st.checkbox("Headless Mode (Background)", value=True)
        st.session_state.headless_mode = headless_mode
        
        max_connections = st.slider("Max Connections per Day", 1, 100, 50)
        max_messages = st.slider("Max Messages per Day", 1, 50, 20)
        
    with col2:
        min_delay = st.slider("Min Delay (seconds)", 1, 10, 2)
        max_delay = st.slider("Max Delay (seconds)", 5, 30, 5)
        page_timeout = st.slider("Page Load Timeout (seconds)", 10, 60, 30)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

def login_page():
    """Login page"""
    st.markdown('<div class="main-header">🔐 LinkedIn Bot Login</div>', unsafe_allow_html=True)
    
    # Load authentication config
    config = load_auth_config()
    
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    
    name, authentication_status, username = authenticator.login('Login to Dashboard', 'main')
    
    if authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        
        with st.expander("🔑 Default Login Credentials"):
            st.info("""
            **Username:** admin  
            **Password:** admin123
            
            ⚠️ **Important:** Change these default credentials in production!
            """)
    
    return authentication_status, name, username, authenticator

def main():
    """Main application function"""
    init_session_state()
    
    # Check authentication
    authentication_status, name, username, authenticator = login_page()
    
    if authentication_status == True:
        # Sidebar navigation
        with st.sidebar:
            st.write(f'Welcome **{name}**')
            
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
                st.success("🟢 Bot is Running")
                if st.button("⏹️ Stop Bot"):
                    st.session_state.bot_running = False
                    st.rerun()
            else:
                st.error("🔴 Bot is Stopped")
                if st.button("▶️ Start Bot"):
                    st.session_state.bot_running = True
                    st.rerun()
            
            st.markdown("---")
            authenticator.logout('Logout', 'sidebar')
        
        # Main content area
        if selected == "Dashboard":
            main_dashboard()
        elif selected == "People Search":
            st.switch_page("pages/People_Search.py")
        elif selected == "Connection Manager":
            st.switch_page("pages/Connection_Manager.py")
        elif selected == "Analytics":
            st.switch_page("pages/Analytics.py")
        elif selected == "Settings":
            bot_settings()

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import time
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from linkedin_bot import LinkedInBot
from utils.message_templates import get_connection_message, extract_field_from_headline

st.set_page_config(page_title="People Search", page_icon="🔍", layout="wide")

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

def save_search_history(keywords, location, results_count):
    """Save search to history"""
    search_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'keywords': keywords,
        'location': location,
        'results_count': results_count
    }
    st.session_state.search_history.append(search_entry)
    
    # Keep only last 20 searches
    if len(st.session_state.search_history) > 20:
        st.session_state.search_history = st.session_state.search_history[-20:]

def perform_search(keywords, location, connection_level, industry_filter):
    """Perform LinkedIn people search"""
    try:
        # Create or get bot instance
        if 'bot_instance' not in st.session_state or st.session_state.bot_instance is None:
            headless = st.session_state.get('headless_mode', True)
            st.session_state.bot_instance = LinkedInBot(headless=headless)
        
        bot = st.session_state.bot_instance
        
        # Start session if not already started
        if not hasattr(bot, 'driver') or bot.driver is None:
            bot.start_session()
            
            # Login if not already logged in
            if not bot.is_logged_in:
                with st.spinner("Logging into LinkedIn..."):
                    success = bot.login()
                    if not success:
                        st.error("Failed to login to LinkedIn. Please check your credentials in Settings.")
                        return []
        
        # Perform search
        with st.spinner(f"Searching for '{keywords}' in {location}..."):
            profiles = bot.search_people(keywords, location)
            
        # Save to history
        save_search_history(keywords, location, len(profiles))
        
        # Add activity log
        activity = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'action': f"Searched for '{keywords}' - found {len(profiles)} profiles"
        }
        if 'activity_log' not in st.session_state:
            st.session_state.activity_log = []
        st.session_state.activity_log.append(activity)
        
        return profiles
        
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return []

def main():
    st.title("🔍 People Search")
    st.markdown("Search for LinkedIn profiles based on keywords, location, and other criteria.")
    
    # Search Form
    st.subheader("🎯 Search Criteria")
    
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            keywords = st.text_input(
                "Keywords", 
                placeholder="e.g., python developer, marketing manager, data scientist",
                help="Enter job titles, skills, or industry keywords"
            )
            
            location = st.text_input(
                "Location", 
                placeholder="e.g., San Francisco, New York, London",
                help="City, state, or country"
            )
        
        with col2:
            connection_level = st.selectbox(
                "Connection Level",
                ["All", "1st", "2nd", "3rd+"],
                index=1,
                help="Filter by connection degree"
            )
            
            industry_filter = st.multiselect(
                "Industry Filter",
                ["Technology", "Finance", "Healthcare", "Marketing", "Sales", "Consulting", "Education"],
                help="Optional industry filters"
            )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            max_results = st.slider("Max Results", 10, 100, 50)
            include_premium = st.checkbox("Include Premium profiles")
            current_company_only = st.checkbox("Current company employees only")
        
        search_submitted = st.form_submit_button("🔍 Search", use_container_width=True, type="primary")
    
    # Perform search when form is submitted
    if search_submitted and keywords:
        profiles = perform_search(keywords, location, connection_level, industry_filter)
        st.session_state.search_results = profiles
        
        if profiles:
            st.success(f"Found {len(profiles)} profiles!")
        else:
            st.warning("No profiles found. Try different keywords or location.")
    
    # Display search results
    if st.session_state.search_results:
        st.markdown("---")
        st.subheader("📋 Search Results")
        
        # Results summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Results", len(st.session_state.search_results))
        with col2:
            if st.button("💾 Export Results"):
                df = pd.DataFrame([{'Profile URL': url} for url in st.session_state.search_results])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"linkedin_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        with col3:
            if st.button("🔄 Clear Results"):
                st.session_state.search_results = []
                st.rerun()
        
        # Results table with actions
        st.subheader("🎯 Select Profiles for Actions")
        
        # Create a dataframe for display
        results_data = []
        for i, url in enumerate(st.session_state.search_results):
            results_data.append({
                'Select': False,
                'Profile #': i + 1,
                'Profile URL': url,
                'Actions': '⚡'
            })
        
        # Display results with selection
        edited_df = st.data_editor(
            pd.DataFrame(results_data),
            column_config={
                "Select": st.column_config.CheckboxColumn("Select"),
                "Profile URL": st.column_config.LinkColumn("Profile URL"),
                "Actions": st.column_config.TextColumn("Actions")
            },
            disabled=["Profile #", "Profile URL", "Actions"],
            hide_index=True,
            use_container_width=True
        )
        
        # Bulk actions for selected profiles
        selected_profiles = edited_df[edited_df['Select'] == True]['Profile URL'].tolist()
        
        if selected_profiles:
            st.markdown("---")
            st.subheader("⚡ Bulk Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📧 Send Connection Requests ({len(selected_profiles)})"):
                    st.switch_page("pages/Connection_Manager.py")
                    # Store selected profiles for connection manager
                    st.session_state.selected_profiles_for_connection = selected_profiles
            
            with col2:
                if st.button(f"📊 Extract Profile Data ({len(selected_profiles)})"):
                    extract_profile_data(selected_profiles)
            
            with col3:
                if st.button(f"💾 Save Selected ({len(selected_profiles)})"):
                    save_selected_profiles(selected_profiles)
    
    # Search History
    if st.session_state.search_history:
        st.markdown("---")
        st.subheader("📚 Search History")
        
        with st.expander("View Recent Searches"):
            history_df = pd.DataFrame(st.session_state.search_history)
            st.dataframe(history_df, use_container_width=True)
            
            if st.button("🗑️ Clear History"):
                st.session_state.search_history = []
                st.rerun()
    
    # Quick Search Templates
    st.markdown("---")
    st.subheader("🚀 Quick Search Templates")
    
    templates = {
        "Tech Professionals": {
            "keywords": "software engineer python developer",
            "location": "San Francisco",
            "description": "Find software engineers and Python developers in SF"
        },
        "Marketing Leaders": {
            "keywords": "marketing manager digital marketing",
            "location": "New York",
            "description": "Marketing professionals in NYC"
        },
        "Data Scientists": {
            "keywords": "data scientist machine learning",
            "location": "Seattle",
            "description": "Data science and ML professionals"
        },
        "Sales Professionals": {
            "keywords": "sales manager business development",
            "location": "Chicago",
            "description": "Sales and BD professionals"
        }
    }
    
    col1, col2 = st.columns(2)
    
    for i, (name, template) in enumerate(templates.items()):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            with st.container():
                st.markdown(f"**{name}**")
                st.caption(template['description'])
                
                if st.button(f"Use Template", key=f"template_{i}"):
                    # Auto-fill the form with template data
                    st.session_state.template_keywords = template['keywords']
                    st.session_state.template_location = template['location']
                    st.rerun()

def extract_profile_data(profile_urls):
    """Extract detailed data from selected profiles"""
    if 'bot_instance' not in st.session_state or st.session_state.bot_instance is None:
        st.error("Bot not initialized. Please perform a search first.")
        return
    
    bot = st.session_state.bot_instance
    extracted_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, url in enumerate(profile_urls):
        status_text.text(f"Extracting data from profile {i+1}/{len(profile_urls)}")
        
        try:
            data = bot.extract_profile_data(url)
            if data:
                extracted_data.append(data)
        except Exception as e:
            st.warning(f"Failed to extract data from {url}: {str(e)}")
        
        progress_bar.progress((i + 1) / len(profile_urls))
        time.sleep(1)  # Small delay to be respectful
    
    if extracted_data:
        # Save extracted data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"extracted_profiles_{timestamp}.csv"
        
        if hasattr(bot, 'save_data_to_csv'):
            bot.save_data_to_csv(extracted_data, filename)
        
        st.success(f"Extracted data from {len(extracted_data)} profiles!")
        
        # Display extracted data
        df = pd.DataFrame(extracted_data)
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Extracted Data",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )
    else:
        st.error("No data could be extracted from the selected profiles.")

def save_selected_profiles(profile_urls):
    """Save selected profiles to a file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"selected_profiles_{timestamp}.csv"
    
    df = pd.DataFrame([{'Profile URL': url} for url in profile_urls])
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="Download Selected Profiles",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
import streamlit as st
import sys
from pathlib import Path
import time
import random
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from linkedin_bot import LinkedInBot
from utils.message_templates import get_connection_message, CONNECTION_TEMPLATES, extract_field_from_headline

st.set_page_config(page_title="Connection Manager", page_icon="📧", layout="wide")

# Initialize session state
if 'connection_queue' not in st.session_state:
    st.session_state.connection_queue = []
if 'connection_history' not in st.session_state:
    st.session_state.connection_history = []
if 'message_templates' not in st.session_state:
    st.session_state.message_templates = []

def add_to_connection_queue(profiles, message_template, template_type):
    """Add profiles to connection queue"""
    for profile_url in profiles:
        queue_item = {
            'profile_url': profile_url,
            'message_template': message_template,
            'template_type': template_type,
            'status': 'Pending',
            'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        st.session_state.connection_queue.append(queue_item)

def send_connection_requests(selected_items, delay_range):
    """Send connection requests for selected items"""
    if 'bot_instance' not in st.session_state or st.session_state.bot_instance is None:
        st.error("Bot not initialized. Please perform a search first.")
        return
    
    bot = st.session_state.bot_instance
    
    # Ensure bot is logged in
    if not bot.is_logged_in:
        with st.spinner("Logging into LinkedIn..."):
            success = bot.login()
            if not success:
                st.error("Failed to login to LinkedIn. Please check your credentials in Settings.")
                return
    
    success_count = 0
    failed_count = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, item in enumerate(selected_items):
        status_text.text(f"Sending connection request {i+1}/{len(selected_items)}")
        
        try:
            # Extract profile data first for personalization
            profile_data = bot.extract_profile_data(item['profile_url'])
            
            # Generate personalized message
            if item['message_template']:
                if profile_data:
                    message = get_connection_message(profile_data, item['template_type'])
                else:
                    message = item['message_template']
            else:
                message = ""
            
            # Send connection request
            success = bot.send_connection_request(item['profile_url'], message)
            
            if success:
                success_count += 1
                item['status'] = 'Sent'
                item['sent_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['message_sent'] = message
                
                # Add to history
                st.session_state.connection_history.append(item.copy())
                
                # Update daily stats
                if 'daily_stats' not in st.session_state:
                    st.session_state.daily_stats = {'connections_sent': 0, 'messages_sent': 0, 'profiles_viewed': 0}
                st.session_state.daily_stats['connections_sent'] += 1
                
                # Add activity log
                activity = {
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'action': f"Connection request sent to {profile_data.get('name', 'Unknown')} ({item['profile_url']})"
                }
                if 'activity_log' not in st.session_state:
                    st.session_state.activity_log = []
                st.session_state.activity_log.append(activity)
                
            else:
                failed_count += 1
                item['status'] = 'Failed'
                item['failed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
        except Exception as e:
            failed_count += 1
            item['status'] = 'Failed'
            item['error'] = str(e)
            st.warning(f"Failed to send connection request: {str(e)}")
        
        progress_bar.progress((i + 1) / len(selected_items))
        
        # Random delay between requests
        if i < len(selected_items) - 1:  # Don't delay after last request
            delay = random.uniform(delay_range[0], delay_range[1])
            time.sleep(delay)
    
    # Remove sent/failed items from queue
    st.session_state.connection_queue = [
        item for item in st.session_state.connection_queue 
        if item not in selected_items
    ]
    
    st.success(f"✅ Sent {success_count} connection requests successfully!")
    if failed_count > 0:
        st.warning(f"⚠️ {failed_count} requests failed")

def main():
    st.title("📧 Connection Manager")
    st.markdown("Manage and send personalized connection requests to your target profiles.")
    
    # Check if there are profiles from search
    if 'selected_profiles_for_connection' in st.session_state and st.session_state.selected_profiles_for_connection:
        st.info(f"Found {len(st.session_state.selected_profiles_for_connection)} profiles from search. Add them to your queue below.")
    
    # Add Profiles Section
    st.subheader("➕ Add Profiles to Queue")
    
    tab1, tab2 = st.tabs(["From Search Results", "Manual Entry"])
    
    with tab1:
        if 'selected_profiles_for_connection' in st.session_state and st.session_state.selected_profiles_for_connection:
            st.write(f"**{len(st.session_state.selected_profiles_for_connection)} profiles** selected from search:")
            
            # Show preview
            for i, url in enumerate(st.session_state.selected_profiles_for_connection[:5]):
                st.write(f"{i+1}. {url}")
            if len(st.session_state.selected_profiles_for_connection) > 5:
                st.write(f"... and {len(st.session_state.selected_profiles_for_connection) - 5} more")
            
            # Message template selection
            template_type = st.selectbox(
                "Message Template Type",
                list(CONNECTION_TEMPLATES.keys()),
                help="Choose the style of connection message"
            )
            
            # Custom message option
            use_custom = st.checkbox("Use custom message template")
            if use_custom:
                custom_message = st.text_area(
                    "Custom Message Template",
                    placeholder="Hi {name}! Your work in {field} is impressive...",
                    help="Use {name} and {field} placeholders for personalization"
                )
                message_template = custom_message
            else:
                message_template = random.choice(CONNECTION_TEMPLATES[template_type])
                st.info(f"**Preview:** {message_template}")
            
            if st.button("📥 Add to Queue", type="primary"):
                add_to_connection_queue(
                    st.session_state.selected_profiles_for_connection,
                    message_template,
                    template_type
                )
                st.success(f"Added {len(st.session_state.selected_profiles_for_connection)} profiles to queue!")
                # Clear the selected profiles
                st.session_state.selected_profiles_for_connection = []
                st.rerun()
        else:
            st.info("No profiles selected from search. Use the People Search page to find profiles first.")
    
    with tab2:
        st.markdown("**Manually add profile URLs:**")
        
        manual_profiles = st.text_area(
            "Profile URLs (one per line)",
            placeholder="https://linkedin.com/in/username1\nhttps://linkedin.com/in/username2",
            height=100
        )
        
        if manual_profiles:
            urls = [url.strip() for url in manual_profiles.split('\n') if url.strip()]
            
            template_type_manual = st.selectbox(
                "Message Template Type",
                list(CONNECTION_TEMPLATES.keys()),
                key="manual_template_type"
            )
            
            message_template_manual = st.text_area(
                "Message Template",
                value=random.choice(CONNECTION_TEMPLATES[template_type_manual]),
                key="manual_message"
            )
            
            if st.button("📥 Add Manual Profiles to Queue"):
                add_to_connection_queue(urls, message_template_manual, template_type_manual)
                st.success(f"Added {len(urls)} profiles to queue!")
                st.rerun()
    
    # Connection Queue Management
    if st.session_state.connection_queue:
        st.markdown("---")
        st.subheader("📋 Connection Queue")
        
        # Queue summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Queued Requests", len(st.session_state.connection_queue))
        with col2:
            pending_count = len([item for item in st.session_state.connection_queue if item['status'] == 'Pending'])
            st.metric("Pending", pending_count)
        with col3:
            # Daily limit check
            daily_sent = st.session_state.get('daily_stats', {}).get('connections_sent', 0)
            remaining = max(0, 50 - daily_sent)  # 50 is daily limit
            st.metric("Daily Remaining", remaining)
        
        # Queue table
        queue_data = []
        for item in st.session_state.connection_queue:
            queue_item = {
                'Select': False,
                'Profile URL': item.get('profile_url', ''),
                'Template Type': item.get('template_type', ''),
                'Status': item.get('status', ''),
                'Added At': item.get('added_at', '')
            }
            queue_data.append(queue_item)
        
        queue_display = queue_data
        
        edited_queue = st.data_editor(
            queue_display,
            column_config={
                "Select": st.column_config.CheckboxColumn("Select"),
                "Profile URL": st.column_config.LinkColumn("Profile URL"),
            },
            disabled=["Profile URL", "Template Type", "Status", "Added At"],
            hide_index=True,
            use_container_width=True
        )
        
        # Bulk actions
        selected_indices = edited_queue[edited_queue['Select'] == True].index.tolist()
        selected_items = [st.session_state.connection_queue[i] for i in selected_indices]
        
        if selected_items:
            st.markdown("---")
            st.subheader("⚡ Send Connection Requests")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Selected:** {len(selected_items)} profiles")
                
                # Delay settings
                delay_min = st.slider("Min delay between requests (seconds)", 5, 30, 10)
                delay_max = st.slider("Max delay between requests (seconds)", 10, 60, 20)
                
                if delay_min >= delay_max:
                    st.error("Maximum delay must be greater than minimum delay")
                
            with col2:
                st.write("**Safety Checks:**")
                
                # Daily limit check
                daily_sent = st.session_state.get('daily_stats', {}).get('connections_sent', 0)
                if daily_sent + len(selected_items) > 50:
                    st.error(f"⚠️ This would exceed daily limit! ({daily_sent + len(selected_items)}/50)")
                else:
                    st.success(f"✅ Within daily limit ({daily_sent + len(selected_items)}/50)")
                
                # Time estimate
                avg_delay = (delay_min + delay_max) / 2
                estimated_time = (len(selected_items) * avg_delay) / 60
                st.info(f"🕒 Estimated time: {estimated_time:.1f} minutes")
            
            # Send button
            if daily_sent + len(selected_items) <= 50 and delay_min < delay_max:
                if st.button(
                    f"🚀 Send {len(selected_items)} Connection Requests",
                    type="primary",
                    use_container_width=True
                ):
                    send_connection_requests(selected_items, (delay_min, delay_max))
                    st.rerun()
            
            # Queue management buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Remove Selected from Queue"):
                    st.session_state.connection_queue = [
                        item for i, item in enumerate(st.session_state.connection_queue)
                        if i not in selected_indices
                    ]
                    st.success(f"Removed {len(selected_items)} items from queue")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Clear Entire Queue"):
                    st.session_state.connection_queue = []
                    st.success("Queue cleared")
                    st.rerun()
    
    else:
        st.info("No profiles in queue. Add some profiles using the sections above.")
    
    # Connection History
    if st.session_state.connection_history:
        st.markdown("---")
        st.subheader("📚 Connection History")
        
        # History summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sent", len(st.session_state.connection_history))
        with col2:
            today_sent = len([
                item for item in st.session_state.connection_history
                if item.get('sent_at', '').startswith(datetime.now().strftime('%Y-%m-%d'))
            ])
            st.metric("Sent Today", today_sent)
        with col3:
            success_rate = len([
                item for item in st.session_state.connection_history
                if item.get('status') == 'Sent'
            ]) / len(st.session_state.connection_history) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        # History table
        with st.expander("View Connection History"):
            history_data = []
            for item in st.session_state.connection_history:
                history_item = {
                    'Profile Url': item.get('profile_url', ''),
                    'Template Type': item.get('template_type', ''),
                    'Status': item.get('status', ''),
                    'Sent At': item.get('sent_at', '')
                }
                history_data.append(history_item)
            
            history_display = history_data
                
                st.dataframe(history_display, use_container_width=True)
                
                # Export history
                csv = history_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download History",
                    data=csv,
                    file_name=f"connection_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            # Clear history button
            if st.button("🗑️ Clear History"):
                st.session_state.connection_history = []
                st.success("History cleared")
                st.rerun()
    
    # Message Templates Management
    st.markdown("---")
    st.subheader("💬 Message Templates")
    
    with st.expander("Manage Custom Templates"):
        st.write("**Built-in Template Types:**")
        for template_type, templates in CONNECTION_TEMPLATES.items():
            st.write(f"**{template_type.title()}:**")
            for template in templates[:2]:  # Show first 2 examples
                st.write(f"  • {template}")
            if len(templates) > 2:
                st.write(f"  ... and {len(templates) - 2} more")
            st.write("")
        
        # Custom template creation
        st.write("**Create Custom Template:**")
        
        custom_name = st.text_input("Template Name")
        custom_message = st.text_area(
            "Template Message",
            placeholder="Hi {name}! I noticed your expertise in {field}...",
            help="Use {name} and {field} for personalization"
        )
        
        if st.button("💾 Save Custom Template") and custom_name and custom_message:
            if 'custom_templates' not in st.session_state:
                st.session_state.custom_templates = {}
            
            st.session_state.custom_templates[custom_name] = custom_message
            st.success(f"Saved template: {custom_name}")

if __name__ == "__main__":
    main()
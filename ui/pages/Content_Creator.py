import streamlit as st
import sys
from pathlib import Path
import time
import json
from datetime import datetime, timedelta
import os
import random

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

# Demo data for managed companies
DEMO_COMPANIES = [
    {
        'name': 'TechCorp Solutions',
        'url': 'https://www.linkedin.com/company/techcorp-solutions',
        'followers': 1250,
        'industry': 'Technology'
    },
    {
        'name': 'Digital Marketing Pro',
        'url': 'https://www.linkedin.com/company/digital-marketing-pro',
        'followers': 850,
        'industry': 'Marketing'
    },
    {
        'name': 'Innovation Labs',
        'url': 'https://www.linkedin.com/company/innovation-labs',
        'followers': 2100,
        'industry': 'Research'
    }
]

# Demo post templates
POST_TEMPLATES = {
    'Personal': {
        'Professional Update': """🚀 Exciting news to share!

I'm thrilled to announce [your achievement/update here]. This journey has been incredible, and I'm grateful for all the support from my network.

Key highlights:
• [Highlight 1]
• [Highlight 2]
• [Highlight 3]

Looking forward to what's next! 💪

#ProfessionalGrowth #Career #LinkedIn""",
        
        'Industry Insights': """💡 Thoughts on [industry/topic]

After [experience/observation], I've noticed some interesting trends:

1. [Trend 1]
2. [Trend 2]
3. [Trend 3]

What's your take on this? I'd love to hear your thoughts in the comments.

#Industry #Insights #TechTrends""",
        
        'Team Recognition': """👏 Shoutout to an amazing team!

Working with [team/colleagues] on [project] has been an absolute pleasure. Their dedication and expertise made all the difference.

Special thanks to:
• [Person 1] - [contribution]
• [Person 2] - [contribution]
• [Person 3] - [contribution]

Grateful to work with such talented people! 🙏

#Teamwork #Gratitude #Success"""
    },
    'Company': {
        'Product Launch': """🎉 We're excited to announce the launch of [Product Name]!

After months of hard work, we're proud to introduce a solution that [key benefit/value proposition].

✨ Key features:
• [Feature 1]
• [Feature 2]
• [Feature 3]

Join us in celebrating this milestone! Learn more: [link]

#ProductLaunch #Innovation #TechSolutions""",
        
        'Company Culture': """🏢 Life at [Company Name]

We believe that great work happens when people feel valued and supported. Here's what makes our culture special:

🌟 Our values:
• [Value 1]
• [Value 2]
• [Value 3]

We're always looking for passionate individuals to join our team. Check out our open positions: [link]

#CompanyCulture #Hiring #TeamWork""",
        
        'Industry Leadership': """📊 [Company Name] Industry Report

Our latest research reveals interesting trends in [industry]:

Key findings:
• [Finding 1]
• [Finding 2]
• [Finding 3]

Download the full report: [link]

What trends are you seeing in your industry? Share your insights below!

#IndustryReport #Leadership #Insights"""
    }
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'post_history' not in st.session_state:
        st.session_state.post_history = []
    if 'scheduled_posts' not in st.session_state:
        st.session_state.scheduled_posts = []
    if 'draft_posts' not in st.session_state:
        st.session_state.draft_posts = []

def save_post_to_history(post_type, content, target, status='Published'):
    """Save post to history"""
    post_entry = {
        'id': len(st.session_state.post_history) + 1,
        'type': post_type,
        'content': content[:100] + '...' if len(content) > 100 else content,
        'target': target,
        'status': status,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'engagement': {
            'likes': random.randint(5, 150),
            'comments': random.randint(0, 25),
            'shares': random.randint(0, 15)
        }
    }
    st.session_state.post_history.append(post_entry)

def schedule_post(post_type, content, target, schedule_time):
    """Schedule a post"""
    scheduled_entry = {
        'id': len(st.session_state.scheduled_posts) + 1,
        'type': post_type,
        'content': content[:100] + '...' if len(content) > 100 else content,
        'target': target,
        'schedule_time': schedule_time,
        'status': 'Scheduled'
    }
    st.session_state.scheduled_posts.append(scheduled_entry)

def save_draft(post_type, content, target):
    """Save post as draft"""
    draft_entry = {
        'id': len(st.session_state.draft_posts) + 1,
        'type': post_type,
        'content': content,
        'target': target,
        'saved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    st.session_state.draft_posts.append(draft_entry)

def demo_post_personal(content, image_path=None, schedule_time=None):
    """Demo function for personal posting"""
    time.sleep(2)  # Simulate processing time
    
    if schedule_time:
        schedule_post('Personal', content, 'Personal Profile', schedule_time)
        return True, "Post scheduled successfully!"
    else:
        save_post_to_history('Personal', content, 'Personal Profile')
        return True, "Post published successfully!"

def demo_post_company(content, company_name, image_path=None, schedule_time=None):
    """Demo function for company posting"""
    time.sleep(2)  # Simulate processing time
    
    if schedule_time:
        schedule_post('Company', content, company_name, schedule_time)
        return True, f"Post scheduled for {company_name} successfully!"
    else:
        save_post_to_history('Company', content, company_name)
        return True, f"Post published to {company_name} successfully!"

def main():
    """Main Content Creator page"""
    st.markdown('<div class="demo-banner">🎭 DEMO: Content Creator</div>', unsafe_allow_html=True)
    
    st.title("📝 Content Creator")
    st.markdown("Create and schedule posts for your personal profile and company pages.")
    
    initialize_session_state()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Create Post", "📅 Scheduled Posts", "📋 Drafts", "📊 Post Analytics"])
    
    with tab1:
        st.subheader("Create New Post")
        
        # Post type selection
        post_type = st.selectbox(
            "Select Post Type",
            ["Personal Profile", "Company Page"],
            help="Choose whether to post to your personal profile or a company page"
        )
        
        # Company selection for company posts
        if post_type == "Company Page":
            st.subheader("Select Company")
            
            # Display managed companies
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Your Managed Companies:**")
                selected_company = st.selectbox(
                    "Choose company",
                    options=[f"{comp['name']} ({comp['followers']} followers)" for comp in DEMO_COMPANIES],
                    help="Select the company page you want to post to"
                )
                
                if selected_company:
                    company_name = selected_company.split(' (')[0]
                    company_data = next((comp for comp in DEMO_COMPANIES if comp['name'] == company_name), None)
                    
                    if company_data:
                        st.info(f"**{company_data['name']}**\nFollowers: {company_data['followers']}\nIndustry: {company_data['industry']}")
            
            with col2:
                st.markdown("**Quick Actions:**")
                if st.button("🔄 Refresh Company List"):
                    st.success("Company list refreshed!")
                
                if st.button("➕ Add New Company"):
                    st.info("This would open the company page setup dialog.")
        
        # Content creation area
        st.subheader("Post Content")
        
        # Template selection
        template_category = 'Personal' if post_type == "Personal Profile" else 'Company'
        template_type = st.selectbox(
            "Use Template (Optional)",
            ["None"] + list(POST_TEMPLATES[template_category].keys()),
            help="Select a pre-made template to get started"
        )
        
        # Content input
        if template_type != "None":
            default_content = POST_TEMPLATES[template_category][template_type]
            st.info(f"Using template: {template_type}")
        else:
            default_content = ""
        
        content = st.text_area(
            "Write your post content",
            value=default_content,
            height=200,
            help="Write your post content here. Use emojis and hashtags to increase engagement."
        )
        
        # Character count
        char_count = len(content)
        if char_count > 1300:
            st.warning(f"Character count: {char_count}/1300 - Consider shortening your post")
        else:
            st.info(f"Character count: {char_count}/1300")
        
        # Media upload
        st.subheader("Media (Optional)")
        uploaded_file = st.file_uploader(
            "Upload image",
            type=['jpg', 'jpeg', 'png', 'gif'],
            help="Upload an image to include with your post"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_column_width=True)
        
        # Post options
        st.subheader("Post Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scheduling
            schedule_option = st.checkbox("Schedule for later")
            
            if schedule_option:
                schedule_date = st.date_input(
                    "Schedule Date",
                    min_value=datetime.now().date(),
                    value=datetime.now().date()
                )
                schedule_time = st.time_input(
                    "Schedule Time",
                    value=datetime.now().time()
                )
                
                schedule_datetime = datetime.combine(schedule_date, schedule_time)
                st.info(f"Post will be published on: {schedule_datetime.strftime('%Y-%m-%d at %H:%M')}")
        
        with col2:
            # Additional options
            notify_connections = st.checkbox("Notify connections", value=True)
            allow_comments = st.checkbox("Allow comments", value=True)
            
            if post_type == "Company Page":
                employee_advocacy = st.checkbox("Enable employee advocacy", help="Allow employees to share this post")
        
        # Action buttons
        st.subheader("Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📝 Save as Draft", use_container_width=True):
                if content:
                    target = selected_company.split(' (')[0] if post_type == "Company Page" else "Personal Profile"
                    save_draft(post_type, content, target)
                    st.success("Draft saved successfully!")
                else:
                    st.error("Please enter some content first.")
        
        with col2:
            if st.button("👁️ Preview", use_container_width=True):
                if content:
                    st.subheader("Post Preview")
                    st.markdown("---")
                    
                    # Show post preview
                    if post_type == "Company Page":
                        st.markdown(f"**{selected_company.split(' (')[0]}**")
                    else:
                        st.markdown("**Your Name**")
                    
                    st.markdown(content)
                    
                    if uploaded_file:
                        st.image(uploaded_file, use_column_width=True)
                    
                    st.markdown("---")
                    st.markdown("👍 Like | 💬 Comment | 📤 Share")
                else:
                    st.error("Please enter some content first.")
        
        with col3:
            if schedule_option:
                if st.button("⏰ Schedule Post", use_container_width=True):
                    if content:
                        target = selected_company.split(' (')[0] if post_type == "Company Page" else "Personal Profile"
                        
                        # Demo posting
                        if post_type == "Personal Profile":
                            success, message = demo_post_personal(content, uploaded_file, schedule_datetime)
                        else:
                            success, message = demo_post_company(content, target, uploaded_file, schedule_datetime)
                        
                        if success:
                            st.success(message)
                            st.balloons()
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter some content first.")
            else:
                # Publish now button
                if st.button("🚀 Publish Now", use_container_width=True):
                    if content:
                        target = selected_company.split(' (')[0] if post_type == "Company Page" else "Personal Profile"
                        
                        # Demo posting
                        if post_type == "Personal Profile":
                            success, message = demo_post_personal(content, uploaded_file)
                        else:
                            success, message = demo_post_company(content, target, uploaded_file)
                        
                        if success:
                            st.success(message)
                            st.balloons()
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter some content first.")
        
        with col4:
            if st.button("🗑️ Clear Form", use_container_width=True):
                st.rerun()
    
    with tab2:
        st.subheader("📅 Scheduled Posts")
        
        if st.session_state.scheduled_posts:
            for post in st.session_state.scheduled_posts:
                with st.expander(f"{post['type']} - {post['target']} (Scheduled: {post['schedule_time']})"):
                    st.write(f"**Content:** {post['content']}")
                    st.write(f"**Status:** {post['status']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📝 Edit", key=f"edit_{post['id']}"):
                            st.info("Edit functionality would open here.")
                    
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_{post['id']}"):
                            st.session_state.scheduled_posts.remove(post)
                            st.rerun()
        else:
            st.info("No scheduled posts. Create a post and select 'Schedule for later' to see them here.")
    
    with tab3:
        st.subheader("📋 Draft Posts")
        
        if st.session_state.draft_posts:
            for draft in st.session_state.draft_posts:
                with st.expander(f"{draft['type']} - {draft['target']} (Saved: {draft['saved_at']})"):
                    st.write(f"**Content:** {draft['content'][:200]}...")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📝 Edit", key=f"edit_draft_{draft['id']}"):
                            st.info("Edit functionality would open here.")
                    
                    with col2:
                        if st.button(f"🚀 Publish", key=f"publish_draft_{draft['id']}"):
                            save_post_to_history(draft['type'], draft['content'], draft['target'])
                            st.session_state.draft_posts.remove(draft)
                            st.success("Draft published successfully!")
                            st.rerun()
                    
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_draft_{draft['id']}"):
                            st.session_state.draft_posts.remove(draft)
                            st.rerun()
        else:
            st.info("No draft posts. Save a post as draft to see them here.")
    
    with tab4:
        st.subheader("📊 Post Analytics")
        
        if st.session_state.post_history:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_posts = len(st.session_state.post_history)
            total_likes = sum(post['engagement']['likes'] for post in st.session_state.post_history)
            total_comments = sum(post['engagement']['comments'] for post in st.session_state.post_history)
            total_shares = sum(post['engagement']['shares'] for post in st.session_state.post_history)
            
            with col1:
                st.metric("Total Posts", total_posts)
            with col2:
                st.metric("Total Likes", total_likes)
            with col3:
                st.metric("Total Comments", total_comments)
            with col4:
                st.metric("Total Shares", total_shares)
            
            # Recent posts table
            st.subheader("Recent Posts Performance")
            
            for post in reversed(st.session_state.post_history[-10:]):  # Show last 10 posts
                with st.expander(f"{post['type']} - {post['target']} ({post['timestamp']})"):
                    st.write(f"**Content:** {post['content']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Likes", post['engagement']['likes'])
                    with col2:
                        st.metric("Comments", post['engagement']['comments'])
                    with col3:
                        st.metric("Shares", post['engagement']['shares'])
                    
                    # Engagement rate
                    total_engagement = post['engagement']['likes'] + post['engagement']['comments'] + post['engagement']['shares']
                    st.write(f"**Total Engagement:** {total_engagement}")
        else:
            st.info("No posts published yet. Create and publish a post to see analytics here.")
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tips for better engagement:**")
    st.markdown("• Use relevant hashtags • Include images • Post at optimal times • Engage with comments")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

def load_historical_data():
    """Load or generate historical data for analytics"""
    # In a real implementation, this would load from a database or files
    # For demo purposes, we'll generate sample data
    
    if 'historical_data' not in st.session_state:
        # Generate sample historical data
        dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
        
        st.session_state.historical_data = {
            'daily_connections': {
                date.strftime('%Y-%m-%d'): max(0, 30 + (i % 10) - 5) 
                for i, date in enumerate(dates)
            },
            'daily_success_rate': {
                date.strftime('%Y-%m-%d'): 75 + (i % 20)
                for i, date in enumerate(dates)
            },
            'daily_profile_views': {
                date.strftime('%Y-%m-%d'): max(0, 80 + (i % 15) - 10)
                for i, date in enumerate(dates)
            },
            'industry_breakdown': {
                'Technology': 35,
                'Finance': 20,
                'Healthcare': 15,
                'Marketing': 12,
                'Sales': 10,
                'Others': 8
            },
            'location_breakdown': {
                'San Francisco': 25,
                'New York': 20,
                'Los Angeles': 15,
                'Seattle': 12,
                'Chicago': 10,
                'Boston': 8,
                'Others': 10
            }
        }
    
    return st.session_state.historical_data

def create_daily_activity_chart():
    """Create daily activity chart"""
    data = load_historical_data()
    
    dates = list(data['daily_connections'].keys())
    connections = list(data['daily_connections'].values())
    profile_views = list(data['daily_profile_views'].values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=connections,
        mode='lines+markers',
        name='Connections Sent',
        line=dict(color='#0077B5', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=profile_views,
        mode='lines+markers',
        name='Profiles Viewed',
        line=dict(color='#00A0DC', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Daily Activity Trends (Last 30 Days)",
        xaxis_title="Date",
        yaxis_title="Count",
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_success_rate_chart():
    """Create success rate chart"""
    data = load_historical_data()
    
    dates = list(data['daily_success_rate'].keys())
    success_rates = list(data['daily_success_rate'].values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=success_rates,
        mode='lines+markers',
        name='Success Rate',
        line=dict(color='#28a745', width=3),
        marker=dict(size=6),
        fill='tonexty'
    ))
    
    # Add average line
    avg_success = sum(success_rates) / len(success_rates)
    fig.add_hline(
        y=avg_success, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Average: {avg_success:.1f}%"
    )
    
    fig.update_layout(
        title="Connection Request Success Rate",
        xaxis_title="Date",
        yaxis_title="Success Rate (%)",
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_industry_breakdown_chart():
    """Create industry breakdown pie chart"""
    data = load_historical_data()
    industry_data = data['industry_breakdown']
    
    fig = px.pie(
        values=list(industry_data.values()),
        names=list(industry_data.keys()),
        title="Target Industries Breakdown",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig

def create_location_breakdown_chart():
    """Create location breakdown bar chart"""
    data = load_historical_data()
    location_data = data['location_breakdown']
    
    fig = px.bar(
        x=list(location_data.keys()),
        y=list(location_data.values()),
        title="Target Locations Distribution",
        color=list(location_data.values()),
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title="Location",
        yaxis_title="Count",
        height=400,
        showlegend=False
    )
    
    return fig

def calculate_performance_metrics():
    """Calculate key performance metrics"""
    # Get current session data
    daily_stats = st.session_state.get('daily_stats', {
        'connections_sent': 0,
        'messages_sent': 0,
        'profiles_viewed': 0
    })
    
    connection_history = st.session_state.get('connection_history', [])
    search_history = st.session_state.get('search_history', [])
    
    # Calculate metrics
    total_connections = len(connection_history)
    successful_connections = len([h for h in connection_history if h.get('status') == 'Sent'])
    success_rate = (successful_connections / total_connections * 100) if total_connections > 0 else 0
    
    total_searches = len(search_history)
    avg_results_per_search = sum(h.get('results_count', 0) for h in search_history) / total_searches if total_searches > 0 else 0
    
    # Today's activity
    today = datetime.now().strftime('%Y-%m-%d')
    today_connections = len([h for h in connection_history if h.get('sent_at', '').startswith(today)])
    
    return {
        'daily_connections': daily_stats['connections_sent'],
        'daily_profiles_viewed': daily_stats['profiles_viewed'],
        'total_connections': total_connections,
        'success_rate': success_rate,
        'total_searches': total_searches,
        'avg_results_per_search': avg_results_per_search,
        'today_connections': today_connections
    }

def main():
    st.title("📊 Analytics Dashboard")
    st.markdown("Track your LinkedIn automation performance and insights.")
    
    # Load data
    load_historical_data()
    metrics = calculate_performance_metrics()
    
    # Key Metrics Overview
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Today's Connections",
            metrics['daily_connections'],
            delta=f"+{metrics['today_connections'] - metrics['daily_connections']}" if metrics['today_connections'] != metrics['daily_connections'] else None
        )
    
    with col2:
        st.metric(
            "Success Rate",
            f"{metrics['success_rate']:.1f}%",
            delta=f"+{metrics['success_rate'] - 85:.1f}%" if metrics['success_rate'] > 85 else f"{metrics['success_rate'] - 85:.1f}%"
        )
    
    with col3:
        st.metric(
            "Total Connections",
            metrics['total_connections'],
            delta=f"+{metrics['today_connections']}" if metrics['today_connections'] > 0 else None
        )
    
    with col4:
        st.metric(
            "Profiles Viewed",
            metrics['daily_profiles_viewed'],
            delta=None
        )
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily Activity Chart
        daily_chart = create_daily_activity_chart()
        st.plotly_chart(daily_chart, use_container_width=True)
        
        # Industry Breakdown
        industry_chart = create_industry_breakdown_chart()
        st.plotly_chart(industry_chart, use_container_width=True)
    
    with col2:
        # Success Rate Chart
        success_chart = create_success_rate_chart()
        st.plotly_chart(success_chart, use_container_width=True)
        
        # Location Breakdown
        location_chart = create_location_breakdown_chart()
        st.plotly_chart(location_chart, use_container_width=True)
    
    # Detailed Analytics
    st.markdown("---")
    st.subheader("🔍 Detailed Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Performance Trends", "Search Analytics", "Connection Analysis", "Reports"])
    
    with tab1:
        st.markdown("### Performance Trends")
        
        # Daily limits progress
        st.markdown("#### Daily Limits Progress")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Connections progress
            connections_progress = metrics['daily_connections'] / 50  # 50 is daily limit
            st.metric("Connections", f"{metrics['daily_connections']}/50")
            st.progress(connections_progress)
        
        with col2:
            # Profile views progress
            views_progress = metrics['daily_profiles_viewed'] / 100  # 100 is daily limit
            st.metric("Profile Views", f"{metrics['daily_profiles_viewed']}/100")
            st.progress(views_progress)
        
        with col3:
            # Messages progress (assuming 0 for now)
            messages_sent = st.session_state.get('daily_stats', {}).get('messages_sent', 0)
            messages_progress = messages_sent / 20  # 20 is daily limit
            st.metric("Messages", f"{messages_sent}/20")
            st.progress(messages_progress)
        
        # Weekly performance comparison
        st.markdown("#### Weekly Performance")
        
        # Generate mock weekly data
        week_data = {
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Connections': [25, 30, 28, 35, 32, 20, 15],
            'Success Rate': [85, 90, 82, 95, 88, 78, 80]
        }
        
        week_df = pd.DataFrame(week_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=week_df['Day'],
            y=week_df['Connections'],
            name='Connections',
            marker_color='#0077B5'
        ))
        
        fig.update_layout(
            title="Weekly Connections Overview",
            xaxis_title="Day of Week",
            yaxis_title="Connections",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Search Analytics")
        
        search_history = st.session_state.get('search_history', [])
        
        if search_history:
            # Search history table
            search_df = pd.DataFrame(search_history)
            st.dataframe(search_df, use_container_width=True)
            
            # Top keywords analysis
            all_keywords = []
            for search in search_history:
                keywords = search.get('keywords', '').lower().split()
                all_keywords.extend(keywords)
            
            if all_keywords:
                from collections import Counter
                keyword_counts = Counter(all_keywords)
                top_keywords = keyword_counts.most_common(10)
                
                if top_keywords:
                    keywords_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Count'])
                    
                    fig = px.bar(
                        keywords_df,
                        x='Keyword',
                        y='Count',
                        title="Most Searched Keywords",
                        color='Count',
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No search history available. Perform some searches to see analytics here.")
    
    with tab3:
        st.markdown("### Connection Analysis")
        
        connection_history = st.session_state.get('connection_history', [])
        
        if connection_history:
            # Connection history table
            history_df = pd.DataFrame(connection_history)
            
            # Connection status distribution
            if 'status' in history_df.columns:
                status_counts = history_df['status'].value_counts()
                
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Connection Request Status Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Template type effectiveness
            if 'template_type' in history_df.columns:
                template_success = history_df.groupby('template_type')['status'].apply(
                    lambda x: (x == 'Sent').sum() / len(x) * 100
                ).reset_index()
                template_success.columns = ['Template Type', 'Success Rate']
                
                fig = px.bar(
                    template_success,
                    x='Template Type',
                    y='Success Rate',
                    title="Message Template Effectiveness",
                    color='Success Rate',
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent connections table
            st.markdown("#### Recent Connections")
            recent_connections = history_df.tail(10) if len(history_df) > 10 else history_df
            st.dataframe(recent_connections[['profile_url', 'template_type', 'status', 'sent_at']], use_container_width=True)
            
        else:
            st.info("No connection history available. Send some connection requests to see analytics here.")
    
    with tab4:
        st.markdown("### Reports & Export")
        
        # Generate comprehensive report
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Generate Reports")
            
            report_type = st.selectbox(
                "Report Type",
                ["Daily Summary", "Weekly Performance", "Monthly Analytics", "Custom Date Range"]
            )
            
            if report_type == "Custom Date Range":
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
            
            if st.button("📊 Generate Report"):
                # Create a sample report
                report_data = {
                    'Metric': [
                        'Total Connections Sent',
                        'Success Rate',
                        'Profiles Viewed',
                        'Searches Performed',
                        'Average Results per Search'
                    ],
                    'Value': [
                        metrics['total_connections'],
                        f"{metrics['success_rate']:.1f}%",
                        metrics['daily_profiles_viewed'],
                        metrics['total_searches'],
                        f"{metrics['avg_results_per_search']:.1f}"
                    ]
                }
                
                report_df = pd.DataFrame(report_data)
                st.dataframe(report_df, use_container_width=True)
                
                # Download button
                csv = report_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Report",
                    data=csv,
                    file_name=f"linkedin_automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("#### Export Data")
            
            export_options = st.multiselect(
                "Select data to export:",
                ["Connection History", "Search History", "Daily Stats", "Performance Metrics"]
            )
            
            if export_options and st.button("📥 Export Selected Data"):
                export_data = {}
                
                if "Connection History" in export_options:
                    export_data['connection_history'] = st.session_state.get('connection_history', [])
                
                if "Search History" in export_options:
                    export_data['search_history'] = st.session_state.get('search_history', [])
                
                if "Daily Stats" in export_options:
                    export_data['daily_stats'] = st.session_state.get('daily_stats', {})
                
                if "Performance Metrics" in export_options:
                    export_data['performance_metrics'] = metrics
                
                # Convert to JSON for download
                json_data = json.dumps(export_data, indent=2, default=str)
                
                st.download_button(
                    label="📥 Download JSON Export",
                    data=json_data,
                    file_name=f"linkedin_automation_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Insights and Recommendations
    st.markdown("---")
    st.subheader("💡 Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Performance Insights")
        
        # Generate insights based on data
        insights = []
        
        if metrics['success_rate'] > 90:
            insights.append("🟢 Excellent success rate! Your message templates are working well.")
        elif metrics['success_rate'] > 75:
            insights.append("🟡 Good success rate. Consider A/B testing different message templates.")
        else:
            insights.append("🔴 Low success rate. Review your targeting criteria and message personalization.")
        
        if metrics['daily_connections'] < 20:
            insights.append("📈 You're well within daily limits. Consider increasing activity if needed.")
        elif metrics['daily_connections'] > 45:
            insights.append("⚠️ Approaching daily limit. Monitor to avoid restrictions.")
        
        if metrics['total_searches'] > 10:
            insights.append("🔍 High search activity. Consider saving frequent search templates.")
        
        for insight in insights:
            st.write(insight)
    
    with col2:
        st.markdown("#### 🚀 Optimization Tips")
        
        tips = [
            "🎯 **Target Optimization**: Focus on 2nd degree connections for better acceptance rates",
            "💬 **Message Personalization**: Include specific details about the person's background",
            "⏰ **Timing**: Send requests during business hours (9 AM - 5 PM) in target timezone",
            "🔄 **Follow-up**: Plan follow-up messages for accepted connections",
            "📊 **A/B Testing**: Test different message templates to optimize success rates"
        ]
        
        for tip in tips:
            st.write(tip)

if __name__ == "__main__":
    main()
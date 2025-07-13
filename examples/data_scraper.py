#!/usr/bin/env python3
"""
LinkedIn Data Scraper Example

This script demonstrates how to extract and analyze LinkedIn profile data
for research and lead generation purposes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linkedin_bot import LinkedInBot
import time
import random
import pandas as pd
from collections import Counter

def analyze_profiles_data(profiles_data):
    """Analyze extracted profile data and generate insights"""
    if not profiles_data:
        print("No profile data to analyze")
        return
        
    df = pd.DataFrame(profiles_data)
    
    print("\n📊 PROFILE ANALYSIS REPORT")
    print("=" * 50)
    
    # Basic statistics
    print(f"Total profiles analyzed: {len(df)}")
    print(f"Profiles with complete data: {len(df.dropna())}")
    
    # Most common locations
    if 'location' in df.columns:
        locations = df['location'].dropna()
        if len(locations) > 0:
            print(f"\n🌍 TOP LOCATIONS:")
            location_counts = Counter(locations)
            for location, count in location_counts.most_common(5):
                print(f"  {location}: {count}")
    
    # Most common keywords in headlines
    if 'headline' in df.columns:
        headlines = df['headline'].dropna()
        if len(headlines) > 0:
            print(f"\n💼 COMMON HEADLINE KEYWORDS:")
            all_words = []
            for headline in headlines:
                words = headline.lower().split()
                # Filter out common words
                filtered_words = [w for w in words if len(w) > 3 and w not in 
                                ['the', 'and', 'for', 'with', 'from', 'this', 'that', 'your']]
                all_words.extend(filtered_words)
            
            word_counts = Counter(all_words)
            for word, count in word_counts.most_common(10):
                print(f"  {word}: {count}")

def main():
    # Research targets
    research_queries = [
        "startup founder",
        "venture capital",
        "artificial intelligence researcher",
        "blockchain developer",
        "sustainable energy",
        "fintech entrepreneur"
    ]
    
    bot = LinkedInBot(headless=False)
    all_profile_data = []
    
    try:
        bot.start_session()
        
        print("🔐 Logging in to LinkedIn...")
        if not bot.login():
            print("❌ Login failed. Check your credentials.")
            return
        print("✅ Successfully logged in!")
        
        for query in research_queries:
            print(f"\n🔍 Researching: {query}")
            print("-" * 30)
            
            # Search for profiles
            profiles = bot.search_people(query)
            print(f"Found {len(profiles)} profiles")
            
            if not profiles:
                continue
                
            # Limit profiles per query to avoid overwhelming
            limited_profiles = profiles[:10]
            
            for i, profile_url in enumerate(limited_profiles, 1):
                print(f"[{i}/{len(limited_profiles)}] Extracting data from profile...")
                
                # Extract detailed profile data
                profile_data = bot.extract_profile_data(profile_url)
                
                if profile_data and profile_data.get('name'):
                    # Add search query to data for analysis
                    profile_data['search_query'] = query
                    profile_data['extracted_date'] = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    all_profile_data.append(profile_data)
                    print(f"✅ Extracted: {profile_data['name']}")
                else:
                    print("❌ Failed to extract profile data")
                
                # Random delay to be respectful
                delay = random.uniform(3, 7)
                time.sleep(delay)
                
            # Longer delay between different search queries
            if query != research_queries[-1]:  # Not the last query
                print("⏳ Waiting before next search query...")
                time.sleep(random.uniform(10, 20))
                
        print(f"\n📊 Data extraction complete! Collected {len(all_profile_data)} profiles")
        
        if all_profile_data:
            # Save raw data
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = f"linkedin_research_data_{timestamp}.csv"
            bot.save_data_to_csv(all_profile_data, filename)
            print(f"💾 Raw data saved to: data/{filename}")
            
            # Generate analysis report
            analyze_profiles_data(all_profile_data)
            
            # Save analysis summary
            summary_data = []
            for query in research_queries:
                query_profiles = [p for p in all_profile_data if p['search_query'] == query]
                summary_data.append({
                    'search_query': query,
                    'profiles_found': len(query_profiles),
                    'avg_name_length': sum(len(p.get('name', '')) for p in query_profiles) / len(query_profiles) if query_profiles else 0
                })
            
            summary_filename = f"research_summary_{timestamp}.csv"
            bot.save_data_to_csv(summary_data, summary_filename)
            print(f"📋 Summary saved to: data/{summary_filename}")
            
        # Show daily statistics
        stats = bot.get_daily_stats()
        print(f"\n📈 Daily Statistics:")
        print(f"Profiles viewed: {stats['profiles_viewed']}")
        print(f"Connections sent: {stats['connections_sent']}")
        
        # Take a final screenshot
        bot.take_screenshot(f"research_complete_{timestamp}.png")
        
    except KeyboardInterrupt:
        print("\n⚠️  Research interrupted by user")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        bot.close_session()
        print("\n👋 Research session closed")
        
        if all_profile_data:
            print(f"\n🎉 Research complete! Analyzed {len(all_profile_data)} profiles")
            print("Check the data/ folder for exported CSV files")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Bulk Connection Requests Example

This script demonstrates how to send bulk connection requests
with personalized messages and proper rate limiting.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linkedin_bot import LinkedInBot
import time
import random

# Personalized message templates
MESSAGE_TEMPLATES = [
    "Hi {name}! I noticed your expertise in {field} and would love to connect.",
    "Hello {name}! Your background in {field} is impressive. Let's connect!",
    "Hi {name}! I'm also passionate about {field}. Would love to network with you.",
    "Hello {name}! I see we share similar interests in {field}. Let's connect!",
    "Hi {name}! Your work in {field} caught my attention. I'd love to connect."
]

def get_personalized_message(profile_data):
    """Generate a personalized message based on profile data"""
    name = profile_data.get('name', '').split()[0] if profile_data.get('name') else 'there'
    headline = profile_data.get('headline', '')
    
    # Extract field from headline
    field = "technology"  # Default
    if any(word in headline.lower() for word in ['developer', 'engineer', 'programming']):
        field = "software development"
    elif any(word in headline.lower() for word in ['marketing', 'sales']):
        field = "marketing"
    elif any(word in headline.lower() for word in ['data', 'analytics']):
        field = "data science"
    elif any(word in headline.lower() for word in ['design', 'ui', 'ux']):
        field = "design"
    
    template = random.choice(MESSAGE_TEMPLATES)
    return template.format(name=name, field=field)

def main():
    # Search parameters
    search_configs = [
        {"keywords": "python developer", "location": "San Francisco"},
        {"keywords": "data scientist", "location": "New York"},
        {"keywords": "product manager", "location": "Seattle"},
    ]
    
    bot = LinkedInBot(headless=False)
    
    try:
        bot.start_session()
        
        # Login
        print("Logging in to LinkedIn...")
        if not bot.login():
            print("❌ Login failed. Check your credentials.")
            return
            
        print("✅ Successfully logged in!")
        
        all_profiles = []
        
        # Search for profiles with different criteria
        for config in search_configs:
            print(f"\n🔍 Searching for: {config['keywords']} in {config['location']}")
            profiles = bot.search_people(config['keywords'], config['location'])
            all_profiles.extend(profiles)
            print(f"Found {len(profiles)} profiles")
            
            # Random delay between searches
            time.sleep(random.uniform(5, 10))
            
        # Remove duplicates
        unique_profiles = list(set(all_profiles))
        print(f"\n📊 Total unique profiles found: {len(unique_profiles)}")
        
        # Limit to avoid overwhelming
        profiles_to_process = unique_profiles[:20]
        
        successful_requests = 0
        failed_requests = 0
        
        for i, profile_url in enumerate(profiles_to_process, 1):
            print(f"\n[{i}/{len(profiles_to_process)}] Processing profile...")
            
            # Extract profile data first
            profile_data = bot.extract_profile_data(profile_url)
            
            if not profile_data or not profile_data.get('name'):
                print("❌ Could not extract profile data, skipping...")
                failed_requests += 1
                continue
                
            print(f"👤 Profile: {profile_data['name']}")
            print(f"💼 Headline: {profile_data.get('headline', 'N/A')}")
            
            # Generate personalized message
            message = get_personalized_message(profile_data)
            print(f"💬 Message: {message}")
            
            # Send connection request
            success = bot.send_connection_request(profile_url, message)
            
            if success:
                successful_requests += 1
                print("✅ Connection request sent successfully!")
            else:
                failed_requests += 1
                print("❌ Failed to send connection request")
                
            # Check daily limits
            stats = bot.get_daily_stats()
            if stats['connections_sent'] >= 50:  # Daily limit
                print("⚠️  Daily connection limit reached. Stopping...")
                break
                
            # Random delay between requests (important for avoiding detection)
            delay = random.uniform(15, 30)
            print(f"⏳ Waiting {delay:.1f} seconds before next request...")
            time.sleep(delay)
            
        # Final statistics
        print(f"\n📈 Final Results:")
        print(f"✅ Successful requests: {successful_requests}")
        print(f"❌ Failed requests: {failed_requests}")
        print(f"📊 Success rate: {(successful_requests/(successful_requests+failed_requests)*100):.1f}%")
        
        # Show daily stats
        final_stats = bot.get_daily_stats()
        print(f"\n📊 Daily Statistics:")
        print(f"Connections sent: {final_stats['connections_sent']}")
        print(f"Profiles viewed: {final_stats['profiles_viewed']}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Script interrupted by user")
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
    finally:
        bot.close_session()
        print("\n👋 Bot session closed")

if __name__ == "__main__":
    main()
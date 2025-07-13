#!/usr/bin/env python3
"""
Basic LinkedIn Bot Usage Example

This script demonstrates how to use the LinkedIn automation bot
for common tasks like searching people and sending connection requests.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linkedin_bot import LinkedInBot
import time

def main():
    # Initialize the bot (set headless=True to run without GUI)
    bot = LinkedInBot(headless=False)
    
    try:
        # Start browser session
        bot.start_session()
        
        # Login to LinkedIn
        print("Logging in to LinkedIn...")
        if not bot.login():
            print("Login failed. Please check your credentials in .env file")
            return
            
        # Search for people
        print("Searching for people...")
        keywords = "python developer"
        location = "San Francisco"
        profiles = bot.search_people(keywords, location)
        
        print(f"Found {len(profiles)} profiles")
        
        # Send connection requests to first 5 profiles
        connection_message = "Hi! I'd love to connect with fellow Python developers."
        
        for i, profile_url in enumerate(profiles[:5]):
            print(f"Sending connection request to profile {i+1}")
            success = bot.send_connection_request(profile_url, connection_message)
            
            if success:
                print(f"✓ Connection request sent to {profile_url}")
            else:
                print(f"✗ Failed to send connection request to {profile_url}")
                
            # Wait between requests to avoid being flagged
            time.sleep(10)
            
        # Extract data from some profiles
        print("Extracting profile data...")
        profile_data = []
        
        for profile_url in profiles[:3]:
            data = bot.extract_profile_data(profile_url)
            if data:
                profile_data.append(data)
                print(f"✓ Extracted data from {data.get('name', 'Unknown')}")
                
        # Save extracted data
        if profile_data:
            bot.save_data_to_csv(profile_data, "extracted_profiles.csv")
            print("✓ Profile data saved to data/extracted_profiles.csv")
            
        # Like some posts in feed
        print("Liking posts in feed...")
        likes_count = bot.like_posts_in_feed(max_likes=5)
        print(f"✓ Liked {likes_count} posts")
        
        # Show daily statistics
        stats = bot.get_daily_stats()
        print("\nDaily Statistics:")
        print(f"Connections sent: {stats['connections_sent']}")
        print(f"Messages sent: {stats['messages_sent']}")
        print(f"Profiles viewed: {stats['profiles_viewed']}")
        
        # Take a screenshot
        bot.take_screenshot("final_screenshot.png")
        print("✓ Screenshot saved")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
    finally:
        # Always close the browser session
        bot.close_session()
        print("Bot session closed")

if __name__ == "__main__":
    main()
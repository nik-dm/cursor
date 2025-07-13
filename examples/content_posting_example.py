#!/usr/bin/env python3
"""
LinkedIn Content Posting Example

This script demonstrates how to use the LinkedIn bot's posting functionality
for both personal profiles and company pages.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from linkedin_bot import LinkedInBot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main function to demonstrate posting functionality"""
    
    # Initialize the bot
    print("🤖 Initializing LinkedIn Bot...")
    bot = LinkedInBot(headless=False)  # Set to True for headless mode
    
    try:
        # Start session and login
        print("\n📱 Starting browser session...")
        bot.start_session()
        
        print("\n🔐 Logging in to LinkedIn...")
        login_success = bot.login()
        
        if not login_success:
            print("❌ Login failed. Please check your credentials.")
            return
        
        print("✅ Successfully logged in!")
        
        # Example 1: Create a personal post
        print("\n" + "="*50)
        print("📝 EXAMPLE 1: Creating a Personal Post")
        print("="*50)
        
        personal_post_content = """🚀 Exciting news to share!

I'm thrilled to announce that I've just completed my LinkedIn automation project. This tool can help professionals manage their LinkedIn presence more efficiently.

Key features:
• Automated connection requests
• Profile data extraction
• Content posting (personal & company pages)
• Analytics and reporting

The journey has been incredible, and I'm grateful for all the support from my network. Looking forward to sharing more updates soon! 💪

#LinkedInAutomation #Python #Automation #TechInnovation #ProfessionalGrowth"""
        
        print(f"Content preview:\n{personal_post_content[:100]}...")
        
        # Post to personal profile
        success = bot.create_personal_post(
            content=personal_post_content,
            image_path=None,  # Add image path if you have one
            schedule_time=None  # Post immediately
        )
        
        if success:
            print("✅ Personal post created successfully!")
        else:
            print("❌ Failed to create personal post.")
        
        # Example 2: Get managed companies
        print("\n" + "="*50)
        print("🏢 EXAMPLE 2: Getting Managed Companies")
        print("="*50)
        
        companies = bot.get_managed_companies()
        
        if companies:
            print(f"Found {len(companies)} managed companies:")
            for i, company in enumerate(companies, 1):
                print(f"{i}. {company['name']} - {company['url']}")
        else:
            print("No managed companies found or user doesn't have admin access.")
        
        # Example 3: Create a company post (if companies are available)
        if companies:
            print("\n" + "="*50)
            print("🏢 EXAMPLE 3: Creating a Company Post")
            print("="*50)
            
            # Use the first company for the example
            company = companies[0]
            
            company_post_content = f"""🎉 We're excited to announce the launch of our new LinkedIn automation toolkit!

After months of development, we're proud to introduce a comprehensive solution that helps businesses:

✨ Key features:
• Automated networking and outreach
• Advanced profile data extraction
• Multi-platform content posting
• Real-time analytics and reporting
• Enterprise-grade security

This tool is designed to help businesses scale their LinkedIn presence while maintaining authentic connections.

Interested in learning more? Visit our website or drop us a message!

#TechInnovation #LinkedInAutomation #BusinessGrowth #SaaS #Productivity"""
            
            print(f"Posting to company: {company['name']}")
            print(f"Content preview:\n{company_post_content[:100]}...")
            
            success = bot.create_company_post(
                company_page_url=company['url'],
                content=company_post_content,
                image_path=None,  # Add image path if you have one
                schedule_time=None  # Post immediately
            )
            
            if success:
                print("✅ Company post created successfully!")
            else:
                print("❌ Failed to create company post.")
        
        # Example 4: Advanced posting with scheduling
        print("\n" + "="*50)
        print("⏰ EXAMPLE 4: Scheduling a Post")
        print("="*50)
        
        scheduled_content = """💡 Weekly Tech Insights

Here are some interesting trends I've been observing in the automation space:

1. AI-powered social media management is becoming mainstream
2. Businesses are prioritizing authentic engagement over volume
3. Privacy-first automation tools are gaining traction

What trends are you seeing in your industry? I'd love to hear your thoughts!

#TechTrends #Automation #AI #DigitalTransformation #Innovation"""
        
        print(f"Scheduling post for future publication...")
        print(f"Content preview:\n{scheduled_content[:100]}...")
        
        # Note: In a real scenario, you would format the schedule_time properly
        # For this example, we'll just show the concept
        schedule_time = "2024-01-15 09:00:00"  # Format: YYYY-MM-DD HH:MM:SS
        
        success = bot.create_personal_post(
            content=scheduled_content,
            image_path=None,
            schedule_time=schedule_time
        )
        
        if success:
            print(f"✅ Post scheduled successfully for {schedule_time}")
        else:
            print("❌ Failed to schedule post.")
        
        # Example 5: Post with image
        print("\n" + "="*50)
        print("🖼️ EXAMPLE 5: Posting with Image")
        print("="*50)
        
        # Check if there's an example image
        image_path = Path(__file__).parent / "sample_image.jpg"
        
        if image_path.exists():
            image_post_content = """🎨 Visual storytelling in action!

Sometimes a picture really is worth a thousand words. This image represents the power of automation in transforming how we work and connect.

What's your favorite way to communicate complex ideas visually?

#VisualStorytelling #Automation #Communication #LinkedInTips"""
            
            print(f"Posting with image: {image_path}")
            print(f"Content preview:\n{image_post_content[:100]}...")
            
            success = bot.create_personal_post(
                content=image_post_content,
                image_path=str(image_path),
                schedule_time=None
            )
            
            if success:
                print("✅ Image post created successfully!")
            else:
                print("❌ Failed to create image post.")
        else:
            print("ℹ️ No sample image found. Skipping image post example.")
            print("  To test image posting, add a sample image at: examples/sample_image.jpg")
        
        print("\n" + "="*50)
        print("📊 SUMMARY")
        print("="*50)
        print("✅ Demonstrated personal post creation")
        print("✅ Showed company discovery and posting")
        print("✅ Explained post scheduling concepts")
        print("✅ Covered image posting functionality")
        print("\n💡 All posting features are now available in the UI dashboard!")
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        
    finally:
        # Always close the session
        print("\n🔒 Closing browser session...")
        bot.close_session()
        print("✅ Session closed successfully!")

def create_sample_posts():
    """Create sample post templates for different use cases"""
    
    sample_posts = {
        "personal": {
            "professional_update": """🚀 Exciting career milestone!

I'm thrilled to share that I've just completed my latest project on LinkedIn automation. This experience has taught me so much about:

• Building scalable automation systems
• Maintaining authentic engagement
• Balancing efficiency with personal touch

The journey has been challenging but incredibly rewarding. Grateful for all the support from my network!

What's the most impactful project you've worked on recently? I'd love to hear about it!

#CareerGrowth #Automation #TechProjects #ProfessionalDevelopment""",
            
            "industry_insights": """💡 Thoughts on the future of workplace automation

After working extensively with LinkedIn automation tools, I've observed some fascinating trends:

1. **Human-AI collaboration** is becoming the norm, not the exception
2. **Ethical automation** is gaining priority over pure efficiency
3. **Personalization at scale** is the new competitive advantage

The key isn't replacing human connection—it's enhancing it.

What's your take on automation in professional networking? Are you seeing similar trends in your industry?

#FutureOfWork #Automation #AI #ProfessionalNetworking #TechTrends""",
            
            "team_appreciation": """👏 Shoutout to an incredible team!

Working on our LinkedIn automation project has been an absolute pleasure, thanks to these amazing colleagues:

• **Sarah** - Her UI/UX expertise made our dashboard intuitive and beautiful
• **Mike** - His backend architecture skills ensured scalability and reliability  
• **Lisa** - Her testing approach caught edge cases we never would have found

Success is truly a team sport. Grateful to work with such talented individuals!

Who's someone in your network that deserves recognition? Tag them below! 👇

#TeamWork #Gratitude #Collaboration #Success #ProfessionalAppreciation"""
        },
        
        "company": {
            "product_launch": """🎉 Introducing our new LinkedIn Automation Suite!

After months of development and testing, we're excited to launch a comprehensive solution that helps businesses:

✨ **Key Features:**
• Intelligent connection management
• Advanced profile analytics
• Multi-platform content scheduling
• Real-time engagement insights
• Enterprise-grade security

Our beta users have seen:
📈 40% increase in meaningful connections
⏰ 60% time savings on LinkedIn management
🎯 3x improvement in content engagement

Ready to transform your LinkedIn strategy? Learn more at [website link]

#ProductLaunch #LinkedInAutomation #BusinessGrowth #TechInnovation #SaaS""",
            
            "company_culture": """🏢 What makes our company culture special?

At [Company Name], we believe that innovation happens when people feel empowered to be their authentic selves. Here's what drives our culture:

🌟 **Our Core Values:**
• **Curiosity over certainty** - We embrace questions and experimentation
• **Collaboration over competition** - Success is a team achievement
• **Impact over hours** - We measure contribution, not time spent
• **Growth over perfection** - Learning from failures is part of our DNA

We're always looking for passionate individuals who share these values. Currently hiring for:
• Senior Software Engineers
• Product Managers
• UX Designers

Check out our careers page: [link]

#CompanyCulture #Hiring #TechCareers #Innovation #TeamValues""",
            
            "thought_leadership": """📊 Industry Report: The State of LinkedIn Automation in 2024

Our latest research surveyed 1,000+ professionals about their LinkedIn automation usage. Key findings:

📈 **Usage Trends:**
• 67% use some form of automation tool
• 45% automate connection requests
• 32% schedule content in advance
• 28% use AI for message personalization

🎯 **Success Metrics:**
• Companies using automation see 2.3x more profile views
• Automated outreach has 18% higher response rates when personalized
• 78% report time savings of 5+ hours per week

⚠️ **Challenges:**
• 42% worry about appearing inauthentic
• 35% struggle with LinkedIn's changing policies
• 29% find it difficult to maintain personal touch

The future lies in intelligent automation that enhances human connection rather than replacing it.

Download our full report: [link]

What's your experience with LinkedIn automation? Share your insights below!

#LinkedInAutomation #IndustryReport #TechTrends #DigitalMarketing #ThoughtLeadership"""
        }
    }
    
    return sample_posts

if __name__ == "__main__":
    print("LinkedIn Content Posting Example")
    print("=" * 50)
    print("This example demonstrates posting to both personal and company LinkedIn pages.")
    print("Make sure to set your LinkedIn credentials in the .env file before running.")
    print("=" * 50)
    
    # Show sample posts
    print("\n📝 Sample post templates available:")
    samples = create_sample_posts()
    
    for category, posts in samples.items():
        print(f"\n{category.upper()} POSTS:")
        for post_type, content in posts.items():
            print(f"• {post_type.replace('_', ' ').title()}")
    
    print("\n🚀 Starting the posting demonstration...")
    main()
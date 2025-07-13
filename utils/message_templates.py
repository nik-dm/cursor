"""
Message Templates and Personalization Utilities

This module provides various message templates and utilities for creating
personalized LinkedIn connection requests and messages.
"""

import random
from typing import Dict, List

# Connection request templates
CONNECTION_TEMPLATES = {
    'professional': [
        "Hi {name}! I noticed your expertise in {field} and would love to connect with a fellow professional.",
        "Hello {name}! Your background in {field} is impressive. I'd love to add you to my professional network.",
        "Hi {name}! I see we both work in {field}. Would love to connect and share insights.",
        "Hello {name}! I'm always looking to connect with talented {field} professionals like yourself.",
    ],
    
    'industry_specific': [
        "Hi {name}! Fellow {field} professional here. Would love to connect and potentially collaborate.",
        "Hello {name}! I'm passionate about {field} and would love to connect with someone with your experience.",
        "Hi {name}! Your work in {field} caught my attention. Let's connect and share industry insights.",
        "Hello {name}! I see we share similar interests in {field}. Would love to expand my network with you.",
    ],
    
    'casual': [
        "Hi {name}! Love your work in {field}. Let's connect!",
        "Hello {name}! Would love to have you in my network. Let's connect!",
        "Hi {name}! Always great to meet fellow {field} enthusiasts. Connect?",
        "Hello {name}! Your {field} background looks fascinating. Let's connect!",
    ],
    
    'mutual_connection': [
        "Hi {name}! I see we have mutual connections in {field}. Would love to connect with you too!",
        "Hello {name}! Noticed we have shared connections. Would love to expand our network together.",
        "Hi {name}! Our mutual connections speak highly of professionals in {field}. Let's connect!",
    ],
    
    'educational': [
        "Hi {name}! I'm always learning about {field} and would love to connect with an expert like you.",
        "Hello {name}! Your expertise in {field} is impressive. Would love to learn from your experience.",
        "Hi {name}! I'm passionate about growing in {field} and would value connecting with you.",
    ]
}

# Industry/field mappings
FIELD_MAPPINGS = {
    'software': ['software development', 'programming', 'coding', 'tech'],
    'data': ['data science', 'analytics', 'machine learning', 'AI'],
    'marketing': ['digital marketing', 'marketing', 'growth', 'branding'],
    'sales': ['sales', 'business development', 'revenue', 'partnerships'],
    'product': ['product management', 'product development', 'innovation'],
    'design': ['UX/UI design', 'design', 'user experience', 'creative'],
    'finance': ['finance', 'accounting', 'investment', 'fintech'],
    'consulting': ['consulting', 'strategy', 'advisory', 'management'],
    'healthcare': ['healthcare', 'medical', 'biotech', 'pharmaceuticals'],
    'education': ['education', 'teaching', 'training', 'academia'],
    'engineering': ['engineering', 'technical', 'systems', 'infrastructure'],
    'startup': ['entrepreneurship', 'startup', 'innovation', 'venture']
}

def extract_field_from_headline(headline: str) -> str:
    """Extract relevant field from LinkedIn headline"""
    if not headline:
        return "technology"
    
    headline_lower = headline.lower()
    
    # Check for specific field keywords
    for field, keywords in FIELD_MAPPINGS.items():
        if any(keyword in headline_lower for keyword in keywords):
            return keywords[0]  # Return the primary term
    
    # Default fallback
    return "your field"

def get_connection_message(
    profile_data: Dict, 
    template_type: str = 'professional',
    custom_field: str = None
) -> str:
    """
    Generate a personalized connection message
    
    Args:
        profile_data: Dictionary containing profile information
        template_type: Type of template to use
        custom_field: Override field detection with custom field
        
    Returns:
        Personalized connection message
    """
    # Extract name (first name only)
    name = profile_data.get('name', '').split()[0] if profile_data.get('name') else 'there'
    
    # Determine field
    if custom_field:
        field = custom_field
    else:
        headline = profile_data.get('headline', '')
        field = extract_field_from_headline(headline)
    
    # Select template
    templates = CONNECTION_TEMPLATES.get(template_type, CONNECTION_TEMPLATES['professional'])
    template = random.choice(templates)
    
    # Format message
    try:
        message = template.format(name=name, field=field)
    except KeyError:
        # Fallback if template has unexpected placeholders
        message = f"Hi {name}! Would love to connect with you on LinkedIn."
    
    return message

def get_follow_up_message(profile_data: Dict) -> str:
    """Generate a follow-up message for accepted connections"""
    name = profile_data.get('name', '').split()[0] if profile_data.get('name') else 'there'
    
    follow_up_templates = [
        f"Thanks for connecting, {name}! Looking forward to staying in touch.",
        f"Great to connect with you, {name}! Hope we can share insights in the future.",
        f"Thanks for accepting my connection request, {name}! Excited to be part of your network.",
        f"Appreciate the connection, {name}! Would love to hear about your current projects sometime."
    ]
    
    return random.choice(follow_up_templates)

def validate_message_length(message: str, max_length: int = 300) -> bool:
    """Validate that message meets LinkedIn's requirements"""
    return len(message) <= max_length and len(message) >= 10

def get_industry_specific_template(industry: str) -> List[str]:
    """Get templates specific to an industry"""
    industry_templates = {
        'tech': [
            "Hi {name}! Fellow tech enthusiast here. Love your work in {field}!",
            "Hello {name}! Your technical background in {field} is impressive. Let's connect!",
            "Hi {name}! Always excited to connect with innovative {field} professionals.",
        ],
        'finance': [
            "Hi {name}! Your expertise in {field} caught my attention. Let's connect!",
            "Hello {name}! Fellow finance professional here. Would love to network with you.",
            "Hi {name}! Impressed by your background in {field}. Let's connect!",
        ],
        'healthcare': [
            "Hi {name}! Your work in {field} is inspiring. Would love to connect!",
            "Hello {name}! Fellow healthcare professional here. Let's connect and share insights!",
            "Hi {name}! Your dedication to {field} is admirable. Let's connect!",
        ]
    }
    
    return industry_templates.get(industry.lower(), CONNECTION_TEMPLATES['professional'])

# Example usage and testing
if __name__ == "__main__":
    # Test the message generation
    test_profile = {
        'name': 'John Smith',
        'headline': 'Senior Software Engineer at Tech Company',
        'location': 'San Francisco, CA'
    }
    
    print("Testing message templates:")
    print("=" * 40)
    
    for template_type in CONNECTION_TEMPLATES.keys():
        message = get_connection_message(test_profile, template_type)
        print(f"{template_type.title()}: {message}")
        print(f"Length: {len(message)} characters")
        print(f"Valid: {validate_message_length(message)}")
        print("-" * 40)
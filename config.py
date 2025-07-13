import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LinkedIn credentials (store in .env file)
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    
    # Browser settings
    HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'
    BROWSER_DELAY = int(os.getenv('BROWSER_DELAY', '2'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    
    # Automation limits (to avoid being flagged)
    MAX_CONNECTIONS_PER_DAY = int(os.getenv('MAX_CONNECTIONS_PER_DAY', '50'))
    MAX_MESSAGES_PER_DAY = int(os.getenv('MAX_MESSAGES_PER_DAY', '20'))
    MAX_PROFILE_VIEWS_PER_DAY = int(os.getenv('MAX_PROFILE_VIEWS_PER_DAY', '100'))
    
    # Delays between actions (in seconds)
    MIN_DELAY_BETWEEN_ACTIONS = int(os.getenv('MIN_DELAY_BETWEEN_ACTIONS', '2'))
    MAX_DELAY_BETWEEN_ACTIONS = int(os.getenv('MAX_DELAY_BETWEEN_ACTIONS', '5'))
    
    # LinkedIn URLs
    LINKEDIN_BASE_URL = "https://www.linkedin.com"
    LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"
    LINKEDIN_FEED_URL = "https://www.linkedin.com/feed/"
    
    # File paths
    LOGS_DIR = "logs"
    DATA_DIR = "data"
    SCREENSHOTS_DIR = "screenshots"
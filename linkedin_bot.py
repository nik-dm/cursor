import os
import time
import random
import logging
from typing import List, Optional, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class LinkedInBot:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        
        # Counters for daily limits
        self.connections_sent_today = 0
        self.messages_sent_today = 0
        self.profiles_viewed_today = 0
        
        # Setup logging
        self._setup_logging()
        
        # Create necessary directories
        self._create_directories()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/linkedin_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _create_directories(self):
        """Create necessary directories"""
        directories = ['logs', 'data', 'screenshots']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def _setup_driver(self):
        """Setup Chrome driver with anti-detection features"""
        try:
            options = uc.ChromeOptions()
            
            # Add anti-detection features
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Random user agent
            ua = UserAgent()
            options.add_argument(f"--user-agent={ua.random}")
            
            if self.headless:
                options.add_argument("--headless")
                
            self.driver = uc.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 30)
            self.logger.info("Chrome driver setup successfully")
            
        except Exception as e:
            self.logger.error(f"Error setting up driver: {str(e)}")
            raise
            
    def _random_delay(self, min_seconds: int = 2, max_seconds: int = 5):
        """Add random delay between actions"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def start_session(self):
        """Start browser session"""
        if not self.driver:
            self._setup_driver()
        self.logger.info("Browser session started")
        
    def close_session(self):
        """Close browser session"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser session closed")
            
    def login(self, email: str = None, password: str = None):
        """Login to LinkedIn"""
        if not self.driver:
            self.start_session()
            
        try:
            # Use environment variables if not provided
            email = email or os.getenv('LINKEDIN_EMAIL')
            password = password or os.getenv('LINKEDIN_PASSWORD')
            
            if not email or not password:
                raise ValueError("Email and password must be provided")
                
            self.logger.info("Attempting to login to LinkedIn")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for page to load
            self._random_delay(2, 4)
            
            # Enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.clear()
            email_field.send_keys(email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            self._random_delay(3, 6)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "home" in self.driver.current_url:
                self.is_logged_in = True
                self.logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                self.logger.error("Login failed - redirected to unexpected page")
                return False
                
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False
            
    def search_people(self, keywords: str, location: str = "", connection_level: str = "2nd") -> List[str]:
        """Search for people on LinkedIn"""
        if not self.is_logged_in:
            self.logger.error("Must be logged in to search people")
            return []
            
        try:
            # Navigate to people search
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}"
            if location:
                search_url += f"&origin=FACETED_SEARCH&geoUrn=%5B%22{location}%22%5D"
                
            self.driver.get(search_url)
            self._random_delay(3, 5)
            
            # Scroll to load more results
            self._scroll_page()
            
            # Extract profile URLs
            profile_links = []
            elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
            
            for element in elements:
                href = element.get_attribute('href')
                if '/in/' in href and href not in profile_links:
                    profile_links.append(href)
                    
            self.logger.info(f"Found {len(profile_links)} profiles for keywords: {keywords}")
            return profile_links[:50]  # Limit results
            
        except Exception as e:
            self.logger.error(f"Error searching people: {str(e)}")
            return []
            
    def send_connection_request(self, profile_url: str, message: str = "") -> bool:
        """Send connection request to a profile"""
        if self.connections_sent_today >= int(os.getenv('MAX_CONNECTIONS_PER_DAY', '50')):
            self.logger.warning("Daily connection limit reached")
            return False
            
        try:
            self.driver.get(profile_url)
            self._random_delay(2, 4)
            
            # Click Connect button
            connect_buttons = self.driver.find_elements(By.XPATH, "//button[contains(.,'Connect')]")
            if not connect_buttons:
                self.logger.warning(f"No Connect button found on {profile_url}")
                return False
                
            connect_buttons[0].click()
            self._random_delay(1, 2)
            
            # Add note if message provided
            if message:
                try:
                    add_note_button = self.driver.find_element(By.XPATH, "//button[contains(.,'Add a note')]")
                    add_note_button.click()
                    self._random_delay(1, 2)
                    
                    message_field = self.driver.find_element(By.XPATH, "//textarea")
                    message_field.send_keys(message)
                    self._random_delay(1, 2)
                except:
                    pass  # Note field might not be available
                    
            # Send invitation
            send_button = self.driver.find_element(By.XPATH, "//button[contains(.,'Send')]")
            send_button.click()
            
            self.connections_sent_today += 1
            self.logger.info(f"Connection request sent to {profile_url}")
            self._random_delay(2, 4)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending connection request: {str(e)}")
            return False
            
    def _scroll_page(self):
        """Scroll page to load more content"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self._random_delay(2, 3)
        
    def extract_profile_data(self, profile_url: str) -> Dict:
        """Extract data from a LinkedIn profile"""
        try:
            self.driver.get(profile_url)
            self._random_delay(3, 5)
            
            data = {
                'url': profile_url,
                'name': '',
                'headline': '',
                'location': '',
                'company': '',
                'experience': [],
                'education': []
            }
            
            # Extract name
            try:
                name_element = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]")
                data['name'] = name_element.text.strip()
            except:
                pass
                
            # Extract headline
            try:
                headline_element = self.driver.find_element(By.XPATH, "//div[contains(@class, 'text-body-medium')]")
                data['headline'] = headline_element.text.strip()
            except:
                pass
                
            # Extract location
            try:
                location_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'text-body-small')]")
                data['location'] = location_element.text.strip()
            except:
                pass
                
            self.profiles_viewed_today += 1
            self.logger.info(f"Extracted data from {profile_url}")
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error extracting profile data: {str(e)}")
            return {}
            
    def like_posts_in_feed(self, max_likes: int = 10) -> int:
        """Like posts in LinkedIn feed"""
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            self._random_delay(3, 5)
            
            likes_count = 0
            like_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Like')]")
            
            for button in like_buttons[:max_likes]:
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    likes_count += 1
                    self.logger.info(f"Liked post {likes_count}")
                    self._random_delay(2, 4)
                except:
                    continue
                    
            return likes_count
            
        except Exception as e:
            self.logger.error(f"Error liking posts: {str(e)}")
            return 0
            
    def save_data_to_csv(self, data: List[Dict], filename: str):
        """Save extracted data to CSV file"""
        try:
            df = pd.DataFrame(data)
            filepath = f"data/{filename}"
            df.to_csv(filepath, index=False)
            self.logger.info(f"Data saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            
    def take_screenshot(self, filename: str = None):
        """Take screenshot of current page"""
        try:
            if not filename:
                filename = f"screenshot_{int(time.time())}.png"
            filepath = f"screenshots/{filename}"
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            
    def get_daily_stats(self) -> Dict:
        """Get daily automation statistics"""
        return {
            'connections_sent': self.connections_sent_today,
            'messages_sent': self.messages_sent_today,
            'profiles_viewed': self.profiles_viewed_today
        }
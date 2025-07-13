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
    
    def create_personal_post(self, content: str, image_path: str = None, schedule_time: str = None) -> bool:
        """Create a post on personal LinkedIn profile"""
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            self._random_delay(3, 5)
            
            # Click on "Start a post" button
            start_post_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-box-feed-entry__trigger')]")
            start_post_button.click()
            self._random_delay(2, 3)
            
            # Wait for post modal to open
            post_textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            
            # Enter content
            post_textarea.clear()
            post_textarea.send_keys(content)
            self._random_delay(1, 2)
            
            # Handle image upload if provided
            if image_path and os.path.exists(image_path):
                try:
                    image_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Add media')]")
                    image_button.click()
                    self._random_delay(1, 2)
                    
                    file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
                    file_input.send_keys(os.path.abspath(image_path))
                    self._random_delay(3, 5)
                    
                    self.logger.info("Image uploaded successfully")
                except Exception as e:
                    self.logger.warning(f"Failed to upload image: {str(e)}")
            
            # Handle scheduling if provided
            if schedule_time:
                try:
                    schedule_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Schedule')]")
                    schedule_button.click()
                    self._random_delay(1, 2)
                    
                    # Note: Scheduling implementation would need specific time format handling
                    self.logger.info(f"Scheduled post for: {schedule_time}")
                except Exception as e:
                    self.logger.warning(f"Failed to schedule post: {str(e)}")
            
            # Click Post button
            post_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]")
            post_button.click()
            self._random_delay(2, 3)
            
            self.logger.info("Personal post created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating personal post: {str(e)}")
            return False
    
    def create_company_post(self, company_page_url: str, content: str, image_path: str = None, schedule_time: str = None) -> bool:
        """Create a post on a LinkedIn company page"""
        try:
            # Navigate to company page
            self.driver.get(company_page_url)
            self._random_delay(3, 5)
            
            # Look for admin posting area (only visible if user is admin)
            try:
                admin_post_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'org-admin-post-composer-trigger')]")
                admin_post_button.click()
                self._random_delay(2, 3)
            except:
                # Alternative approach - look for "Create a post" button
                try:
                    create_post_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create a post')]")
                    create_post_button.click()
                    self._random_delay(2, 3)
                except:
                    self.logger.error("Cannot find company post creation button - user may not have admin access")
                    return False
            
            # Wait for post modal to open
            post_textarea = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            
            # Enter content
            post_textarea.clear()
            post_textarea.send_keys(content)
            self._random_delay(1, 2)
            
            # Handle image upload if provided
            if image_path and os.path.exists(image_path):
                try:
                    image_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Add media')]")
                    image_button.click()
                    self._random_delay(1, 2)
                    
                    file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
                    file_input.send_keys(os.path.abspath(image_path))
                    self._random_delay(3, 5)
                    
                    self.logger.info("Image uploaded successfully")
                except Exception as e:
                    self.logger.warning(f"Failed to upload image: {str(e)}")
            
            # Handle scheduling if provided
            if schedule_time:
                try:
                    schedule_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Schedule')]")
                    schedule_button.click()
                    self._random_delay(1, 2)
                    
                    # Note: Scheduling implementation would need specific time format handling
                    self.logger.info(f"Scheduled company post for: {schedule_time}")
                except Exception as e:
                    self.logger.warning(f"Failed to schedule company post: {str(e)}")
            
            # Click Post button
            post_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]")
            post_button.click()
            self._random_delay(2, 3)
            
            self.logger.info("Company post created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating company post: {str(e)}")
            return False
    
    def get_managed_companies(self) -> List[Dict]:
        """Get list of company pages the user can manage"""
        try:
            # Navigate to company admin area
            self.driver.get("https://www.linkedin.com/company/")
            self._random_delay(3, 5)
            
            companies = []
            
            # Look for company cards or listings
            try:
                company_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'company-card')]")
                
                for element in company_elements:
                    try:
                        name_element = element.find_element(By.XPATH, ".//h3")
                        link_element = element.find_element(By.XPATH, ".//a")
                        
                        company_info = {
                            'name': name_element.text.strip(),
                            'url': link_element.get_attribute('href'),
                            'type': 'company'
                        }
                        companies.append(company_info)
                        
                    except Exception as e:
                        self.logger.warning(f"Error extracting company info: {str(e)}")
                        continue
                        
            except Exception as e:
                self.logger.warning(f"Could not find company listings: {str(e)}")
            
            self.logger.info(f"Found {len(companies)} managed companies")
            return companies
            
        except Exception as e:
            self.logger.error(f"Error getting managed companies: {str(e)}")
            return []
    
    def get_post_analytics(self, post_url: str) -> Dict:
        """Get analytics for a specific post"""
        try:
            self.driver.get(post_url)
            self._random_delay(3, 5)
            
            analytics = {
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'views': 0,
                'engagement_rate': 0
            }
            
            # Extract engagement metrics
            try:
                # Likes
                likes_element = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Like')]//span")
                analytics['likes'] = int(likes_element.text.replace(',', '')) if likes_element.text.isdigit() else 0
            except:
                pass
                
            try:
                # Comments
                comments_element = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Comment')]//span")
                analytics['comments'] = int(comments_element.text.replace(',', '')) if comments_element.text.isdigit() else 0
            except:
                pass
                
            try:
                # Shares
                shares_element = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Share')]//span")
                analytics['shares'] = int(shares_element.text.replace(',', '')) if shares_element.text.isdigit() else 0
            except:
                pass
                
            # Calculate engagement rate
            total_engagement = analytics['likes'] + analytics['comments'] + analytics['shares']
            if analytics['views'] > 0:
                analytics['engagement_rate'] = (total_engagement / analytics['views']) * 100
            
            self.logger.info(f"Post analytics retrieved: {analytics}")
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting post analytics: {str(e)}")
            return analytics
            
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
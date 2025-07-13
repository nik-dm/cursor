#!/usr/bin/env python3
"""
LinkedIn Automation Bot Setup Script

This script helps set up the LinkedIn automation environment,
install dependencies, and configure the initial setup.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🤖 LinkedIn Automation Bot Setup")
    print("=" * 60)
    print("Setting up your LinkedIn automation environment...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_chrome_browser():
    """Check if Chrome browser is installed"""
    print("🌐 Checking for Chrome browser...")
    
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✅ Chrome browser found")
            return True
    
    # Try to find chrome in PATH
    if shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium"):
        print("✅ Chrome browser found in PATH")
        return True
    
    print("⚠️  Chrome browser not found")
    print("   Please install Google Chrome from: https://www.google.com/chrome/")
    return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    directories = ["logs", "data", "screenshots"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   Created: {directory}/")
    
    print("✅ Directories created successfully")

def setup_environment_file():
    """Setup environment configuration file"""
    print("⚙️  Setting up environment configuration...")
    
    if os.path.exists(".env"):
        print("   .env file already exists")
        return True
    
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from template")
        print("   Please edit .env with your LinkedIn credentials")
        return True
    else:
        # Create basic .env file
        env_content = """# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password_here

# Browser Settings
HEADLESS_MODE=False
BROWSER_DELAY=2
PAGE_LOAD_TIMEOUT=30

# Automation Limits
MAX_CONNECTIONS_PER_DAY=50
MAX_MESSAGES_PER_DAY=20
MAX_PROFILE_VIEWS_PER_DAY=100

# Delays Between Actions (seconds)
MIN_DELAY_BETWEEN_ACTIONS=2
MAX_DELAY_BETWEEN_ACTIONS=5
"""
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ Created .env file")
        print("   Please edit .env with your LinkedIn credentials")
        return True

def run_test():
    """Run a basic test to verify setup"""
    print("🧪 Running basic test...")
    
    try:
        # Test imports
        import selenium
        import undetected_chromedriver
        import pandas
        from fake_useragent import UserAgent
        
        print("✅ All required packages imported successfully")
        
        # Test if we can create the bot instance
        from linkedin_bot import LinkedInBot
        bot = LinkedInBot(headless=True)
        print("✅ LinkedInBot class loaded successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Edit the .env file with your LinkedIn credentials:")
    print("   - Add your LinkedIn email and password")
    print("   - Adjust automation limits as needed")
    print()
    print("2. Run the basic example:")
    print("   python examples/basic_usage.py")
    print()
    print("3. Check the documentation:")
    print("   - README.md for detailed instructions")
    print("   - examples/ folder for usage examples")
    print()
    print("⚠️  Important Reminders:")
    print("- Use this tool responsibly and ethically")
    print("- Respect LinkedIn's Terms of Service")
    print("- Start with small limits and test carefully")
    print("- Monitor your account for any issues")
    print()
    print("🚀 Happy automating!")

def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    check_chrome_browser()  # Warning only, not required for setup
    
    # Setup steps
    steps = [
        create_directories,
        install_dependencies,
        setup_environment_file,
        run_test
    ]
    
    for step in steps:
        try:
            if not step():
                print(f"❌ Setup failed at step: {step.__name__}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error in {step.__name__}: {e}")
            sys.exit(1)
        
        print()  # Add spacing between steps
    
    print_next_steps()

if __name__ == "__main__":
    main()
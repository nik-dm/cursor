# LinkedIn Automation Bot 🤖

A comprehensive Python-based LinkedIn automation framework designed for responsible networking, lead generation, and data research. This tool helps automate common LinkedIn tasks while respecting platform limits and maintaining authentic engagement.

## ⚠️ Important Disclaimer

This tool is for educational and research purposes. Please ensure you comply with LinkedIn's Terms of Service and use this responsibly. The authors are not responsible for any account restrictions or violations that may result from misuse.

## 🚀 Features

### 🖥️ Web-Based Dashboard
- **Beautiful UI** - Modern, responsive web interface built with Streamlit
- **User Authentication** - Secure login system with session management
- **Real-time Monitoring** - Live bot status and activity tracking
- **Interactive Analytics** - Charts, graphs, and performance insights
- **Queue Management** - Visual connection request queue with bulk actions
- **Settings Panel** - Easy configuration management through the UI

### Core Automation
- **Automated Login** - Secure login with anti-detection measures
- **People Search** - Advanced search with keywords, location, and filters
- **Connection Requests** - Send personalized connection requests with custom messages
- **Profile Data Extraction** - Extract detailed profile information for research
- **Content Posting** - Create and schedule posts for personal profiles and company pages
- **Company Page Management** - Discover and manage company pages you have admin access to
- **Post Analytics** - Track engagement metrics for your posted content
- **Feed Engagement** - Automatically like posts in your LinkedIn feed
- **Screenshot Capture** - Take screenshots for monitoring and debugging

### Safety & Compliance
- **Rate Limiting** - Built-in daily limits to avoid being flagged
- **Random Delays** - Human-like timing between actions
- **Anti-Detection** - Undetected Chrome driver with stealth features
- **Comprehensive Logging** - Track all activities with detailed logs
- **Daily Statistics** - Monitor your automation usage

### Data Management
- **CSV Export** - Save extracted data in structured formats
- **Profile Analytics** - Generate insights from collected data
- **Progress Tracking** - Monitor success rates and performance

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed
- Linux/macOS/Windows

### Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd linkedin-automation
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your LinkedIn credentials and preferences
```

4. **Set up your credentials in `.env`:**
```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password_here
HEADLESS_MODE=False
MAX_CONNECTIONS_PER_DAY=50
MAX_MESSAGES_PER_DAY=20
```

5. **Launch the Web Dashboard:**
```bash
# Quick launch
./launch_ui.sh

# Or using Python
python3 launch_ui.py
```

6. **Access the dashboard:**
- Open http://localhost:8501 in your browser
- Login with default credentials: `admin` / `admin123`
- Configure your settings through the web interface

## 🎯 Quick Start

### Option 1: Web Dashboard (Recommended)

**Launch the web interface:**
```bash
# Easy launch (recommended)
./launch_ui.sh

# Or using Python
python3 launch_ui.py

# Or directly with Streamlit
streamlit run ui/app.py
```

**Access the dashboard:**
- 🌐 Open http://localhost:8501 in your browser
- 🔐 Login with: `admin` / `admin123`
- 🎯 Use the intuitive web interface to manage your automation

### Option 2: Python Scripts

**Basic Usage:**

```python
from linkedin_bot import LinkedInBot

# Initialize the bot
bot = LinkedInBot(headless=False)

try:
    # Start session and login
    bot.start_session()
    bot.login()
    
    # Search for people
    profiles = bot.search_people("python developer", "San Francisco")
    
    # Send connection requests
    for profile in profiles[:5]:
        message = "Hi! I'd love to connect with fellow developers."
        bot.send_connection_request(profile, message)
        
    # Extract profile data
    data = bot.extract_profile_data(profiles[0])
    print(f"Name: {data['name']}")
    print(f"Headline: {data['headline']}")
    
finally:
    bot.close_session()
```

## �️ Web Dashboard Features

The web interface provides a comprehensive dashboard for managing your LinkedIn automation:

### 🏠 Dashboard Overview
- **Real-time Status** - Monitor bot activity and connection status
- **Daily Statistics** - Track connections sent, profiles viewed, and success rates
- **Quick Actions** - Easy access to search, connection management, and analytics
- **Activity Log** - Real-time feed of bot activities and operations

### 🔍 People Search
- **Advanced Search** - Find profiles using keywords, location, and industry filters
- **Search Templates** - Pre-configured searches for common use cases
- **Bulk Selection** - Select multiple profiles for batch operations
- **Export Results** - Download search results as CSV files

### 📧 Connection Manager
- **Queue System** - Organize connection requests in a visual queue
- **Message Templates** - Use built-in or create custom message templates
- **Bulk Operations** - Send multiple connection requests with safety controls
- **Progress Tracking** - Monitor request status and success rates

### � Content Creator
- **Post Creation** - Create posts for both personal profiles and company pages
- **Content Templates** - Pre-built templates for different post types
- **Media Upload** - Add images to your posts for better engagement
- **Scheduling** - Schedule posts for optimal timing
- **Draft Management** - Save and edit drafts before publishing
- **Company Selection** - Choose from your managed company pages
- **Post Analytics** - Track engagement metrics for published content

### �📊 Analytics Dashboard
- **Performance Charts** - Visual representation of your automation performance
- **Success Rate Tracking** - Monitor connection acceptance rates over time
- **Industry Analysis** - Breakdown of target industries and locations
- **Export Reports** - Generate and download detailed analytics reports

### ⚙️ Settings & Configuration
- **Credential Management** - Securely update LinkedIn login credentials
- **Automation Limits** - Configure daily limits and safety parameters
- **Browser Settings** - Control headless mode and timing preferences

## �📚 Command Line Examples

The `examples/` directory contains ready-to-use scripts:

### 1. Basic Usage (`examples/basic_usage.py`)
Demonstrates fundamental bot operations including login, search, and connection requests.

```bash
python examples/basic_usage.py
```

### 2. Bulk Connection Requests (`examples/bulk_connection_requests.py`)
Advanced script for sending personalized connection requests at scale.

```bash
python examples/bulk_connection_requests.py
```

### 3. Data Scraper (`examples/data_scraper.py`)
Research-focused script for extracting and analyzing profile data.

```bash
python examples/data_scraper.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LINKEDIN_EMAIL` | Your LinkedIn email | Required |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | Required |
| `HEADLESS_MODE` | Run browser in background | `False` |
| `MAX_CONNECTIONS_PER_DAY` | Daily connection limit | `50` |
| `MAX_MESSAGES_PER_DAY` | Daily message limit | `20` |
| `MAX_PROFILE_VIEWS_PER_DAY` | Daily profile view limit | `100` |
| `MIN_DELAY_BETWEEN_ACTIONS` | Minimum delay (seconds) | `2` |
| `MAX_DELAY_BETWEEN_ACTIONS` | Maximum delay (seconds) | `5` |

### Safety Limits

The bot includes built-in safety measures:
- **Daily Connection Limit**: 50 requests (LinkedIn's recommended limit)
- **Random Delays**: 2-5 seconds between actions
- **Session Management**: Automatic browser cleanup
- **Error Handling**: Graceful failure recovery

## 📊 Data Output

### Directory Structure
```
project/
├── data/           # Exported CSV files
├── logs/           # Activity logs
├── screenshots/    # Captured screenshots
└── examples/       # Usage examples
```

### CSV Exports
- **Profile Data**: Names, headlines, locations, experience
- **Connection Stats**: Success rates, daily counts
- **Research Reports**: Analyzed insights and trends

## 🛡️ Best Practices

### Responsible Usage
1. **Respect Limits** - Don't exceed daily connection limits
2. **Personalize Messages** - Always send meaningful connection requests
3. **Monitor Activity** - Check logs regularly for any issues
4. **Use Delays** - Maintain human-like timing between actions
5. **Stay Updated** - Keep the tool updated with latest LinkedIn changes

### Security Tips
- Store credentials securely in `.env` file
- Never commit credentials to version control
- Use strong, unique passwords
- Enable 2FA on your LinkedIn account
- Monitor your account for unusual activity

## 🐛 Troubleshooting

### Common Issues

**Login Failed**
```
Error: Login failed - redirected to unexpected page
Solution: Check credentials, enable 2FA, or try manual login first
```

**Connection Requests Not Sending**
```
Error: No Connect button found
Solution: User may already be connected or not accepting requests
```

**Browser Crashes**
```
Error: Chrome driver setup failed
Solution: Update Chrome browser and restart the script
```

### Debug Mode
Run with verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Monitoring

### Logs
Check `logs/linkedin_bot.log` for detailed activity:
```
2024-01-15 10:30:15 - INFO - Successfully logged in to LinkedIn
2024-01-15 10:30:45 - INFO - Found 25 profiles for keywords: python developer
2024-01-15 10:31:20 - INFO - Connection request sent to https://linkedin.com/in/user123
```

### Daily Statistics
Monitor your automation usage:
```python
stats = bot.get_daily_stats()
print(f"Connections sent today: {stats['connections_sent']}")
print(f"Profiles viewed today: {stats['profiles_viewed']}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

This tool is provided for educational and research purposes only. Users are responsible for ensuring their use complies with:
- LinkedIn's Terms of Service
- Data protection regulations (GDPR, CCPA, etc.)
- Local laws and regulations
- Professional and ethical standards

The developers assume no liability for any misuse or violations resulting from the use of this tool.

## 🆘 Support

- 📖 **Documentation**: Check this README and code comments
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Submit enhancement ideas
- 💬 **Questions**: Use GitHub Discussions

## 📝 Changelog

### v1.0.0
- Initial release with core automation features
- Anti-detection measures implemented
- Rate limiting and safety features
- Comprehensive logging and data export
- Example scripts and documentation

---

**Happy Networking! 🚀**

*Remember: Automation should enhance authentic networking, not replace genuine human connections.*
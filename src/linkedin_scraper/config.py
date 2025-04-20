"""
LinkedIn crawler configuration file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LinkedIn login credentials
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME", "your_email@example.com")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "your_password")

# Browser configuration
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = int(
    os.getenv("SLOW_MO", "50")
)  # Slow down Playwright operations in milliseconds, helps bypass anti-crawling

# User agent configuration - use modern browser user agent
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
)

# Proxy configuration (if needed)
PROXY = os.getenv("PROXY", None)

# Timeout settings
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "300000"))  # 30 seconds
# Path to save data
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
)
COOKIES_PATH = os.path.join(DATA_DIR, "cookies.json")
# Cookies configuration (optional, read from .env)
LINKEDIN_COOKIES = os.getenv("LINKEDIN_COOKIES", None)
LINKEDIN_URL = "https://www.linkedin.com"
LINKEDIN_LOGIN_URL = "https://www.linkedin.com/login"

import json
import httpx
from playwright.async_api import async_playwright

from ..config import (
    LINKEDIN_USERNAME,
    LINKEDIN_PASSWORD,
    SLOW_MO,
    USER_AGENT,
    PROXY,
    DEFAULT_TIMEOUT,
    DATA_DIR,
    LINKEDIN_COOKIES,
    HEADLESS,
    LINKEDIN_URL,
    COOKIES_PATH,
)
from ..auth_handler import LinkedInAuthHandler
from ..anti_detection import AntiDetectionHandler
from .profile import ProfileScraper
from .company import CompanyScraper
from ..logging import debug, error


class LinkedInScraper:
    """Main LinkedIn scraper class that orchestrates the scraping process."""

    def __init__(self, headless=None) -> None:
        """Initialize the LinkedIn scraper."""
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.headless = headless if headless is not None else HEADLESS
        self.anti_detection = AntiDetectionHandler()
        self.auth_handler = LinkedInAuthHandler(
            username=LINKEDIN_USERNAME,
            password=LINKEDIN_PASSWORD,
            cookies_path=COOKIES_PATH,
        )

    async def initialize_browser(self) -> None:
        """Initialize browser and apply stealth techniques."""
        # Initialize Playwright
        self.playwright = await async_playwright().start()

        # Get browser launch options
        browser_options = self.anti_detection.get_browser_launch_options(
            use_proxy=bool(PROXY), proxy_url=PROXY
        )

        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=SLOW_MO,  # Control browser operation delay (ms)
            args=browser_options.get("args", []),
        )

        # Create browser context
        self.context = await self.browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080},
            device_scale_factor=1,
            is_mobile=False,
            has_touch=False,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )

        # Set default timeout
        # self.context.set_default_timeout(DEFAULT_TIMEOUT)
        # debug(f"DEFAULT_TIMEOUT: {DEFAULT_TIMEOUT}")
        self.context.set_default_timeout(DEFAULT_TIMEOUT)

        # Create new page
        self.page = await self.context.new_page()

        # Apply stealth techniques
        await self.apply_stealth_techniques()

    async def apply_stealth_techniques(self) -> None:
        """Apply stealth techniques to evade detection."""
        from undetected_playwright import stealth_async

        # Apply stealth mode to bypass anti-bot detection
        await stealth_async(self.page)
        # Apply additional anti-detection techniques
        await self.anti_detection.apply_stealth_techniques(self.context, self.page)

    async def login(self) -> bool:
        """Handle LinkedIn login process."""
        login_success = False

        # Try to login with cookies from environment variable first
        if LINKEDIN_COOKIES:
            debug(
                "Detected environment variable LINKEDIN_COOKIES, "
                "will try to use it for login..."
            )
            try:
                # Handle both JSON format and cookie string format
                try:
                    # Try parsing as JSON first
                    cookies = json.loads(LINKEDIN_COOKIES)
                except json.JSONDecodeError:
                    # If not JSON, parse as cookie string
                    cookies = []
                    cookie_pairs = LINKEDIN_COOKIES.split(";")
                    for pair in cookie_pairs:
                        if "=" in pair:
                            name, value = pair.strip().split("=", 1)
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            cookies.append(
                                {
                                    "name": name,
                                    "value": value,
                                    "domain": ".linkedin.com",
                                    "path": "/",
                                }
                            )

                await self.context.add_cookies(cookies)

                await self.page.goto(LINKEDIN_URL, waitUntil="domcontentloaded")

                if await self.auth_handler.is_logged_in(self.page):
                    debug("Login successful using environment variable cookies")
                    login_success = True
                else:
                    debug(
                        "Environment variable cookies are invalid, "
                        "will try account password login"
                    )
                login_success = True
            except Exception as e:
                error_msg = (
                    f"Environment variable cookies format error or "
                    f"injection failed: {e}"
                )
                debug(f"{error_msg}, cookies: {cookies}")
                error(f"{error_msg}, will try account password login")

        # If cookies login failed, try account login
        if not login_success:
            # debug("Will use account password login")
            login_success = await self.auth_handler.login(self.page, self.context)

        return login_success

    async def scrape_profile(self, profile_name: str) -> None:
        """Scrape a LinkedIn profile."""
        profile_scraper = ProfileScraper(data_dir=DATA_DIR)
        await profile_scraper.scrape_profile(self.page, profile_name)

    async def scrape_profile_html(self, profile_name: str) -> str:
        """Scrape a LinkedIn profile."""
        profile_scraper = ProfileScraper(data_dir=DATA_DIR)
        return await profile_scraper.scrape_profile_html(self.page, profile_name)

    async def scrape_company(self, company_name: str) -> None:
        """Scrape a LinkedIn company profile."""
        company_scraper = CompanyScraper(data_dir=DATA_DIR)
        await company_scraper.scrape_company(self.page, company_name)

    async def scrape_company_html(self, company_name: str) -> str:
        """Scrape a LinkedIn company profile."""
        company_scraper = CompanyScraper(data_dir=DATA_DIR)
        return await company_scraper.scrape_company_html(self.page, company_name)

    async def cleanup(self) -> None:
        """Close browser and Playwright."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


def get_profile_html(profile_name: str) -> str:
    """Get the HTML content of a LinkedIn profile."""
    url = f"https://www.linkedin.com/in/{profile_name}"
    # load cookies from file
    with open(COOKIES_PATH, "r") as f:
        cookies = json.load(f)

    # Create cookie jar and client
    cookies_jar = httpx.Cookies()
    for cookie in cookies:
        cookies_jar.set(
            cookie["name"],
            cookie["value"],
            domain=cookie["domain"],
            path=cookie.get("path", "/"),
        )

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }

    # Create client with cookies
    client = httpx.Client(cookies=cookies_jar, headers=headers)
    response = client.get(url)

    return response.text

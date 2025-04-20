"""
LinkedIn Scraper - Authentication Handler Module
Focuses on handling LinkedIn login, CAPTCHA, and security verification
"""

import os
import json
import time
import random
from pathlib import Path
from playwright.async_api import Page, BrowserContext
from .config import DEFAULT_TIMEOUT, LINKEDIN_URL, LINKEDIN_LOGIN_URL
from .logging import get_logger

logger = get_logger()


class LinkedInAuthHandler:
    """
    Handles LinkedIn authentication, CAPTCHA, and security verification
    """

    def __init__(self, username, password, cookies_path):
        """
        Initialize authentication handler

        Args:
            username: LinkedIn username/email
            password: LinkedIn password
            cookies_path: File path to save/load cookies
        """
        self.username = username
        self.password = password
        self.cookies_path = cookies_path

    async def login(self, page: Page, context: BrowserContext):
        """
        Handle LinkedIn login process

        Args:
            page: Playwright page object
            context: Playwright browser context

        Returns:
            bool: Whether login was successful
        """
        logger.debug("Attempting to log in to LinkedIn...")

        # First try using saved cookies
        if await self.load_cookies(context):
            # Use cookies to access LinkedIn homepage and check if still valid
            await page.goto(LINKEDIN_URL)
            # Check if already logged in
            if await self.is_logged_in(page):
                logger.debug("Successfully logged in using saved cookies")
                return True

        # If no cookies or cookies are invalid, perform login process
        await page.goto(LINKEDIN_LOGIN_URL)
        self._random_sleep(1, 2)

        # Enter username and password
        logger.debug(f"Entering username: {self.username}")
        logger.debug(f"Entering password: {self.password}")
        await page.fill("input#username", self.username)
        self._random_sleep(1, 2)
        await page.fill("input#password", self.password)
        self._random_sleep(1, 2)

        # Click login button
        await page.click('button[type="submit"]')

        # Wait for page to load, CAPTCHA or security check may appear
        try:
            # Wait for redirect to complete
            await page.wait_for_load_state("networkidle", timeout=DEFAULT_TIMEOUT)

            # Check if login was successful
            if await self.is_logged_in(page):
                logger.debug("Login successful")
                # Save cookies for next use
                await self.save_cookies(page, context)
                return True
            else:
                logger.debug("Login failed, please check your username and password")
                return False

        except Exception as e:
            logger.debug(f"Error occurred during login: {e}")
            return False

    async def load_cookies(self, context: BrowserContext):
        """
        Load cookies from file

        Args:
            context: Playwright browser context

        Returns:
            bool: Whether cookies were loaded successfully
        """
        if Path(self.cookies_path).exists():
            try:
                with open(self.cookies_path, "r") as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
                logger.debug(f"Cookies loaded from {self.cookies_path}")
                return True
            except Exception as e:
                logger.debug(f"Error loading cookies: {e}")
        return False

    async def save_cookies(self, page: Page, context: BrowserContext):
        """
        Save cookies to file

        Args:
            page: Playwright page object
            context: Playwright browser context
        """
        cookies = await context.cookies()
        os.makedirs(os.path.dirname(self.cookies_path), exist_ok=True)
        with open(self.cookies_path, "w") as f:
            json.dump(cookies, f)
        logger.debug(f"Cookies saved to {self.cookies_path}")

    async def is_logged_in(self, page: Page):
        """
        Check if successfully logged in to LinkedIn

        Args:
            page: Playwright page object

        Returns:
            bool: Whether logged in
        """
        # Check if profile icon exists in the navigation bar, usually indicates logged in
        try:
            # Try multiple possible selectors
            selectors = [
                "div.global-nav__me",
                "img.global-nav__me-photo",
                "li.global-nav__nav-item--profile",
                'a[data-control-name="identity_profile_photo"]',
            ]

            for selector in selectors:
                if await page.is_visible(selector):
                    return True

            # Another check method: Find specific URL elements
            current_url = page.url
            if "/feed" in current_url or "/mynetwork" in current_url:
                return True

            # Add to is_logged_in method
            error_selectors = [
                "div.alert-error",
                "#error-for-username",
                "#error-for-password",
                "div.form__error",
                "p.alert-content",
            ]
            for selector in error_selectors:
                if await page.is_visible(selector):
                    error_text = await page.text_content(selector)
                    msg = "LinkedIn error message: " + str(error_text)
                    logger.debug(msg)
                    return False

            return False
        except Exception as e:
            logger.debug(f"Error checking login state: {e}")
            return False

    async def detect_captcha(self, page: Page):
        """
        Detect if there is a CAPTCHA on the page

        Args:
            page: Playwright page object

        Returns:
            bool: Whether a CAPTCHA is detected
        """
        captcha_selectors = [
            "div.recaptcha-checkbox-border",  # Google reCAPTCHA
            'iframe[title*="recaptcha"]',  # reCAPTCHA iframe
            'iframe[src*="recaptcha"]',  # reCAPTCHA iframe (another form)
            "div.g-recaptcha",  # reCAPTCHA div
            "div.captcha-container",  # LinkedIn custom CAPTCHA
            'img[alt*="CAPTCHA"]',  # Image CAPTCHA
            'input[name="captcha"]',  # CAPTCHA input box
        ]

        for selector in captcha_selectors:
            try:
                if await page.is_visible(selector):
                    logger.debug(f"CAPTCHA detected: {selector}")
                    return True
            except Exception:
                continue

        # Check if page content contains CAPTCHA-related text
        page_content = await page.content()
        captcha_keywords = [
            "captcha",
            "CAPTCHA",
            "human verification",
            "security verification",
            "please prove",
            "I'm not a robot",
            "I am not a robot",
        ]
        for keyword in captcha_keywords:
            if keyword.lower() in page_content.lower():
                logger.debug(f"CAPTCHA keyword detected in page content: {keyword}")
                return True

        return False

    async def handle_captcha(self, page: Page):
        """
        Handle CAPTCHA challenge

        Args:
            page: Playwright page object
        """
        logger.debug("Handling CAPTCHA...")

        # Check if it is Google reCAPTCHA
        recaptcha_iframe = page.frame_locator(
            'iframe[title*="recaptcha"], iframe[src*="recaptcha"]'
        )
        if await recaptcha_iframe.count() > 0:
            # Try clicking the reCAPTCHA checkbox
            try:
                await recaptcha_iframe.locator("div.recaptcha-checkbox-border").click()
                # Wait for a while to see if it passes automatically
                self._random_sleep(3, 5)

                # If image CAPTCHA appears, may require manual intervention
                if await page.is_visible('iframe[title*="challenge"]'):
                    logger.debug(
                        "Need to solve image CAPTCHA, please complete manually"
                    )
                    # In actual use, you can integrate CAPTCHA solving services here
                    # e.g.: 2captcha, Anti-Captcha, etc.
                    logger.debug("Waiting for user to solve CAPTCHA manually...")
                    await page.wait_for_timeout(
                        30000
                    )  # Give user 30 seconds to solve manually
            except Exception as e:
                logger.debug(f"Error handling reCAPTCHA: {e}")

        # Wait for page change after CAPTCHA is handled
        await page.wait_for_load_state("networkidle")
        self._random_sleep(2, 4)

        # Check if CAPTCHA still exists
        if await self.detect_captcha(page):
            logger.debug("CAPTCHA still exists, may need manual solution")
            await page.wait_for_timeout(30000)  # Give user more time to solve manually

    async def detect_security_verification(self, page: Page):
        """
        Detect if security verification is required

        Args:
            page: Playwright page object

        Returns:
            bool: Whether security verification is detected
        """
        security_selectors = [
            "input#verification-code",  # Verification code input box
            "div.challenge-dialog",  # Security challenge dialog
            'input[name="pin"]',  # PIN input
            'h1.form__header:text("Verification")',  # Verification page title
            "div.verification-code",  # Verification code container
            'input[name="security_code"]',  # Security code input
            'form[name="two-step-challenge"]',  # Two-step verification form
        ]

        for selector in security_selectors:
            try:
                if await page.is_visible(selector):
                    logger.debug(f"Security verification detected: {selector}")
                    return True
            except Exception:
                continue

        # Check if page content contains security verification related text
        page_content = await page.content()
        security_keywords = [
            "security verification",
            "verify your identity",
            "two-step verification",
            "unusual activity",
            "verify it's you",
            "confirm it's you",
        ]
        for keyword in security_keywords:
            if keyword.lower() in page_content.lower():
                msg = (
                    "Security verification keyword detected in "
                    "page content: " + str(keyword)
                )
                logger.debug(msg)
                return True

        return False

    async def handle_security_verification(self, page: Page):
        """
        Handle security verification

        Args:
            page: Playwright page object
        """
        logger.debug("Security verification detected, may require manual handling...")

        # Check if it is email verification code
        if await page.is_visible(
            'input#verification-code, input[name="security_code"]'
        ):
            logger.debug("Email verification code required, please check your email")
            # In actual use, you can integrate email API here
            logger.debug("Waiting for user to enter the verification code manually...")
            await page.wait_for_timeout(
                60000
            )  # Give user 60 seconds to check email and enter code

        # Check if it is SMS verification code
        elif await page.is_visible('input[name="pin"]'):
            logger.debug(
                "SMS verification code required, please check your phone messages"
            )
            logger.debug("Waiting for user to enter the verification code manually...")
            await page.wait_for_timeout(
                60000
            )  # Give user 60 seconds to check SMS and enter code

        # Other security challenges
        elif await page.is_visible(
            'div.challenge-dialog, form[name="two-step-challenge"]'
        ):
            logger.debug("Security challenge required, please handle manually")
            logger.debug(
                "Waiting for user to handle the security challenge manually..."
            )
            await page.wait_for_timeout(
                60000
            )  # Give user 60 seconds to handle manually

        # Wait for page change after verification is complete
        await page.wait_for_load_state("networkidle")
        self._random_sleep(2, 4)

    def _random_sleep(self, min_seconds=1, max_seconds=5):
        """
        Randomly wait for a period of time to simulate human behavior

        Args:
            min_seconds: Minimum wait seconds
            max_seconds: Maximum wait seconds
        """
        time.sleep(random.uniform(min_seconds, max_seconds))

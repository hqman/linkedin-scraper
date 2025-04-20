"""
LinkedIn Scraper Utility Functions
"""

import random
import time
import json
import os
from pathlib import Path
from src.linkedin_scraper.logging import get_logger

logger = get_logger()


def random_sleep(min_seconds=1, max_seconds=5):
    """
    Sleep for a random period to simulate human behavior
    """
    time.sleep(random.uniform(min_seconds, max_seconds))


def save_cookies(page, cookie_file):
    """
    Save browser cookies to file
    """
    cookies = page.context.cookies()
    os.makedirs(os.path.dirname(cookie_file), exist_ok=True)
    with open(cookie_file, "w") as f:
        json.dump(cookies, f)
    logger.debug(f"Cookies saved to {cookie_file}")


def load_cookies(context, cookie_file):
    """
    Prefer loading cookies from environment variable, otherwise load from file
    """
    env_cookies = os.getenv("LINKEDIN_COOKIES")
    if env_cookies:
        try:
            cookies = json.loads(env_cookies)
            context.add_cookies(cookies)
            logger.debug("Cookies loaded from environment variable LINKEDIN_COOKIES")
            return True
        except Exception as e:
            logger.debug(f"Error loading cookies from env: {e}")
            return False
    # If environment variable is not set, try file
    if not Path(cookie_file).exists():
        logger.debug(f"Cookie file {cookie_file} does not exist")
        return False
    try:
        with open(cookie_file, "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        logger.debug(f"Cookies loaded from {cookie_file}")
        return True
    except Exception as e:
        logger.debug(f"Error loading cookies: {e}")
        return False


def extract_profile_data(page):
    """
    Extract data from LinkedIn profile page
    """
    profile_data = {}

    # Extract name
    try:
        name_element = page.locator("h1.text-heading-xlarge")
        profile_data["name"] = name_element.text_content().strip()
    except Exception:
        profile_data["name"] = "Name not found"

    # Extract headline/title
    try:
        headline_element = page.locator("div.text-body-medium").first
        profile_data["headline"] = headline_element.text_content().strip()
    except Exception:
        profile_data["headline"] = "Headline not found"

    # Extract location
    try:
        location_element = page.locator("span.text-body-small").first
        profile_data["location"] = location_element.text_content().strip()
    except Exception:
        profile_data["location"] = "Location not found"

    # Extract about section
    try:
        about_element = page.locator("div#about")
        next_div = about_element.locator("xpath=following-sibling::div").first
        span_element = next_div.locator('span[aria-hidden="true"]')
        profile_data["about"] = span_element.text_content().strip()
    except Exception:
        profile_data["about"] = "About section not found"

    # Extract experience
    try:
        exp_element = page.locator("div#experience")
        next_div = exp_element.locator("xpath=following-sibling::div")
        experience_items = next_div.locator("li.artdeco-list__item")

        experiences = []
        for i in range(experience_items.count()):
            item = experience_items.nth(i)
            experience = {}
            try:
                title_element = item.locator("span.mr1.t-bold")
                experience["title"] = title_element.text_content().strip()

                company_element = item.locator("span.t-14.t-normal").first
                experience["company"] = company_element.text_content().strip()

                duration_element = item.locator(
                    "span.t-14.t-normal.t-black--light"
                ).first
                experience["duration"] = duration_element.text_content().strip()

                experiences.append(experience)
            except Exception:
                continue
        profile_data["experiences"] = experiences
    except Exception:
        profile_data["experiences"] = []

    return profile_data


def extract_company_data(page):
    """
    Extract data from LinkedIn company page
    """
    company_data = {}

    # Extract company name
    try:
        name_element = page.locator("h1.org-top-card-summary__title")
        company_data["name"] = name_element.text_content().strip()
    except Exception:
        company_data["name"] = "Company name not found"

    # Extract company tagline
    try:
        tagline_element = page.locator("p.org-top-card-summary__tagline")
        company_data["tagline"] = tagline_element.text_content().strip()
    except Exception:
        company_data["tagline"] = "Tagline not found"

    # Extract company info (size, industry, etc.)
    try:
        info_selector = "div.org-top-card-summary-info-list__info-item"
        info_items = page.locator(info_selector)

        for i in range(info_items.count()):
            item_text = info_items.nth(i).text_content().strip()
            if "员工" in item_text or "人" in item_text:
                company_data["size"] = item_text
            elif "行业" in item_text:
                company_data["industry"] = item_text
    except Exception:
        company_data["size"] = "Company size not found"
        company_data["industry"] = "Industry info not found"

    # Extract about section
    try:
        about_section = page.locator("section.artdeco-card.p5.mb4").first
        about_element = about_section.locator("p.break-words")
        company_data["about"] = about_element.text_content().strip()
    except Exception:
        company_data["about"] = "About section not found"

    return company_data

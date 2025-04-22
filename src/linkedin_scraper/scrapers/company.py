import os
import json
import random
import asyncio
from playwright.async_api import Page
from ..logging import get_logger

from ..config import LINKEDIN_URL

logger = get_logger()


class CompanyScraper:
    """
    LinkedIn company profile scraper
    Focuses on scraping LinkedIn company profiles
    """

    def __init__(self, data_dir):
        """
        Initialize the company profile scraper

        Args:
            data_dir: Directory to save data
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    async def scrape_company_html(self, page: Page, company_name: str):
        """
        Scrape LinkedIn company profile

        Args:
            page: Playwright page object
            company_url: Company profile URL

        Returns:
            str: Scraped company profile HTML
        """
        logger.debug(f"Scraping company profile: {company_name}")

        # try:
        # Visit company page
        company_url = f"{LINKEDIN_URL}/company/{company_name}/"

        await page.goto(company_url)
        # await page.wait_for_load_state("networkidle")

        # Ensure JavaScript execution completes
        await page.wait_for_selector("body")

        # Scroll the page to load more content
        await self._scroll_page(page)
        # Get page content
        page_content = await page.content()
        return page_content

    async def scrape_company(self, page: Page, company_name: str):
        """
        Scrape LinkedIn company profile

        Args:
            page: Playwright page object
            company_url: Company profile URL

        Returns:
            dict: Scraped company profile data
        """
        logger.debug(f"Scraping company profile: {company_name}")

        # try:
        # Visit company page
        company_url = f"{LINKEDIN_URL}/company/{company_name}/"

        await page.goto(company_url)
        # await page.wait_for_load_state("networkidle")

        await self._random_sleep(1, 2)

        # Ensure JavaScript execution completes
        await page.wait_for_selector("body")

        # Scroll the page to load more content
        await self._scroll_page(page)
        # Get page content
        # await self._random_sleep(0.5, 1)
        # await page.wait_for_selector("div#ember41", state="visible")
        # await page.wait_for_selector(
        #     '//*[@id="ember41"]', state="visible", timeout=DEFAULT_TIMEOUT
        # )
        # await page.click('//*[@id="ember41"]')
        # node = page.locator('//*[@id="ember42"]')

        # # After clicking, get the HTML content of the node with
        # # class org-module-card__margin-bottom
        # # Get the content of this specific node, not the entire HTML
        # # Get page content
        # html_content = await node.inner_html()  # Get the HTML content of the node

        # Print the obtained content
        # logger.debug(f"HTML Content: {html_content}")

        await self._random_sleep(1.5, 2)
        # page_content = await page.content()
        # print(page_content)

        # Extract company profile data
        company_data = await self._extract_company_data(page)

        # Save data
        company_id = company_url.split("/company/")[-1].split("/")[0]
        output_file = os.path.join(self.data_dir, f"company_{company_id}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(company_data, f, ensure_ascii=False, indent=2)

        logger.debug(f"Company profile data saved to: {output_file}")
        return company_data

    async def _extract_company_data(self, page: Page):
        """
        Extract data from LinkedIn company page

        Args:
            page: Playwright page object

        Returns:
            dict: Extracted company profile data
        """
        company_data = {}

        # Extract basic info
        await self._extract_basic_info(page, company_data)

        return company_data

    async def _extract_basic_info(self, page: Page, company_data: dict):
        """
        Extract basic information

        Args:
            page: Playwright page object
            company_data: Company profile data dictionary
        """
        # Extract company name
        try:
            name_selector = (
                '//div[contains(@class, "org-module-card__margin-bottom")]//h1'
            )

            name_locator = page.locator(name_selector)
            if await name_locator.count() > 0:
                company_data["name"] = await name_locator.text_content()
                company_data["name"] = company_data["name"].strip()
            else:
                company_data["name"] = "Company name not found"
        except Exception as e:
            logger.debug(f"Error extracting company name: {e}")
            company_data["name"] = "Error extracting company name"

        # Extract company tagline
        try:
            tagline_selector = (
                "//div[contains(@class, 'org-module-card__margin-bottom')]//p"
            )

            tagline_locator = page.locator(tagline_selector)
            if await tagline_locator.count() > 0:
                company_data["tagline"] = await tagline_locator.first.text_content()
                company_data["tagline"] = company_data["tagline"].strip()
                if not company_data["tagline"]:
                    company_data["tagline"] = "Company tagline not found"
            else:
                company_data["tagline"] = "Company tagline not found"
        except Exception as e:
            logger.debug(f"Error extracting company tagline: {e}")
            company_data["tagline"] = "Error extracting company tagline"

    async def _scroll_page(self, page: Page):
        """
        Scroll the page to load more content

        Args:
            page: Playwright page object
        """
        try:
            # Get page height, add error handling
            height = await page.evaluate(
                """() => {
                if (document.body && document.body.scrollHeight) {
                    return document.body.scrollHeight;
                } else if (document.documentElement && document.documentElement.scrollHeight) {
                    return document.documentElement.scrollHeight;
                } else {
                    return 1000; // Default height
                }
            }"""
            )

            viewport_height = await page.evaluate(
                """() => {
                return window.innerHeight || 800;
            }"""
            )

            # Calculate number of scrolls
            scroll_times = min(10, max(3, height // viewport_height))

            # Scroll the page multiple times to simulate human reading
            for i in range(scroll_times):
                # Calculate next scroll position, add some randomness
                next_pos = int(
                    (i + 1) * height / scroll_times * (0.8 + 0.4 * random.random())
                )

                # Safely perform scroll
                await page.evaluate(
                    f"""() => {{
                    if (typeof window.scrollTo === 'function') {{
                        window.scrollTo(0, {next_pos});
                    }}
                }}"""
                )

                # Random pause to simulate reading
                await self._random_sleep(0.5, 2)

                # Occasionally scroll up a bit to simulate reviewing content
                if random.random() < 0.3 and i > 0:
                    back_pos = max(0, next_pos - random.randint(100, 300))
                    await page.evaluate(
                        f"""() => {{
                        if (typeof window.scrollTo === 'function') {{
                            window.scrollTo(0, {back_pos});
                        }}
                    }}"""
                    )
                    await self._random_sleep(0.5, 1.5)
                    await page.evaluate(
                        f"""() => {{
                        if (typeof window.scrollTo === 'function') {{
                            window.scrollTo(0, {next_pos});
                        }}
                    }}"""
                    )
                    await self._random_sleep(0.5, 1.5)

            # Scroll back to top
            await page.evaluate(
                """() => {
                if (typeof window.scrollTo === 'function') {
                    window.scrollTo(0, 0);
                }
            }"""
            )
            await self._random_sleep(1, 2)
        except Exception as e:
            logger.debug(f"Error scrolling page: {e}")
            # Continue execution, do not let scroll error affect overall scraping

    async def _random_sleep(self, min_seconds=1, max_seconds=5):
        """
        Randomly wait for a period of time to simulate human behavior

        Args:
            min_seconds: Minimum wait seconds
            max_seconds: Maximum wait seconds
        """
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))

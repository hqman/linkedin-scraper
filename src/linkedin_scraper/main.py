import os
import asyncio
from typing import Literal

from bs4 import BeautifulSoup

from .utils.html_cleaner import clean_html

from .config import DATA_DIR

from .scrapers.linkedin import LinkedInScraper
from .logging import debug, error


async def scrape(
    target_name: str, target_type: Literal["profile", "company"] = "profile"
) -> None:
    """
    Main scraping function that orchestrates the LinkedIn scraping process.

    Args:
        target_name: The profile or company name/identifier
        target_type: The type of target to scrape ("profile" or "company")
    """
    scraper = LinkedInScraper()

    try:
        # Check if data directory exists, create it if it doesn't
        if not os.path.exists(DATA_DIR):
            debug(f"Creating data directory: {DATA_DIR}")
            os.makedirs(DATA_DIR)

        # Initialize browser
        await scraper.initialize_browser()

        # Login to LinkedIn
        login_success = await scraper.login()
        if not login_success:
            error("Login failed, cannot continue")
            return

        # Scrape the target
        if target_type == "profile":
            await scraper.scrape_profile(target_name)
        else:  # company

            await scraper.scrape_company(target_name)

        debug(f"Scraping {target_type} completed successfully")

    except Exception as e:
        error(f"Error occurred during scraping: {e}")

    finally:
        # Clean up resources
        await scraper.cleanup()


async def scrape_html(type: Literal["profile", "company"], name: str):
    scraper = LinkedInScraper(headless=True)
    try:
        # Initialize browser
        await scraper.initialize_browser()
        # Login to LinkedIn
        login_success = await scraper.login()
        if not login_success:
            error("Login failed, cannot continue")

        # Scrape the target
        if type == "profile":
            html = await scraper.scrape_profile_html(name)
        else:
            html = await scraper.scrape_company_html(name)
        html = clean_html(html)
        # bs4  main
        soup = BeautifulSoup(html, "html.parser")
        # main
        main = soup.find("main")
        # print(main.prettify())
        return main.prettify().replace("\n", "")
    except Exception as e:
        error(f"Error occurred during scraping: {e}")
        return ""


if __name__ == "__main__":
    # Create data directory

    # Single target examples
    profile_name = "jamesalexandersydney"
    company_name = "relevanceai"

    # Run a single scrape job
    asyncio.run(scrape(company_name, "company"))

    # Uncomment to run multiple scraping jobs in parallel
    # targets = [
    #     ("jamesalexandersydney", "profile"),
    #     ("jasonzhoudesign", "profile"),
    #     ("relevanceai", "company")
    # ]
    #  tasks = [scrape(name, type_) for name, type_ in targets]
    # await asyncio.gather(*tasks)

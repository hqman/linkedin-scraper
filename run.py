import asyncio
import argparse
from src.linkedin_scraper.logging import get_logger
from src.linkedin_scraper.main import scrape

logger = get_logger()


def main():
    logger.debug("Hello from linkedin-scraper!")

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="LinkedIn Scraper")

    # Create a mutually exclusive group for profile and company options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--profile", action="store_true", help="Scrape a LinkedIn profile"
    )
    group.add_argument(
        "--company", action="store_true", help="Scrape a LinkedIn company"
    )

    # Name parameter
    parser.add_argument(
        "--name", required=True, help="Profile or company name to scrape"
    )

    args = parser.parse_args()

    # Determine target type
    target_type = "profile" if args.profile else "company"

    # Run scrape job
    asyncio.run(scrape(args.name, target_type))


if __name__ == "__main__":
    main()

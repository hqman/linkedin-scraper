import asyncio
import argparse
import json
from src.linkedin_scraper.logging import get_logger
from src.linkedin_scraper.main import scrape, scrape_html
from src.linkedin_scraper.llm_extractor import extract_profile, extract_company

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

    # Add llm parameter
    parser.add_argument(
        "--llm", action="store_true", help="Use LLM extraction on scraped HTML"
    )

    args = parser.parse_args()

    # Determine target type
    target_type = "profile" if args.profile else "company"

    # Run scrape job
    if args.llm:
        # Use scrape_html and LLM extractor
        async def run_llm_extraction():
            html = await scrape_html(type=target_type, name=args.name)

            if target_type == "profile":
                result = extract_profile(html)
            else:
                result = extract_company(html)

            # pretty print the result
            print(json.dumps(result, indent=4))

        asyncio.run(run_llm_extraction())
    else:
        # Use regular scrape
        asyncio.run(scrape(args.name, target_type))


if __name__ == "__main__":
    main()

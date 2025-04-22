import pytest
from linkedin_scraper.llm_extractor import extract_profile, extract_company
from linkedin_scraper.main import scrape_html


@pytest.mark.asyncio
async def test_profile_llm_extractor():
    main_html = await scrape_html(type="profile", name="hqman")
    print(extract_profile(main_html))


@pytest.mark.asyncio
async def test_company_llm_extractor():
    main_html = await scrape_html(type="company", name="relevanceai")
    print(extract_company(main_html))

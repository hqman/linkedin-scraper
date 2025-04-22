import json
import os
import random
import asyncio
from playwright.async_api import Page
from ..logging import get_logger
from ..config import LINKEDIN_URL, DEFAULT_TIMEOUT

logger = get_logger()


class ProfileScraper:
    """
    LinkedIn profile and company data scraper
    Focuses on scraping LinkedIn user and company profiles
    """

    def __init__(self, data_dir):
        """
        Initialize the profile scraper

        Args:
            data_dir: Directory to save data
        """
        self.data_dir = data_dir
        self.profile_name = None
        os.makedirs(data_dir, exist_ok=True)

    async def scrape_profile_html(self, page: Page, profile_name: str):
        """
        Scrape LinkedIn profile data

        Args:
            page: Playwright page object
            profile_url: Profile URL

        Returns:
            str: Scraped    HTML
        """
        self.profile_name = profile_name
        profile_url = f"{LINKEDIN_URL}/in/{profile_name}"
        try:
            logger.debug("step1: goto")
            await page.goto(
                profile_url, timeout=DEFAULT_TIMEOUT, wait_until="domcontentloaded"
            )
            # await self._random_sleep(1, 2)

            logger.debug("step3: scroll page")
            await self._scroll_page(page)

            logger.debug("step5: save data")
            html = await page.content()
            return html

        except Exception as e:
            logger.debug(f"Error scraping profile: {e}")
            return {"error": str(e)}

    async def scrape_profile(self, page: Page, profile_name: str):
        """
        Scrape LinkedIn profile data

        Args:
            page: Playwright page object
            profile_url: Profile URL

        Returns:
            dict: Scraped profile data
        """
        self.profile_name = profile_name
        profile_url = f"{LINKEDIN_URL}/in/{profile_name}"
        try:
            logger.debug("step1: goto")
            await page.goto(
                profile_url, timeout=DEFAULT_TIMEOUT, wait_until="domcontentloaded"
            )
            await self._random_sleep(1, 2)

            # Check if page loaded successfully
            if await page.title() == "":
                logger.debug("Page load failed, possibly requiring login")
                return {"error": "Page load failed, possibly requiring login"}

            # Try to detect if blocked by LinkedIn
            # if await page.locator("text=Sign in").count() > 0:
            #     logger.debug("Detected login page, need to log in to LinkedIn first")

            #     return {"error": "Need to log in to LinkedIn first"}

            logger.debug("step3: scroll page")
            await self._scroll_page(page)

            logger.debug("step4: extract profile data")

            profile_data = await self._extract_profile_data(page)

            logger.debug("step5: save data")
            logger.debug(profile_data)
            return profile_data

        except Exception as e:
            logger.debug(f"Error scraping profile: {e}")
            return {"error": str(e)}

    async def _extract_profile_data(self, page: Page):
        """
        Extract profile data from LinkedIn profile page

        Args:
            page: Playwright page object

        Returns:
            dict: Extracted profile data
        """
        profile_data = {}

        # Extract basic information
        await self._extract_basic_info(page, profile_data)

        # Extract about information
        # await self._extract_about_info(page, profile_data)

        # Extract work experience
        # await self._extract_experience(page, profile_data)

        # # Extract education
        # await self._extract_education(page, profile_data)

        # # Extract skills
        # await self._extract_skills(page, profile_data)

        # # Extract certifications
        # await self._extract_certifications(page, profile_data)

        # # Extract languages
        # await self._extract_languages(page, profile_data)
        # Save data
        try:
            # Extract profile ID from URL
            output_file = os.path.join(
                self.data_dir, f"profile_{self.profile_name}.json"
            )
            logger.debug(f"Creating output file path: {output_file}")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(profile_data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Profile data saved to: {output_file}")

        except Exception as e:
            logger.debug(f"Error saving profile data: {e}")

        return profile_data

    async def _extract_basic_info(self, page: Page, profile_data: dict):
        """
        Extract basic information

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        # Set a shorter timeout to avoid long waits
        page.set_default_timeout(DEFAULT_TIMEOUT)  # Set 10 seconds timeout

        # Extract name
        try:
            # Use XPath selector to find the name element
            name_element = page.locator(
                "//span[contains(@class, 'ember-view')]//following::h1[1]"
            )
            if await name_element.count() > 0:
                profile_data["name"] = await name_element.text_content()
            else:
                # If XPath selector fails, fallback to the original CSS selector
                profile_data["name"] = await page.locator(
                    "h1.text-heading-xlarge"
                ).text_content()
            profile_data["name"] = profile_data["name"].strip()
        except Exception as e:
            logger.debug(f"Error extracting name: {e}")
            profile_data["name"] = "Name not found"

        # Extract headline/position
        try:
            # Try to use XPath selector to find headline element
            headline_xpath_selector = (
                '//*[@id="profile-content"]/div/div[2]/div/div/main/'
                "section[1]/div[2]/div[2]/div[1]/div[2]"
            )
            headline_xpath = page.locator(headline_xpath_selector)
            if await headline_xpath.count() > 0:
                profile_data["headline"] = await headline_xpath.text_content()
            else:
                # If XPath selector fails, fallback to the original CSS selector
                profile_data["headline"] = await page.locator(
                    "div.text-body-medium"
                ).first.text_content()
            profile_data["headline"] = profile_data["headline"].strip()
        except Exception as e:
            logger.debug(f"Error extracting headline: {e}")
            profile_data["headline"] = "Position not found"

        # Extract location
        try:
            # Try to use XPath selector to find location element
            location_xpath_selector = (
                '//*[@id="profile-content"]/div/div[2]/div/div/main/'
                "section[1]/div[2]/div[2]/div[2]/span[1]"
            )
            location_xpath = page.locator(location_xpath_selector)
            if await location_xpath.count() > 0:
                profile_data["location"] = await location_xpath.text_content()
            else:
                # If XPath selector fails, fallback to the original CSS selector
                profile_data["location"] = await page.locator(
                    "span.text-body-small"
                ).first.text_content()
            profile_data["location"] = profile_data["location"].strip()
        except Exception as e:
            logger.debug(f"Error extracting location: {e}")
            profile_data["location"] = "Location not found"
        # Extract company information
        try:
            # Try to use XPath selector to find company information element
            company_xpath_selector = (
                '//*[@id="profile-content"]/div/div[2]/div/div/main/'
                "section[1]/div[2]/div[2]/ul/li[1]/button/span/div"
            )
            company_xpath = page.locator(company_xpath_selector)
            if await company_xpath.count() > 0:
                profile_data["company"] = await company_xpath.text_content()
                profile_data["company"] = profile_data["company"].strip()
            else:
                # If XPath selector fails, do not try other selectors, leave empty
                profile_data["company"] = ""
        except Exception as e:
            logger.debug(f"Error extracting company information: {e}")
            profile_data["company"] = "Company information not found"

        # Extract education information
        try:
            # Try to use XPath selector to find education information element
            education_xpath_selector = (
                '//*[@id="profile-content"]/div/div[2]/div/div/main/'
                "section[1]/div[2]/div[2]/ul/li[2]/button/span/div"
            )
            education_xpath = page.locator(education_xpath_selector)
            if await education_xpath.count() > 0:
                profile_data["education"] = await education_xpath.text_content()
                profile_data["education"] = profile_data["education"].strip()
            else:
                # If XPath selector fails, do not try other selectors, leave empty
                profile_data["education"] = ""
        except Exception as e:
            logger.debug(f"Error extracting education information: {e}")
            profile_data["education"] = "Education information not found"
        try:
            # Click "Contact Information" button
            contact_button = page.locator('a[href="#contact-info"]')
            if await contact_button.count() > 0:
                await contact_button.click()
                await self._random_sleep(1, 2)

                # Extract contact information
                contact_info = {}

                # Extract email
                email_locator = page.locator(
                    'section.pv-contact-info a[href^="mailto:"]'
                )
                if await email_locator.count() > 0:
                    contact_info["email"] = await email_locator.text_content()

                # Extract LinkedIn URL
                linkedin_sel = (
                    'section.pv-contact-info a[href^="https://www.linkedin.com/in/"]'
                )
                linkedin_locator = page.locator(linkedin_sel)
                if await linkedin_locator.count() > 0:
                    contact_info["linkedin"] = await linkedin_locator.get_attribute(
                        "href"
                    )

                # Extract website
                website_sel = (
                    'section.pv-contact-info a[href^="http"]'
                    ':not([href^="https://www.linkedin.com"])'
                )
                website_locator = page.locator(website_sel)
                if await website_locator.count() > 0:
                    contact_info["website"] = await website_locator.get_attribute(
                        "href"
                    )

                # Extract phone
                phone_locator = page.locator(
                    'section.pv-contact-info span:has-text("+")'
                )
                if await phone_locator.count() > 0:
                    contact_info["phone"] = await phone_locator.text_content()

                profile_data["contact_info"] = contact_info

                # Close contact information dialog
                close_button = page.locator(
                    'button[aria-label="Close"], button[aria-label="Close"]'
                )
                if await close_button.count() > 0:
                    await close_button.click()
                    await self._random_sleep(1, 2)
        except Exception as e:
            logger.debug(f"Error extracting contact information: {e}")
            profile_data["contact_info"] = {}

    async def _extract_about_info(self, page: Page, profile_data: dict):
        """
        Extract about information

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        try:
            # Try multiple possible selectors
            about_selectors = [
                'div#about ~ div.display-flex span[aria-hidden="true"]',
                # Split long selectors
                'section[data-section="summary"] div.pv-shared-text-with-see-more '
                'span[aria-hidden="true"]',
                "section.pv-about-section p",
                'div.text-body-medium span[aria-hidden="true"]',
            ]

            for selector in about_selectors:
                about_locator = page.locator(selector)
                if await about_locator.count() > 0:
                    profile_data["about"] = await about_locator.text_content()
                    profile_data["about"] = profile_data["about"].strip()
                    break

            if "about" not in profile_data:
                profile_data["about"] = "About information not found"
        except Exception as e:
            logger.debug(f"Error extracting about information: {e}")
            profile_data["about"] = "Error extracting about information"

    async def _extract_experience(self, page: Page, profile_data: dict):
        """
        Extract work experience

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        try:
            experiences = []

            # Try multiple possible selectors
            experience_section_selectors = [
                "section#experience",
                'section[data-section="experience"]',
                "section.experience-section",
            ]

            for section_selector in experience_section_selectors:
                section = page.locator(section_selector)
                if await section.count() > 0:
                    # Try to get experience list items
                    experience_items_selectors = [
                        "ul.pvs-list > li",
                        "ul.experience-list > li",
                        "div.pvs-entity",
                    ]

                    for items_selector in experience_items_selectors:
                        items = section.locator(items_selector)
                        count = await items.count()

                        if count > 0:
                            for i in range(count):
                                item = items.nth(i)
                                experience = {}

                                # Extract title
                                try:
                                    title_selectors = [
                                        "span.mr1.t-bold",
                                        "span.pv-entity__secondary-title",
                                        "span.t-14.t-bold",
                                        "span.pvs-entity__path-node",
                                    ]

                                    for title_selector in title_selectors:
                                        title_locator = item.locator(title_selector)
                                        if await title_locator.count() > 0:
                                            experience["title"] = (
                                                await title_locator.text_content()
                                            )
                                            experience["title"] = experience[
                                                "title"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting title: {e}")

                                # Extract company
                                try:
                                    company_selectors = [
                                        "span.t-14.t-normal",
                                        "span.pv-entity__secondary-title",
                                        "span.pvs-entity__secondary-title",
                                    ]

                                    for company_selector in company_selectors:
                                        company_locator = item.locator(company_selector)
                                        if await company_locator.count() > 0:
                                            experience["company"] = (
                                                await company_locator.text_content()
                                            )
                                            experience["company"] = experience[
                                                "company"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting company: {e}")

                                # Extract duration
                                try:
                                    duration_selectors = [
                                        "span.t-14.t-normal.t-black--light",
                                        "span.pv-entity__date-range",
                                        "span.pvs-entity__caption-text",
                                    ]

                                    for duration_selector in duration_selectors:
                                        duration_locator = item.locator(
                                            duration_selector
                                        )
                                        if await duration_locator.count() > 0:
                                            experience["duration"] = (
                                                await duration_locator.text_content()
                                            )
                                            experience["duration"] = experience[
                                                "duration"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting duration: {e}")

                                # Extract location
                                try:
                                    location_selectors = [
                                        "span.t-14.t-normal.t-black--light:nth-child(2)",
                                        "span.pv-entity__location",
                                        "span.pvs-entity__caption-text:nth-child(2)",
                                    ]

                                    for location_selector in location_selectors:
                                        location_locator = item.locator(
                                            location_selector
                                        )
                                        if await location_locator.count() > 0:
                                            experience["location"] = (
                                                await location_locator.text_content()
                                            )
                                            experience["location"] = experience[
                                                "location"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting location: {e}")

                                # Extract description
                                try:
                                    description_selectors = [
                                        "div.pv-entity__description",
                                        "div.pvs-entity__description",
                                        "p.pv-shared-text-with-see-more",
                                    ]

                                    for description_selector in description_selectors:
                                        description_locator = item.locator(
                                            description_selector
                                        )
                                        if await description_locator.count() > 0:
                                            experience["description"] = (
                                                await description_locator.text_content()
                                            )
                                            experience["description"] = experience[
                                                "description"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting description: {e}")

                                # If at least one title or company information, add to experience list
                                if "title" in experience or "company" in experience:
                                    experiences.append(experience)

                            break  # Found and processed experience item, exit loop

            profile_data["experiences"] = experiences
        except Exception as e:
            logger.debug(f"Error extracting experience: {e}")
            profile_data["experiences"] = []

    async def _extract_education(self, page: Page, profile_data: dict):
        """
        Extract education

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        try:
            educations = []

            # Try multiple possible selectors
            education_section_selectors = [
                "section#education",
                'section[data-section="education"]',
                "section.education-section",
            ]

            for section_selector in education_section_selectors:
                section = page.locator(section_selector)
                if await section.count() > 0:
                    # Try to get education list items
                    education_items_selectors = [
                        "ul.pvs-list > li",
                        "ul.education-list > li",
                        "div.pvs-entity",
                    ]

                    for items_selector in education_items_selectors:
                        items = section.locator(items_selector)
                        count = await items.count()

                        if count > 0:
                            for i in range(count):
                                item = items.nth(i)
                                education = {}

                                # Extract school
                                try:
                                    school_selectors = [
                                        "span.mr1.t-bold",
                                        "h3.pv-entity__school-name",
                                        "span.t-14.t-bold",
                                        "span.pvs-entity__path-node",
                                    ]

                                    for school_selector in school_selectors:
                                        school_locator = item.locator(school_selector)
                                        if await school_locator.count() > 0:
                                            education["school"] = (
                                                await school_locator.text_content()
                                            )
                                            education["school"] = education[
                                                "school"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting school: {e}")

                                # Extract degree
                                try:
                                    degree_selectors = [
                                        "span.t-14.t-normal",
                                        "span.pv-entity__secondary-title",
                                        "span.pvs-entity__secondary-title",
                                    ]

                                    for degree_selector in degree_selectors:
                                        degree_locator = item.locator(degree_selector)
                                        if await degree_locator.count() > 0:
                                            education["degree"] = (
                                                await degree_locator.text_content()
                                            )
                                            education["degree"] = education[
                                                "degree"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting degree: {e}")

                                # Extract duration
                                try:
                                    duration_selectors = [
                                        "span.t-14.t-normal.t-black--light",
                                        "span.pv-entity__date-range",
                                        "span.pvs-entity__caption-text",
                                    ]

                                    for duration_selector in duration_selectors:
                                        duration_locator = item.locator(
                                            duration_selector
                                        )
                                        if await duration_locator.count() > 0:
                                            education["duration"] = (
                                                await duration_locator.text_content()
                                            )
                                            education["duration"] = education[
                                                "duration"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting duration: {e}")

                                # If at least one school information, add to education list
                                if "school" in education:
                                    educations.append(education)

                            break  # Found and processed education item, exit loop

            profile_data["educations"] = educations
        except Exception as e:
            logger.debug(f"Error extracting education: {e}")
            profile_data["educations"] = []

    async def _extract_skills(self, page: Page, profile_data: dict):
        """
        Extract skills

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        try:
            skills = []

            # Try multiple possible selectors
            skills_section_selectors = [
                "section#skills",
                'section[data-section="skills"]',
                "section.pv-skill-categories-section",
            ]

            for section_selector in skills_section_selectors:
                section = page.locator(section_selector)
                if await section.count() > 0:
                    # Try to get skill list items
                    skills_items_selectors = [
                        "ul.pvs-list > li",
                        "ol.pv-skill-categories-section__top-skills > li",
                        "div.pvs-entity",
                    ]

                    for items_selector in skills_items_selectors:
                        items = section.locator(items_selector)
                        count = await items.count()

                        if count > 0:
                            for i in range(count):
                                item = items.nth(i)

                                # Extract skill name
                                try:
                                    skill_selectors = [
                                        "span.mr1.t-bold",
                                        "span.pv-skill-category-entity__name-text",
                                        "span.t-14.t-bold",
                                        "span.pvs-entity__path-node",
                                    ]

                                    for skill_selector in skill_selectors:
                                        skill_locator = item.locator(skill_selector)
                                        if await skill_locator.count() > 0:
                                            skill = await skill_locator.text_content()
                                            skill = skill.strip()
                                            if skill and skill not in skills:
                                                skills.append(skill)
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting skill: {e}")

                            break  # Found and processed skill item, exit loop

            profile_data["skills"] = skills
        except Exception as e:
            logger.debug(f"Error extracting skills: {e}")
            profile_data["skills"] = []

    async def _extract_certifications(self, page: Page, profile_data: dict):
        """
        Extract certifications

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        try:
            certifications = []

            # Try multiple possible selectors
            certifications_section_selectors = [
                "section#certifications",
                'section[data-section="certifications"]',
                "section.pv-certifications-section",
            ]

            for section_selector in certifications_section_selectors:
                section = page.locator(section_selector)
                if await section.count() > 0:
                    # Try to get certification list items
                    certifications_items_selectors = [
                        "ul.pvs-list > li",
                        "ul.pv-certifications__list > li",
                        "div.pvs-entity",
                    ]

                    for items_selector in certifications_items_selectors:
                        items = section.locator(items_selector)
                        count = await items.count()

                        if count > 0:
                            for i in range(count):
                                item = items.nth(i)
                                certification = {}

                                # Extract certification name
                                try:
                                    name_selectors = [
                                        "span.mr1.t-bold",
                                        "h3.pv-certifications__name",
                                        "span.t-14.t-bold",
                                        "span.pvs-entity__path-node",
                                    ]

                                    for name_selector in name_selectors:
                                        name_locator = item.locator(name_selector)
                                        if await name_locator.count() > 0:
                                            certification["name"] = (
                                                await name_locator.text_content()
                                            )
                                            certification["name"] = certification[
                                                "name"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(
                                        f"Error extracting certification name: {e}"
                                    )

                                # Extract issuer
                                try:
                                    issuer_selectors = [
                                        "span.t-14.t-normal",
                                        "span.pv-certifications__subtitle",
                                        "span.pvs-entity__secondary-title",
                                    ]

                                    for issuer_selector in issuer_selectors:
                                        issuer_locator = item.locator(issuer_selector)
                                        if await issuer_locator.count() > 0:
                                            certification["issuer"] = (
                                                await issuer_locator.text_content()
                                            )
                                            certification["issuer"] = certification[
                                                "issuer"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting issuer: {e}")

                                # Extract date
                                try:
                                    date_selectors = [
                                        "span.t-14.t-normal.t-black--light",
                                        "span.pv-certifications__date-range",
                                        "span.pvs-entity__caption-text",
                                    ]

                                    for date_selector in date_selectors:
                                        date_locator = item.locator(date_selector)
                                        if await date_locator.count() > 0:
                                            certification["date"] = (
                                                await date_locator.text_content()
                                            )
                                            certification["date"] = certification[
                                                "date"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting date: {e}")

                                # If at least one certification name, add to certification list
                                if "name" in certification:
                                    certifications.append(certification)

                            break  # Found and processed certification item, exit loop

            profile_data["certifications"] = certifications
        except Exception as e:
            logger.debug(f"Error extracting certifications: {e}")
            profile_data["certifications"] = []

    async def _extract_languages(self, page: Page, profile_data: dict):
        """
        Extract languages

        Args:
            page: Playwright page object
            profile_data: Profile data dictionary
        """
        try:
            languages = []

            # Try multiple possible selectors
            languages_section_selectors = [
                "section#languages",
                'section[data-section="languages"]',
                "section.pv-languages-section",
            ]

            for section_selector in languages_section_selectors:
                section = page.locator(section_selector)
                if await section.count() > 0:
                    # Try to get language list items
                    languages_items_selectors = [
                        "ul.pvs-list > li",
                        "ul.pv-languages__list > li",
                        "div.pvs-entity",
                    ]

                    for items_selector in languages_items_selectors:
                        items = section.locator(items_selector)
                        count = await items.count()

                        if count > 0:
                            for i in range(count):
                                item = items.nth(i)
                                language = {}

                                # Extract language name
                                try:
                                    name_selectors = [
                                        "span.mr1.t-bold",
                                        "h3.pv-languages__name",
                                        "span.t-14.t-bold",
                                        "span.pvs-entity__path-node",
                                    ]

                                    for name_selector in name_selectors:
                                        name_locator = item.locator(name_selector)
                                        if await name_locator.count() > 0:
                                            language["name"] = (
                                                await name_locator.text_content()
                                            )
                                            language["name"] = language["name"].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting language name: {e}")

                                # Extract proficiency
                                try:
                                    proficiency_selectors = [
                                        "span.t-14.t-normal",
                                        "span.pv-languages__proficiency",
                                        "span.pvs-entity__secondary-title",
                                    ]

                                    for proficiency_selector in proficiency_selectors:
                                        proficiency_locator = item.locator(
                                            proficiency_selector
                                        )
                                        if await proficiency_locator.count() > 0:
                                            language["proficiency"] = (
                                                await proficiency_locator.text_content()
                                            )
                                            language["proficiency"] = language[
                                                "proficiency"
                                            ].strip()
                                            break
                                except Exception as e:
                                    logger.debug(f"Error extracting proficiency: {e}")

                                # If at least one language name, add to language list
                                if "name" in language:
                                    languages.append(language)

                            break  # Found and processed language item, exit loop

            profile_data["languages"] = languages
        except Exception as e:
            logger.debug(f"Error extracting languages: {e}")
            profile_data["languages"] = []

    async def _scroll_page(self, page: Page):
        """
        Scroll page to load more content

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

            # Calculate scroll times
            scroll_times = min(10, max(3, height // viewport_height))

            # Scroll page multiple times, simulating human reading
            for i in range(scroll_times):
                # Calculate next scroll position, add some randomness
                next_pos = int(
                    (i + 1) * height / scroll_times * (0.8 + 0.4 * random.random())
                )

                # Safe execute scroll
                await page.evaluate(
                    f"""() => {{
                    if (typeof window.scrollTo === 'function') {{
                        window.scrollTo(0, {next_pos});
                    }}
                }}"""
                )

                # Random pause, simulating reading
                await self._random_sleep(0.5, 2)

                # Occasionally scroll up a little, simulating looking back at content
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
        Randomly wait for a while, simulating human behavior

        Args:
            min_seconds: Minimum wait seconds
            max_seconds: Maximum wait seconds
        """
        await asyncio.sleep(random.uniform(min_seconds, max_seconds))

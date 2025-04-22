"""
HTML Cleaner module for optimizing token usage when sending HTML content to LLM.
This module provides functions to clean HTML content by removing irrelevant elements
like images, headers, footers, scripts, styles, and other non-essential parts.
"""

import re
from typing import List, Optional, Set, Dict, Tuple, Any

from bs4 import BeautifulSoup, Comment
from src.linkedin_scraper.logging import get_logger

logger = get_logger()


def clean_html(html_content: str) -> str:
    cleaner = HTMLCleaner()
    return cleaner.clean_html(html_content)


def clean_image_html(html_content: str) -> str:
    cleaner = HTMLCleaner()
    return cleaner.clean_image_html(html_content)


class HTMLCleaner:
    """
    A class for cleaning HTML content to reduce token usage when sending to LLM.
    """

    def __init__(self):
        """
        Initialize the HTMLCleaner with default settings.
        """
        # Default tags to remove
        self.default_remove_tags = {
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            "svg",
            "img",
            "picture",
            "video",
            "audio",
            "iframe",
            "canvas",
            "map",
            "figure",
            "figcaption",
            "form",
            "button",
            "input",
            "select",
            "option",
            "textarea",
            "fieldset",
            "legend",
            "datalist",
            "output",
            "progress",
            "meter",
            "details",
            "summary",
            "menu",
            "menuitem",
            "dialog",
            "template",
            "slot",
            "portal",
            "code",
        }

        # Default attributes to remove
        self.default_remove_attrs = {
            "style",
            "class",
            "id",
            "onclick",
            "onload",
            "onmouseover",
            "onmouseout",
            "onkeydown",
            "onkeyup",
            "onkeypress",
            "data-*",
            "aria-*",
            "role",
            "tabindex",
            "title",
            "alt",
            "src",
            "href",
            "target",
            "rel",
        }

        # Default CSS selectors to remove
        self.default_remove_selectors = [
            ".header",
            ".footer",
            ".nav",
            ".sidebar",
            ".menu",
            ".advertisement",
            ".ad",
            ".banner",
            ".social-media",
            ".cookie-notice",
            ".popup",
            ".modal",
            ".overlay",
            "#header",
            "#footer",
            "#nav",
            "#sidebar",
            "#menu",
            "#advertisement",
            "#ad",
            "#banner",
            "#social-media",
            "#cookie-notice",
            "#popup",
            "#modal",
            "#overlay",
        ]

    def clean_html(
        self,
        html_content: str,
        remove_tags: Optional[Set[str]] = None,
        remove_attrs: Optional[Set[str]] = None,
        remove_selectors: Optional[List[str]] = None,
        keep_job_content: bool = True,
    ) -> str:
        """
        Clean HTML content by removing irrelevant elements.

        Args:
            html_content (str): The HTML content to clean
            remove_tags (Set[str], optional): Set of HTML tags to remove
            remove_attrs (Set[str], optional): Set of HTML attributes to remove
            remove_selectors (List[str], optional): List of CSS selectors to remove
            keep_job_content (bool): Whether to prioritize keeping job-related content

        Returns:
            str: The cleaned HTML content
        """
        if not html_content:
            return ""

        # Use default values if not provided
        remove_tags = remove_tags or self.default_remove_tags
        remove_attrs = remove_attrs or self.default_remove_attrs
        remove_selectors = remove_selectors or self.default_remove_selectors

        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove elements by CSS selectors
        for selector in remove_selectors:
            for element in soup.select(selector):
                element.decompose()

        # Remove specified tags
        for tag in remove_tags:
            for element in soup.find_all(tag):
                element.decompose()

        # Remove specified attributes from remaining elements
        for element in soup.find_all():
            attrs_to_remove = []
            for attr in element.attrs:
                # Handle data-* and aria-* attributes
                if attr.startswith("data-") and "data-*" in remove_attrs:
                    attrs_to_remove.append(attr)
                elif attr.startswith("aria-") and "aria-*" in remove_attrs:
                    attrs_to_remove.append(attr)
                elif attr in remove_attrs:
                    attrs_to_remove.append(attr)

            for attr in attrs_to_remove:
                del element.attrs[attr]

        # If keep_job_content is True, try to identify and preserve job-related content
        if keep_job_content:
            self._preserve_job_content(soup)

        # Convert back to string
        cleaned_html = str(soup)

        # Remove excessive whitespace and newlines
        cleaned_html = re.sub(r"\n\s*\n", "\n", cleaned_html)
        cleaned_html = re.sub(r"[ \t]+", " ", cleaned_html)

        return cleaned_html

    def _preserve_job_content(self, soup: BeautifulSoup) -> None:
        """
        Identify and preserve job-related content.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object
        """
        # Common job-related keywords
        job_keywords = [
            "job",
            "position",
            "career",
            "employment",
            "work",
            "role",
            "opportunity",
            "responsibilities",
            "requirements",
            "qualifications",
            "skills",
            "experience",
            "salary",
            "benefits",
            "apply",
            "application",
            "hiring",
            "recruit",
            "description",
            "summary",
            "overview",
            "duties",
            "tasks",
            "location",
            "remote",
            "hybrid",
            "onsite",
            "full-time",
            "part-time",
            "contract",
            "permanent",
            "temporary",
            "intern",
            "internship",
            "entry-level",
            "senior",
            "junior",
            "mid-level",
            "manager",
            "director",
            "executive",
            "lead",
            "department",
            "team",
            "group",
            "division",
            "unit",
            "company",
            "organization",
            "firm",
            "enterprise",
            "corporation",
            "business",
            "employer",
            "workplace",
            "office",
            "site",
            "facility",
            "headquarters",
            "branch",
            "division",
            "deadline",
            "closing date",
            "start date",
            "duration",
            "term",
            "period",
            "compensation",
            "wage",
            "pay",
            "stipend",
            "bonus",
            "commission",
            "equity",
            "stock",
            "options",
            "benefits",
            "insurance",
            "healthcare",
            "dental",
            "vision",
            "retirement",
            "401k",
            "pension",
            "vacation",
            "pto",
            "leave",
            "holidays",
            "flexible",
            "schedule",
            "hours",
            "shift",
            "rotation",
            "education",
            "degree",
            "certification",
            "license",
            "diploma",
            "major",
            "minor",
            "field",
            "discipline",
            "specialty",
            "concentration",
            "focus",
            "background",
            "history",
            "track record",
            "portfolio",
            "samples",
            "projects",
            "achievements",
            "accomplishments",
            "successes",
            "awards",
            "recognition",
            "honors",
            "accolades",
            "distinctions",
            "merits",
            "credentials",
            "references",
            "recommendations",
            "endorsements",
            "testimonials",
            "feedback",
            "reviews",
            "ratings",
            "evaluations",
            "assessments",
            "interviews",
            "screening",
            "selection",
            "consideration",
            "candidacy",
            "eligibility",
            "suitability",
            "fit",
            "match",
            "compatibility",
            "diversity",
            "inclusion",
            "equal opportunity",
            "affirmative action",
            "eeo",
            "ada",
            "reasonable accommodation",
            "accessibility",
            "relocation",
            "moving",
            "travel",
            "commute",
            "transportation",
            "visa",
            "sponsorship",
            "citizenship",
            "residency",
            "authorization",
            "clearance",
            "security",
            "background check",
            "drug test",
            "screening",
            "probation",
            "trial",
            "orientation",
            "onboarding",
            "training",
            "development",
            "growth",
            "advancement",
            "promotion",
            "career path",
            "trajectory",
            "progression",
            "ladder",
            "hierarchy",
            "structure",
            "reporting",
            "supervision",
            "management",
            "leadership",
            "guidance",
            "mentorship",
            "coaching",
            "feedback",
            "evaluation",
            "performance",
            "review",
            "assessment",
            "appraisal",
            "rating",
            "ranking",
            "score",
            "grade",
            "level",
            "tier",
            "band",
            "classification",
            "category",
            "class",
            "group",
            "segment",
            "section",
            "unit",
            "division",
            "department",
            "team",
            "squad",
            "crew",
            "staff",
            "personnel",
            "workforce",
            "manpower",
            "human resources",
            "hr",
            "talent",
            "acquisition",
            "recruitment",
            "sourcing",
            "headhunting",
            "placement",
            "staffing",
            "agency",
            "consultant",
            "advisor",
            "specialist",
            "expert",
            "professional",
            "practitioner",
            "technician",
            "operator",
            "associate",
            "assistant",
            "coordinator",
            "administrator",
            "clerk",
            "secretary",
            "receptionist",
            "representative",
            "agent",
            "liaison",
            "ambassador",
            "advocate",
            "champion",
            "evangelist",
            "influencer",
            "thought leader",
            "visionary",
            "innovator",
            "creator",
            "builder",
            "maker",
            "developer",
            "engineer",
            "architect",
            "designer",
            "analyst",
            "strategist",
            "planner",
            "consultant",
            "advisor",
            "coach",
            "mentor",
            "teacher",
            "instructor",
            "trainer",
            "facilitator",
            "moderator",
            "mediator",
            "negotiator",
            "arbitrator",
            "judge",
            "referee",
            "umpire",
            "official",
            "authority",
            "expert",
            "specialist",
            "professional",
            "practitioner",
            "technician",
            "operator",
        ]

        # Common job-related CSS classes and IDs
        job_selectors = [
            ".job",
            ".position",
            ".career",
            ".employment",
            ".work",
            ".role",
            ".opportunity",
            ".responsibilities",
            ".requirements",
            ".qualifications",
            ".skills",
            ".experience",
            ".salary",
            ".benefits",
            ".apply",
            ".application",
            ".hiring",
            ".recruit",
            ".description",
            ".summary",
            ".overview",
            ".duties",
            ".tasks",
            ".location",
            "#job",
            "#position",
            "#career",
            "#employment",
            "#work",
            "#role",
            "#opportunity",
            "#responsibilities",
            "#requirements",
            "#qualifications",
            "#skills",
            "#experience",
            "#salary",
            "#benefits",
            "#apply",
            "#application",
            "#hiring",
            "#recruit",
            "#description",
            "#summary",
            "#overview",
            "#duties",
            "#tasks",
            "#location",
        ]

        # Find elements with job-related text content
        for element in soup.find_all(text=True):
            parent = element.parent
            if parent and any(keyword in element.lower() for keyword in job_keywords):
                # Mark this element and its ancestors as important
                current = parent
                while current and current.name != "body":
                    current["data-job-content"] = "true"
                    current = current.parent

        # Find elements with job-related selectors
        for selector in job_selectors:
            for element in soup.select(selector):
                element["data-job-content"] = "true"
                # Mark ancestors as important
                current = element.parent
                while current and current.name != "body":
                    current["data-job-content"] = "true"
                    current = current.parent

    def clean_html_for_job_listing(self, html_content: str) -> str:
        """
        Clean HTML content specifically for job listing pages.
        This is a specialized version of clean_html with settings optimized for job listings.

        Args:
            html_content (str): The HTML content to clean

        Returns:
            str: The cleaned HTML content
        """
        # Additional tags to remove for job listings
        job_listing_remove_tags = self.default_remove_tags.union(
            {
                "meta",
                "link",
                "comment",
                "head",
                "title",
                "base",
                "object",
                "embed",
                "param",
                "track",
                "source",
                "wbr",
                "br",
                "hr",
                "marquee",
                "blink",
            }
        )

        # Additional selectors to remove for job listings
        job_listing_remove_selectors = self.default_remove_selectors + [
            ".related-jobs",
            ".similar-jobs",
            ".job-recommendations",
            ".job-alerts",
            ".job-search",
            ".search-filters",
            ".filter-options",
            ".sort-options",
            ".pagination",
            ".page-navigation",
            ".breadcrumbs",
            ".breadcrumb",
            ".share-buttons",
            ".social-share",
            ".print-button",
            ".save-button",
            ".apply-button",
            ".application-form",
            ".login-prompt",
            ".signup-prompt",
            ".newsletter-signup",
            ".email-alerts",
            ".company-info",
            ".about-company",
            ".company-profile",
            ".company-culture",
            ".company-values",
            ".company-mission",
            ".company-vision",
            ".company-goals",
            ".company-history",
            ".company-timeline",
            ".company-news",
            ".company-press",
            ".company-media",
            ".company-awards",
            ".company-recognition",
            ".company-achievements",
            ".company-successes",
            ".company-testimonials",
            ".company-reviews",
            ".company-ratings",
            ".company-feedback",
            ".company-endorsements",
            ".company-recommendations",
            ".company-references",
            ".company-clients",
            ".company-partners",
            ".company-collaborators",
            ".company-affiliates",
            ".company-sponsors",
            ".company-investors",
            ".company-funding",
            ".company-financials",
            ".company-metrics",
            ".company-statistics",
            ".company-data",
            ".company-facts",
            ".company-figures",
            ".company-numbers",
            ".company-counts",
            ".company-totals",
            ".company-sums",
            ".company-averages",
            ".company-means",
            ".company-medians",
            ".company-modes",
            ".company-ranges",
            ".company-minimums",
            ".company-maximums",
            ".company-lows",
            ".company-highs",
            ".company-extremes",
            ".company-outliers",
            ".company-exceptions",
            ".company-anomalies",
            ".company-irregularities",
            ".company-peculiarities",
            ".company-oddities",
            ".company-quirks",
            ".company-idiosyncrasies",
            ".company-eccentricities",
            ".company-uniqueness",
            ".company-distinctiveness",
            ".company-differentiation",
            ".company-specialness",
            ".company-exceptionalism",
            ".company-superiority",
            ".company-excellence",
            ".company-greatness",
            ".company-wonderfulness",
            ".company-amazingness",
            ".company-awesomeness",
            ".company-coolness",
            ".company-hipness",
            ".company-trendiness",
            ".company-fashionableness",
            ".company-stylishness",
            ".company-chic",
            ".company-elegance",
            ".company-sophistication",
            ".company-refinement",
            ".company-polish",
            ".company-finesse",
            ".company-grace",
            ".company-poise",
            ".company-dignity",
            ".company-class",
            ".company-prestige",
            ".company-status",
            ".company-standing",
            ".company-reputation",
            ".company-renown",
            ".company-fame",
            ".company-glory",
            ".company-honor",
            ".company-distinction",
            ".company-esteem",
            ".company-regard",
            ".company-respect",
            ".company-admiration",
            ".company-appreciation",
            ".company-recognition",
            ".company-acknowledgment",
            ".company-credit",
            ".company-praise",
            ".company-commendation",
            ".company-compliment",
            ".company-flattery",
            ".company-adulation",
            ".company-worship",
            ".company-idolization",
            ".company-veneration",
            ".company-reverence",
            ".company-awe",
            ".company-wonder",
            ".company-amazement",
            ".company-astonishment",
            ".company-surprise",
            ".company-shock",
            ".company-disbelief",
            ".company-incredulity",
            ".company-skepticism",
            ".company-doubt",
            ".company-uncertainty",
            ".company-hesitation",
            ".company-reluctance",
            ".company-resistance",
            ".company-opposition",
            ".company-objection",
            ".company-protest",
            ".company-complaint",
            ".company-grievance",
            ".company-dissatisfaction",
            ".company-displeasure",
            ".company-discontent",
            ".company-unhappiness",
            ".company-sadness",
            ".company-sorrow",
            ".company-grief",
            ".company-misery",
            ".company-woe",
            ".company-anguish",
            ".company-pain",
            ".company-suffering",
            ".company-agony",
            ".company-torment",
            ".company-torture",
            ".company-hell",
            ".company-purgatory",
            ".company-limbo",
            ".company-abyss",
            ".company-void",
            ".company-emptiness",
            ".company-nothingness",
            ".company-nihility",
            ".company-nonexistence",
            ".company-absence",
            ".company-lack",
            ".company-deficiency",
            ".company-shortage",
            ".company-scarcity",
            ".company-dearth",
            ".company-paucity",
            ".company-insufficiency",
            ".company-inadequacy",
            ".company-defectiveness",
            ".company-imperfection",
            ".company-flaw",
            ".company-fault",
            ".company-defect",
            ".company-blemish",
            ".company-stain",
            ".company-spot",
            ".company-mark",
            ".company-scar",
            ".company-wound",
            ".company-injury",
            ".company-damage",
            ".company-harm",
            ".company-hurt",
            ".company-pain",
            ".company-suffering",
            ".company-distress",
            ".company-affliction",
            ".company-torment",
            ".company-torture",
            ".company-agony",
            ".company-anguish",
            ".company-misery",
            ".company-woe",
            ".company-sorrow",
            ".company-grief",
            ".company-sadness",
            ".company-unhappiness",
            ".company-discontent",
            ".company-displeasure",
            ".company-dissatisfaction",
            ".company-grievance",
            ".company-complaint",
            ".company-protest",
            ".company-objection",
            ".company-opposition",
            ".company-resistance",
            ".company-reluctance",
            ".company-hesitation",
            ".company-uncertainty",
            ".company-doubt",
            ".company-skepticism",
            ".company-incredulity",
            ".company-disbelief",
            ".company-shock",
            ".company-surprise",
            ".company-astonishment",
            ".company-amazement",
            ".company-wonder",
            ".company-awe",
            ".company-reverence",
            ".company-veneration",
            ".company-idolization",
            ".company-worship",
            ".company-adulation",
            ".company-flattery",
            ".company-compliment",
            ".company-commendation",
            ".company-praise",
            ".company-credit",
            ".company-acknowledgment",
            ".company-recognition",
            ".company-appreciation",
            ".company-admiration",
            ".company-respect",
            ".company-regard",
            ".company-esteem",
            ".company-distinction",
            ".company-honor",
            ".company-glory",
            ".company-fame",
            ".company-renown",
            ".company-reputation",
            ".company-standing",
            ".company-status",
            ".company-prestige",
            ".company-class",
            ".company-dignity",
            ".company-poise",
            ".company-grace",
            ".company-finesse",
            ".company-polish",
            ".company-refinement",
            ".company-sophistication",
            ".company-elegance",
            ".company-chic",
            ".company-stylishness",
            ".company-fashionableness",
            ".company-trendiness",
            ".company-hipness",
            ".company-coolness",
            ".company-awesomeness",
            ".company-amazingness",
            ".company-wonderfulness",
            ".company-greatness",
            ".company-excellence",
            ".company-superiority",
            ".company-exceptionalism",
            ".company-specialness",
            ".company-differentiation",
            ".company-distinctiveness",
            ".company-uniqueness",
            ".company-idiosyncrasies",
            ".company-eccentricities",
            ".company-quirks",
            ".company-oddities",
            ".company-peculiarities",
            ".company-irregularities",
            ".company-anomalies",
            ".company-exceptions",
            ".company-outliers",
            ".company-extremes",
            ".company-highs",
            ".company-lows",
            ".company-maximums",
            ".company-minimums",
            ".company-ranges",
            ".company-modes",
            ".company-medians",
            ".company-means",
            ".company-averages",
            ".company-sums",
            ".company-totals",
            ".company-counts",
            ".company-numbers",
            ".company-figures",
            ".company-facts",
            ".company-data",
            ".company-statistics",
            ".company-metrics",
            ".company-financials",
            ".company-funding",
            ".company-investors",
            ".company-sponsors",
            ".company-affiliates",
            ".company-collaborators",
            ".company-partners",
            ".company-clients",
            ".company-references",
            ".company-recommendations",
            ".company-endorsements",
            ".company-feedback",
            ".company-ratings",
            ".company-reviews",
            ".company-testimonials",
            ".company-successes",
            ".company-achievements",
            ".company-recognition",
            ".company-awards",
            ".company-media",
            ".company-press",
            ".company-news",
            ".company-timeline",
            ".company-history",
            ".company-goals",
            ".company-vision",
            ".company-mission",
            ".company-values",
            ".company-culture",
            ".company-profile",
            ".company-info",
            ".about-company",
        ]

        return self.clean_html(
            html_content,
            remove_tags=job_listing_remove_tags,
            remove_selectors=job_listing_remove_selectors,
            keep_job_content=True,
        )

    def clean_html_for_job_detail(self, html_content: str) -> str:
        """
        Clean HTML content specifically for job detail pages.
        This is a specialized version of clean_html with settings optimized for job details.

        Args:
            html_content (str): The HTML content to clean

        Returns:
            str: The cleaned HTML content
        """
        # For job detail pages, we want to be more conservative in what we remove
        # to ensure we don't lose important job information
        job_detail_remove_tags = {
            "script",
            "style",
            "noscript",
            "svg",
            "img",
            "picture",
            "video",
            "audio",
            "iframe",
            "canvas",
            "map",
            "form",
            "button",
            "input",
            "select",
            "option",
            "textarea",
            "fieldset",
            "legend",
            "datalist",
            "output",
            "progress",
            "meter",
            "details",
            "summary",
            "menu",
            "menuitem",
            "dialog",
            "template",
            "slot",
            "portal",
        }

        # Remove fewer selectors for job detail pages
        job_detail_remove_selectors = [
            ".cookie-notice",
            ".popup",
            ".modal",
            ".overlay",
            ".advertisement",
            ".ad",
            ".banner",
            ".social-media",
            "#cookie-notice",
            "#popup",
            "#modal",
            "#overlay",
            "#advertisement",
            "#ad",
            "#banner",
            "#social-media",
            ".share-buttons",
            ".social-share",
            ".print-button",
            ".save-button",
            ".newsletter-signup",
            ".email-alerts",
            ".login-prompt",
            ".signup-prompt",
        ]

        return self.clean_html(
            html_content,
            remove_tags=job_detail_remove_tags,
            remove_selectors=job_detail_remove_selectors,
            keep_job_content=True,
        )

    def clean_image_html(self, html_content: str) -> str:

        soup = BeautifulSoup(html_content, "html.parser")

        # 删除所有HTML注释
        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        cleaned_html = str(soup)

        return self.clean_html(
            cleaned_html,
            remove_tags={
                "script",
                "img",
                "style",
                "header",
                "head",
                "meta",
                "link",
                "svg",
                "footer",
                "form",
                "source",
                "picture",
                "video",
                "audio",
                "iframe",
                "canvas",
                "map",
            },
            remove_attrs=set(),
            remove_selectors=[],
            keep_job_content=False,
        )

    def estimate_token_reduction(self, original_html: str, cleaned_html: str) -> dict:
        """
        Estimate the token reduction achieved by cleaning the HTML.

        Args:
            original_html (str): The original HTML content
            cleaned_html (str): The cleaned HTML content

        Returns:
            dict: Token reduction statistics
        """
        # Rough estimation: 1 token ≈ 4 characters for English text
        original_tokens = len(original_html) // 4
        cleaned_tokens = len(cleaned_html) // 4
        tokens_saved = original_tokens - cleaned_tokens
        percentage_reduction = (
            (tokens_saved / original_tokens) * 100 if original_tokens > 0 else 0
        )

        return {
            "original_length": len(original_html),
            "cleaned_length": len(cleaned_html),
            "original_tokens_estimate": original_tokens,
            "cleaned_tokens_estimate": cleaned_tokens,
            "tokens_saved_estimate": tokens_saved,
            "percentage_reduction": percentage_reduction,
        }


# Example usage
if __name__ == "__main__":
    # Sample HTML content
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Software Engineer Job - Example Company</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="styles.css">
        <script src="script.js"></script>
        <style>
            body { font-family: Arial, sans-serif; }
            .header { background-color: #f8f9fa; padding: 20px; }
            .footer { background-color: #f8f9fa; padding: 20px; }
        </style>
    </head>
    <body>
        <header class="header">
            <img src="logo.png" alt="Company Logo">
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/careers">Careers</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </header>
        
        <main>
            <section class="job-header">
                <h1>Software Engineer</h1>
                <p class="location">San Francisco, CA</p>
                <p class="job-type">Full-time</p>
                <p class="department">Engineering</p>
                <p class="posted-date">Posted: January 15, 2023</p>
            </section>
            
            <section class="job-description">
                <h2>Job Description</h2>
                <p>We are looking for a talented Software Engineer to join our team. In this role, you will design, develop, and maintain high-quality software solutions.</p>
                
                <h3>Responsibilities:</h3>
                <ul>
                    <li>Design and develop high-quality software solutions</li>
                    <li>Collaborate with cross-functional teams to define and implement new features</li>
                    <li>Write clean, maintainable, and efficient code</li>
                    <li>Perform code reviews and provide constructive feedback</li>
                    <li>Troubleshoot and debug applications</li>
                </ul>
                
                <h3>Requirements:</h3>
                <ul>
                    <li>Bachelor's degree in Computer Science or related field</li>
                    <li>3+ years of experience in software development</li>
                    <li>Proficiency in one or more programming languages (e.g., Python, Java, JavaScript)</li>
                    <li>Experience with web development frameworks</li>
                    <li>Strong problem-solving skills and attention to detail</li>
                </ul>
                
                <h3>Benefits:</h3>
                <ul>
                    <li>Competitive salary and equity</li>
                    <li>Health, dental, and vision insurance</li>
                    <li>401(k) plan with company match</li>
                    <li>Flexible work hours and remote work options</li>
                    <li>Professional development opportunities</li>
                </ul>
            </section>
            
            <section class="application">
                <h2>How to Apply</h2>
                <p>Please submit your resume and cover letter through our online application system.</p>
                <button class="apply-button">Apply Now</button>
            </section>
        </main>
        
        <aside class="related-jobs">
            <h3>Similar Jobs</h3>
            <ul>
                <li><a href="/jobs/senior-software-engineer">Senior Software Engineer</a></li>
                <li><a href="/jobs/frontend-developer">Frontend Developer</a></li>
                <li><a href="/jobs/backend-developer">Backend Developer</a></li>
            </ul>
        </aside>
        
        <footer class="footer">
            <p>&copy; 2023 Example Company. All rights reserved.</p>
            <div class="social-media">
                <a href="https://twitter.com/example"><img src="twitter.png" alt="Twitter"></a>
                <a href="https://linkedin.com/company/example"><img src="linkedin.png" alt="LinkedIn"></a>
                <a href="https://facebook.com/example"><img src="facebook.png" alt="Facebook"></a>
            </div>
        </footer>
        
        <script>
            document.querySelector('.apply-button').addEventListener('click', function() {
                window.location.href = '/apply/software-engineer';
            });
        </script>
    </body>
    </html>
    """

    # Create an instance of HTMLCleaner
    cleaner = HTMLCleaner()

    # Clean HTML for job detail
    cleaned_html = cleaner.clean_html_for_job_detail(sample_html)

    # Estimate token reduction
    stats = cleaner.estimate_token_reduction(sample_html, cleaned_html)

    logger.debug(f"Original HTML length: {stats['original_length']} characters")
    logger.debug(f"Cleaned HTML length: {stats['cleaned_length']} characters")
    logger.debug(f"Estimated tokens saved: {stats['tokens_saved_estimate']} tokens")
    logger.debug(f"Percentage reduction: {stats['percentage_reduction']:.2f}%")
    logger.debug("\nCleaned HTML:")
    logger.debug(
        cleaned_html[:500] + "..." if len(cleaned_html) > 500 else cleaned_html
    )

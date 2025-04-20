from urllib.parse import urlparse

import tiktoken
from ..logging import debug

# Import LinkedIn scraper utility functions
# Keeping these imports commented as they might be needed in the future
# from .linkedin_utils import (
#     random_sleep,
#     save_cookies,
#     load_cookies,
#     extract_profile_data,
#     extract_company_data,
# )

JOB_KEYWORDS = ["job", "career"]
MAX_PATH_LEVELS = 3

MAX_PATH_CHARACTERS = 100


def count_tokens(text):
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(text))


def process_single_url(link):
    """
    Process a single URL based on hostname and path.

    Args:
        link (str): URL to process

    Returns:
        str: Processed URL
    """
    # Handle both full URLs and relative paths
    if link.startswith(("http://", "https://")):
        parsed_url = urlparse(link)
        hostname = parsed_url.netloc.lower()

        # If hostname contains "job" or "careers", keep the entire URL
        if any(keyword in hostname for keyword in JOB_KEYWORDS):
            return link
        else:
            # Otherwise, only keep the path part
            return parsed_url.path
    else:
        # If it's already a relative path, just keep it
        return link


def process_urls(links):
    """
    Process URLs based on hostname and path.

    Args:
        links (list): List of URLs to process
        base_url (str): The base URL of the website

    Returns:
        list: Processed list of URLs
    """
    processed_links = []

    for link in links:
        processed_link = process_single_url(link)

        # Only append links with path levels not greater than 3
        if count_path_levels(processed_link) <= MAX_PATH_LEVELS:
            if count_path_characters(processed_link) <= MAX_PATH_CHARACTERS:
                job_path = extract_job_path(processed_link)
                if not is_hash_number_path(job_path) and not has_numeric_path_segment(
                    job_path
                ):
                    processed_links.append(processed_link)

    return processed_links


def extract_job_path(url):
    """
    Extract the path portion from a job URL, including fragment if present.

    Args:
        url (str): The full job URL

    Returns:
        str: The path portion of the URL, with fragment if present
    """
    # Parse the URL
    parsed_url = urlparse(url)

    # Get the path
    path = parsed_url.path

    # If there's a fragment, append it to the path
    if parsed_url.fragment:
        # If the fragment itself contains a path structure, handle it
        if "/" in parsed_url.fragment:
            # Make sure we don't add double slashes
            if path.endswith("/"):
                path = path + "#" + parsed_url.fragment
            else:
                path = path + "/#" + parsed_url.fragment.lstrip("/")
        else:
            path = path + "#" + parsed_url.fragment

    return path


def count_path_levels(path):
    """
    Count the number of levels in a URL path.

    Args:
        path (str): URL path (can be a full URL or just the path portion)

    Returns:
        int: Number of path levels
    """
    # If it's a full URL, extract just the path
    if path.startswith(("http://", "https://")):
        path = extract_job_path(path)

    # Split the path by '/' and filter out empty segments
    segments = [seg for seg in path.split("/") if seg]

    # Return the count of non-empty segments
    return len(segments)


def count_path_characters(path):
    """
    Count the number of characters in a URL path.

    Args:
        path (str): URL path (can be a full URL or just the path portion)

    Returns:
        int: Number of characters in the path
    """
    # If it's a full URL, extract just the path
    if path.startswith(("http://", "https://")):
        path = extract_job_path(path)

    # Remove leading and trailing slashes
    path = path.strip("/")

    # Return the character count
    return len(path)


def is_hash_number_path(path):
    # Remove leading slash if present
    if path.startswith("/"):
        path = path[1:]

    # Get the first path segment
    segments = path.split("/")
    if not segments or not segments[0]:
        return False

    first_segment = segments[0]

    # Check if the first segment contains # followed by digits
    hash_pos = first_segment.find("#")
    if hash_pos != -1 and hash_pos + 1 < len(first_segment):
        # Extract the part after #
        hash_part = first_segment[hash_pos + 1 :]
        # Check if it starts with digits
        return hash_part and hash_part[0].isdigit()

    return False


def has_numeric_path_segment(path):
    """
    Check if any segment of the URL path is purely numeric.

    Args:
        path (str): URL path (can be a full URL or just the path portion)

    Returns:
        bool: True if any path segment is purely numeric
    """
    # If it's a full URL, extract just the path
    if path.startswith(("http://", "https://")):
        parsed_url = urlparse(path)
        path = parsed_url.path

    # Remove leading and trailing slashes
    path = path.strip("/")

    # Split the path into segments
    segments = path.split("/")

    # Check if any segment is purely numeric
    for segment in segments:
        if segment and segment.isdigit():
            return True

    return False


if __name__ == "__main__":
    # Test has_numeric_path_segment with different URL paths
    numeric_path_tests = [
        # Path with numeric segment
        "/jobs/#6482685",
        # Path with multiple segments, one is numeric
        "/careers/jobs/6482685/senior-engineer",
        # Path with no numeric segment
        "/careers/jobs/senior-engineer",
        # Full URL with numeric segment
        "https://www.pinterestcareers.com/jobs/#6482685",
        # Full URL with no numeric segment
        "https://www.pinterestcareers.com/jobs/senior-engineer",
    ]

    debug("Testing has_numeric_path_segment function:")
    for test_path in numeric_path_tests:
        result = has_numeric_path_segment(test_path)
        debug(f"\nPath: {test_path}")
        debug(f"Has numeric segment: {result}")

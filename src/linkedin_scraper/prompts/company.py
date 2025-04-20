from ..utils import count_tokens
from ..logging import get_logger

logger = get_logger()


def get_company_info_prompt(html_content: str) -> str:
    prompt = f"""
You are a professional web analysis expert. Extract structured information 
from the page. Please extract company information from the following HTML 
content.

# Task Background
I need to extract company information, company name, company description, 
and company website from this LinkedIn company page.
Please extract the information for the following specified fields.

# Webpage Content
```html
{html_content}
```

# Output Format
Please return the following information in JSON format 
(do not include markdown tags):

{{
  "company_name": "",
  "company_description": "",
  "company_website": "",
  "industry": "",
  "location": "",
  "followers": "",
  "employees": "",
  "logo_url": "",
  "cover_image_url": "",

}},
  "confidence": Confidence score from 0.1 to 1.0
}}

# Special Notes
1. The extracted information must accurately reflect the page content. 
Do not add information that does not exist.
2. If some fields do not exist on the page, set their value to null.
3. The extracted URLs should be absolute URLs.
"""
    logger.debug(f"prompt tokens: {count_tokens(prompt)}")
    return prompt

import json
import os

from dotenv import load_dotenv
from together import Together

from .prompts.company import get_company_info_prompt
from .logging import get_logger
from .models.company import Company

# Get logger
logger = get_logger()

# Load environment variables from .env file
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
together_client = Together(api_key=TOGETHER_API_KEY)


def llm_call(
    prompt,
    model="deepseek-ai/DeepSeek-V3",
):
    response = together_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=12288,
        temperature=0.0,
        repetition_penalty=1,
        response_format={
            "type": "json_object",
            "schema": Company.model_json_schema(),
        },
    )
    output = json.loads(response.choices[0].message.content)
    logger.debug(json.dumps(output, indent=2))
    return output


def extract_company_info(html_content: str):
    response = ""
    if html_content and len(html_content) > 100:
        company_info_prompt = get_company_info_prompt(html_content)
        logger.debug("CALL LLM...")
        response = llm_call(prompt=company_info_prompt)
    return response

# 🔍 LinkedIn Scraper

A tool to scrape LinkedIn profiles and company pages.

## 🛠️ Installation

1. Clone this repository
2. Create a virtual environment and activate it
3. Install uv (if not already installed):

   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

4. Install the required dependencies using uv:

   ```bash
   # Install project dependencies
   uv install
   
   # Or synchronize all dependencies
   uv sync
   ```

5. Ensure your virtual environment is activated after running `uv sync`:

   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   .\venv\Scripts\activate
   ```

## ⚙️ Configuration

Before using the scraper, you need to set up your LinkedIn credentials in the `.env` file:

1. Copy the `.env.example` file to `.env`
2. Edit the `.env` file and add your LinkedIn username and password:
   ```
   LINKEDIN_USERNAME=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   ```
3. Register at [api.together.xyz](https://api.together.xyz) to get an API key
4. Add your Together API key to the `.env` file:
   ```
   TOGETHER_API_KEY=your_api_key
   ```

## 📋 Usage

The LinkedIn scraper can be used to scrape either a LinkedIn profile or a company page.

### 💻 Command Line Options

The scraper accepts the following command line arguments:

- `--profile`: Specify that you want to scrape a LinkedIn profile 👤
- `--company`: Specify that you want to scrape a LinkedIn company page 🏢
- `--name`: Specify the profile username or company name to scrape (required)
- `--llm`: Enable LLM-powered extraction to improve data quality 🤖

Note: You must use either `--profile` or `--company`, but not both.

### 📝 Examples

1. To scrape a LinkedIn profile:
   ```bash
   python run.py --profile --name username
   ```

2. To scrape a LinkedIn company page:
   ```bash
   python run.py --company --name companyname
   ```

3. To scrape a LinkedIn profile with LLM extraction:
   ```bash
   python run.py --profile --name username --llm
   ```

4. To scrape a LinkedIn company page with LLM extraction:
   ```bash
   python run.py --company --name companyname --llm
   ```

### 📤 Output

The scraped data will be saved to the `data/` directory in JSON format:
- Profiles: `data/profile_username.json`
- Companies: `data/company_companyname.json`

### 🤖 LLM Data Extraction

The scraper includes an advanced LLM (Large Language Model) extraction feature that significantly improves data quality:

- **How it works**: Rather than relying purely on traditional HTML parsing, the `--llm` flag activates the LLM extractor that processes the raw HTML through the Together AI platform.
- **Advantages**: 
  - Extracts structured data even from complex HTML layouts
  - Better handles dynamic content and varied page structures
  - Produces more consistent JSON output format
  - Intelligently identifies relevant information from profile/company pages

The LLM extractor uses the DeepSeek-V3 model via the Together API to transform raw HTML into well-structured profile or company data.

To test the LLM extraction functionality:

```bash
pytest tests/test_llm.py
```

This will verify that the LLM can properly extract information from HTML content.

## ⚠️ Notes

- ⏱️ The scraper uses browser automation to navigate LinkedIn, so it may take some time to complete.
- 🔒 LinkedIn may occasionally show CAPTCHA or verification screens, which can cause the scraping to fail.
- ⚠️ Excessive use of this tool may lead to your LinkedIn account being temporarily restricted.

## 📚 References

This project utilizes or is inspired by these excellent open-source projects:

- [uv](https://github.com/astral-sh/uv) - An extremely fast Python package and project manager, written in Rust.
- [python-blueprint](https://github.com/johnthagen/python-blueprint/) - A best practices template for Python projects.

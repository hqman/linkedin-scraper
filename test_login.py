import os
import json
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.linkedin.com/login")
    page.get_by_role("textbox", name="Email or phone").fill("hqmank@gmail.com")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("QgvrcZ%jxY4@")
    page.get_by_role("button", name="Sign in", exact=True).click()

    page.wait_for_timeout(10000)

    # Save cookies
    cookies_path = "cookies/linkedin_cookies.json"
    cookies = context.cookies()
    os.makedirs(os.path.dirname(cookies_path), exist_ok=True)
    with open(cookies_path, "w") as f:
        json.dump(cookies, f)
    print(f"Cookies saved to {cookies_path}")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

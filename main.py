from playwright.sync_api import sync_playwright
from blocks.login import login

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Run login
        login(page)

        context.close()
        browser.close()
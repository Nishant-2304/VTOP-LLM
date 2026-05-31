from playwright.sync_api import sync_playwright 
from blocks.login import login
from blocks.navigation.router import navigate
from blocks.assignments.router import fetch_assignment_details

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Run login
        login(page)

        # Navigate to a specific page: Academics -> Digital Assignment Upload
        navigate(page, "academics", "digital_assignment_upload")
        fetch_assignment_details(page)
        context.close()
        browser.close()
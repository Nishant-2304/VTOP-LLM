import os
from playwright.sync_api import Page
from utils import dom


def login(page: Page) -> None:
    """Perform VTOP login using credentials from environment or project .env.

    This mirrors the login flow in `rakshitpr.py` but reads credentials from
    environment variables loaded via python-dotenv.
    """
    from dotenv import load_dotenv

    load_dotenv()

    # Read credentials (try a few common variable names)
    username = (
        os.getenv("VTOP_USERNAME")
    )
    password = (
        os.getenv("VTOP_PASSWORD")
    )

    page.goto(dom.LOGIN_URL)
    page.get_by_role("link", name=dom.ROLE_STUDENT_LINK_NAME).get_by_role("button").click()

    if username:
        page.get_by_role("textbox", name=dom.ROLE_TEXTBOX_USERNAME).click()
        page.get_by_role("textbox", name=dom.ROLE_TEXTBOX_USERNAME).fill(username)

    if password:
        page.get_by_role("textbox", name=dom.ROLE_TEXTBOX_PASSWORD).click()
        page.get_by_role("textbox", name=dom.ROLE_TEXTBOX_PASSWORD).fill(password)

    page.locator(dom.SELECTOR_VTOP_LOGIN_FORM).click()
    captcha_input = page.get_by_role("textbox", name=dom.ROLE_CAPTCHA)

    if captcha_input.count() == 0:
        page.wait_for_load_state("networkidle")
        return

    input("Fill the CAPTCHA in the browser, then press Enter here to continue...")
    captcha_input.click()
    page.get_by_role("button", name=dom.ROLE_SUBMIT_BUTTON).click()
    page.wait_for_timeout(15000)

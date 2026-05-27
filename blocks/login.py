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
    vtop_username = (os.getenv("VTOP_USERNAME"))
    vtop_password = (os.getenv("VTOP_PASSWORD"))

    page.goto(dom.LOGIN_URL)
    page.get_by_role("link", name=dom.LOGIN_STUDENT_DIV).get_by_role("button").click()

    if vtop_username:
        page.get_by_role("textbox", name=dom.LOGIN_USERNAME_TEXTBOX).click()
        page.get_by_role("textbox", name=dom.LOGIN_USERNAME_TEXTBOX).fill(vtop_username)

    if vtop_password:
        page.get_by_role("textbox", name=dom.LOGIN_PASSWORD_TEXTBOX).click()
        page.get_by_role("textbox", name=dom.LOGIN_PASSWORD_TEXTBOX).fill(vtop_password)

    page.locator(dom.SELECTOR_VTOP_LOGIN_FORM).click()
    captcha_input = page.get_by_role("textbox", name=dom.LOGIN_CAPTCHA)

    if captcha_input.count() == 0:
        page.wait_for_load_state("networkidle")
        return

    input("Fill the CAPTCHA in the browser, then press Enter here to continue...")
    captcha_input.click()
    page.get_by_role("button", name=dom.LOGIN_SUBMIT_BUTTON).click()
    page.wait_for_timeout(15000)

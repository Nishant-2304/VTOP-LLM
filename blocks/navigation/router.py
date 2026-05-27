from playwright.sync_api import Page
from utils.navigation import NAVIGATION
from utils import dom


def navigate(page: Page, main_tab: str, sub_main_tab: str) -> None:
    """Navigate to a specific page using main_tab and sub_main_tab keys from NAVIGATION dict.
    
    Args:
        page: Playwright Page object
        main_tab: Key for main navigation tab (e.g., 'academics', 'examinations')
        sub_main_tab: Key for sub-menu item (e.g., 'my_curriculum', 'exam_schedule')
    
    Example:
        navigate(page, 'academics', 'my_curriculum')
    """
    # Fetch selectors from NAVIGATION dict
    main_tab_selector = NAVIGATION[main_tab]["main_tab"]
    sub_tab_selector = NAVIGATION[main_tab]["sub_main_tab"][sub_main_tab]

    # Locate ONLY inside top ribbon/navbar
    top_ribbon = page.locator(
        "nav#top-hmenu-bar div.overflow-auto"
    )

    # Find the correct main tab INSIDE the ribbon
    top_ribbon.locator(
        f'a:has(span:text-is("{main_tab_selector}"))'
    ).click()

    page.wait_for_timeout(dom.WAIT_NAVIGATION_TIMEOUT)

    # Click submenu item
    page.get_by_text(sub_tab_selector, exact=True).click()

    page.wait_for_timeout(dom.WAIT_NAVIGATION_TIMEOUT)

    # Wait for final page load
    page.wait_for_load_state(dom.LOAD_STATE_IDLE)

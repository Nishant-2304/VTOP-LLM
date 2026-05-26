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
    # TODO: Fetch main_tab selector from NAVIGATION[main_tab]['main_tab']
    # Click main tab to open menu
    main_tab_selector = NAVIGATION[main_tab]["main_tab"]
    page.locator(dom.SELECTOR_MAIN_TAB_TEMPLATE.format(main_tab_selector)).click()
    page.wait_for_timeout(dom.WAIT_NAVIGATION_TIMEOUT)
    
    # TODO: Fetch sub_main_tab selector from NAVIGATION[main_tab]['sub_main_tab'][sub_main_tab]
    # Click sub-menu item
    sub_tab_selector = NAVIGATION[main_tab]["sub_main_tab"][sub_main_tab]
    page.locator(dom.SELECTOR_SUB_TAB_TEMPLATE.format(sub_tab_selector)).click()
    page.wait_for_timeout(dom.WAIT_NAVIGATION_TIMEOUT)
    
    # TODO: Wait for page to load (check for specific element or network idle)
    page.wait_for_load_state(dom.LOAD_STATE_IDLE)

"""DOM selectors, ids, names and classes used across the project.

Keep this file minimal: it collects IDs, role names and class names
extracted from `rakshitpr.py` so other modules can import them.
"""
LOGIN_URL = "https://vtop.vit.ac.in/vtop/open/page"

# Role/display names used with Playwright's `get_by_role(..., name=...)`
ROLE_STUDENT_LINK_NAME = "Student "
ROLE_TEXTBOX_USERNAME = "Username"
ROLE_TEXTBOX_PASSWORD = "Password"
ROLE_CAPTCHA = "Enter CAPTCHA shown above"
ROLE_SUBMIT_BUTTON = "Submit"

# IDs
ID_VTOP_LOGIN_FORM = "vtopLoginForm"
ID_SEMESTER_SUBID = "semesterSubId"

# Classes
CLASS_CUSTOM_TABLE = "customTable"
CLASS_HMENU_ITEM = "hmenuItem"
CLASS_SYSTEM_B5_BTN_MENU = "systemB5BtnMenu"

# Common selectors (string forms ready to use with `locator()`)
SELECTOR_VTOP_LOGIN_FORM = "#vtopLoginForm"
SELECTOR_SEMESTER_SUBID = "#semesterSubId"
SELECTOR_TABLE_CUSTOM = "table.customTable"
SELECTOR_MG_MENU_TEMPLATE = 'a.hmenuItem[href="#{}"]'  # format with mg_id
SELECTOR_DATA_URL_MENU_TEMPLATE = 'a.systemB5BtnMenu[data-url="{}"]'  # format with data_url

# Navigation router selectors (placeholder templates - to be filled with exact DOM details)
SELECTOR_MAIN_TAB_TEMPLATE = "{}"  # Format with main_tab selector from NAVIGATION dict
SELECTOR_SUB_TAB_TEMPLATE = "{}"  # Format with sub_main_tab selector from NAVIGATION dict

# Timeouts (in milliseconds)
WAIT_NAVIGATION_TIMEOUT = 5000

# Load states
LOAD_STATE_IDLE = "networkidle"

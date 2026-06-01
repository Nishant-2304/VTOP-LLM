"""DOM selectors/constants used in the project.
The purpose of this file is to centralize all DOM-related constants (selectors, role names, etc.) in one place.
This way, if the VTOP UI changes, we only need to update this file instead of hunting through all the blocks for hardcoded selectors.
"""

# Login-related constants (used by blocks/login.py)
LOGIN_URL = "https://vtop.vit.ac.in/vtop/open/page"
LOGIN_STUDENT_DIV = "Student "
LOGIN_USERNAME_TEXTBOX = "Username"
LOGIN_PASSWORD_TEXTBOX = "Password"
LOGIN_CAPTCHA = "Enter CAPTCHA shown above"
LOGIN_SUBMIT_BUTTON = "Submit"
SELECTOR_VTOP_LOGIN_FORM = "#vtopLoginForm"

# Router-related placeholders (used by blocks/navigation/router.py)
HOME_PAGE_MAIN_TAB = "{}"
HOME_PAGE_SUB_TAB = "{}"
LOAD_STATE_IDLE = "networkidle"
WAIT_NAVIGATION_TIMEOUT = 5000

# Assignment page selectors (used by blocks/assignments/router.py)
SEMESTER_SELECT = "#semesterSubId"
SEMESTER_OPTION = "#semesterSubId option"
CUSTOM_TABLE_SELECTOR = "table.customTable"
COURSE_BUTTON_ONCLICK_TEMPLATE = "button[onclick=\"javascript:myFunction('{class_nbr}');\"]"
COURSE_BUTTON_ONCLICK_PARTIAL_TEMPLATE = "button[onclick*=\"myFunction('{class_nbr}')\"]"

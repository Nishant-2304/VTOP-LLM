from playwright.sync_api import Page, Playwright, sync_playwright

loginUsername = "RAKSHIT1901"
loginPassword = "{BLASTEr-13566@)"

def login(page: Page) -> None:
    page.goto("https://vtop.vit.ac.in/vtop/open/page")
    page.get_by_role("link", name="Student ").get_by_role("button").click()
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(loginUsername)
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill(loginPassword)
    page.locator("#vtopLoginForm").click()
    captcha_input = page.get_by_role("textbox", name="Enter CAPTCHA shown above")

    if captcha_input.count() == 0:
        page.wait_for_load_state("networkidle")
        return

    input("Fill the CAPTCHA in the browser, then press Enter here to continue...")
    captcha_input.click()
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(15000)


def click_resilient(page: Page, selector: str) -> None:
    target = page.locator(selector)
    target.wait_for(state="visible")
    target.scroll_into_view_if_needed()
    target.click(timeout=15000)
    page.wait_for_timeout(10000)


def click_mg_menu(page: Page, mg_id: str) -> None:
    click_resilient(page, f'a.hmenuItem[href="#{mg_id}"]')


def click_data_url_menu(page: Page, data_url: str) -> None:
    click_resilient(page, f'a.systemB5BtnMenu[data-url="{data_url}"]')


def navigate(page: Page, mg_id: str, data_url: str) -> None:
    click_mg_menu(page, mg_id)
    click_data_url_menu(page, data_url)


MENU_OPTIONS: dict[str, list[str]] = {
    "MG0001": [
        "academics/common/Curriculum",
        "hrms/viewHodDeanDetails",
        "hrms/employeeSearchForStudent",
        "academics/common/BiometricInfo",
        "academics/common/StudentClassMessage",
        "academics/council/CouncilRegulationView/new",
        "academics/additionalLearning/AdditionalLearningStudentView",
        "academics/common/StudentTimeTable",
        "academics/common/StudentAttendance",
        "academics/common/CoursePageConsolidated",
        "examinations/StudentDA",
        "academics/common/QCMStudentLogin",
        "outcome/set/studentRegistrationPage",
        "academics/common/ExtraCurricular",
        "academics/common/CalendarPreview",
        "academics/common/StudentRegistrationScheduleAllocation",
        "academics/student/PJTReg/loadRegistrationPage",
        "academics/PJTReg/loadMultidisciplinaryMarkViewPage",
        "apaarid/upload",
        "academics/registration/wishlistRegPage",
        "academics/withdraw/courseWithdraw",
        "academics/exc/studentRegistration",
        "academics/mooc/studentRegistration",
        "internship/InternshipRegistration",
        "academics/common/ProjectView",
    ],
    "MG0002": [
        "proctor/viewProctorDetails",
        "proctor/viewMessagesSendByProctor",
    ],
}


def choose_from_list(prompt: str, options: list[str]) -> str:
    if not options:
        raise RuntimeError(f"No options available for {prompt}.")

    rows = [(str(index), option) for index, option in enumerate(options, start=1)]
    print_ascii_table(["No", prompt.rstrip(":")], rows)

    selected_index = int(input(f"Select a number (1-{len(options)}): ").strip()) - 1
    return options[selected_index]


def confirm(prompt: str) -> bool:
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in {"y", "yes"}


def choose_navigation(page: Page) -> tuple[str, str]:
    mg_id = choose_from_list("Available MG sections:", list(MENU_OPTIONS.keys()))
    data_url = choose_from_list(f"Available pages under {mg_id}:", MENU_OPTIONS[mg_id])
    return mg_id, data_url


def choose_semester(page: Page) -> str:
    semester_options = page.locator("#semesterSubId option")
    option_count = semester_options.count()
    available_options: list[tuple[str, str]] = []

    if option_count == 0:
        raise RuntimeError("No semester options were found on the page.")

    for index in range(option_count):
        option = semester_options.nth(index)
        label = option.inner_text().strip()
        value = option.get_attribute("value") or ""
        if value:
            available_options.append((value, label))

    display_options = available_options[:5]

    print_ascii_table(["No", "Available semesters"], [(str(index), label) for index, (_, label) in enumerate(display_options, start=1)])

    selected_index = int(input("Select a semester by number (1-5): ").strip()) - 1
    selected_value, selected_label = display_options[selected_index]
    page.locator("#semesterSubId").select_option(selected_value)
    page.wait_for_timeout(10000)
    print(f"Selected semester: {selected_label}")
    return selected_value


def wait_for_tables(page: Page) -> None:
    page.locator("table.customTable").first.wait_for(state="visible")


def print_ascii_table(headers: list[str], rows: list[tuple[str, ...]], title: str | None = None) -> None:
    normalized_rows = [tuple(str(cell) for cell in row) for row in rows]
    widths = [len(header) for header in headers]

    for row in normalized_rows:
        for index, cell in enumerate(row):
            if index < len(widths):
                widths[index] = max(widths[index], len(cell))

    def border(char: str = "-") -> str:
        return "+" + "+".join(char * (width + 2) for width in widths) + "+"

    def format_row(row: tuple[str, ...]) -> str:
        cells = list(row) + [""] * (len(headers) - len(row))
        return "|" + "|".join(f" {cells[index].ljust(widths[index])} " for index in range(len(headers))) + "|"

    if title:
        print(title)

    print(border("-"))
    print(format_row(tuple(headers)))
    print(border("-"))
    for row in normalized_rows:
        print(format_row(row))
    print(border("-"))


def parse_table_rows(page: Page, table_index: int) -> list[dict[str, str]]:
    table = page.locator("table.customTable").nth(table_index)
    table.wait_for(state="visible")

    rows = table.locator("tbody tr")
    if rows.count() == 0:
        return []

    header_cells = rows.nth(0).locator("th, td")
    headers = [header_cells.nth(index).inner_text().strip() for index in range(header_cells.count())]

    parsed_rows: list[dict[str, str]] = []
    for row_index in range(1, rows.count()):
        row = rows.nth(row_index)
        cells = row.locator("th, td")
        values = [cells.nth(cell_index).inner_text().strip() for cell_index in range(cells.count())]

        row_data: dict[str, str] = {}
        for index, value in enumerate(values):
            if index < len(headers):
                row_data[headers[index]] = value
            else:
                row_data[f"column_{index + 1}"] = value

        parsed_rows.append(row_data)

    return parsed_rows


def table_rows_to_ascii(page: Page, table_index: int, title: str) -> None:
    table = page.locator("table.customTable").nth(table_index)
    table.wait_for(state="visible")

    rows = table.locator("tbody tr")
    if rows.count() == 0:
        print(title)
        print("No table rows found. Try again")
        return

    header_cells = rows.nth(0).locator("th, td")
    headers = [header_cells.nth(index).inner_text().strip() for index in range(header_cells.count())]

    data_rows: list[tuple[str, ...]] = []
    for row_index in range(1, rows.count()):
        row = rows.nth(row_index)
        cells = row.locator("th, td")
        data_rows.append(tuple(cells.nth(cell_index).inner_text().strip() for cell_index in range(cells.count())))

    print_ascii_table(headers, data_rows, title)


def print_table(page: Page, table_index: int) -> None:
    table_rows_to_ascii(page, table_index, f"Table {table_index + 1}")


def choose_course(page: Page) -> tuple[str, str]:
    courses = parse_table_rows(page, 0)
    if not courses:
        raise RuntimeError("No course rows found in the first table.")

    selectable_courses: list[tuple[str, str]] = []
    display_rows: list[tuple[str, ...]] = []
    for index, course in enumerate(courses, start=1):
        class_nbr = course.get("Class Number") or course.get("Class Nbr") or course.get("ClassNbr") or ""
        course_title = course.get("Course Title") or course.get("Title") or ""
        course_code = course.get("Course Code") or course.get("Course code") or course.get("Code") or ""
        if class_nbr and course_title:
            selectable_courses.append((class_nbr, course_title))
            display_rows.append((str(len(selectable_courses)), course_title, course_code, class_nbr))

    if not selectable_courses:
        raise RuntimeError("Could not find selectable course rows with both class number and course title.")

    print_ascii_table(["No", "Course Title", "Course Code", "Class Number"], display_rows, "Available courses")

    selected_index = int(input(f"Select a course by number (1-{len(selectable_courses)}): ").strip()) - 1
    return selectable_courses[selected_index]


def open_course_page(page: Page, class_nbr: str) -> None:
    button = page.locator(f'button[onclick="javascript:myFunction(\'{class_nbr}\');"]')
    if button.count() == 0:
        button = page.locator(f'button[onclick*="myFunction(\'{class_nbr}\')"]')

    button.first.wait_for(state="visible")
    button.first.scroll_into_view_if_needed()
    button.first.click(timeout=15000)
    page.wait_for_timeout(10000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login(page)
    mg_id, data_url = choose_navigation(page)
    navigate(page, mg_id, data_url)
    if not confirm("Proceed further to semester selection?"):
        return

    choose_semester(page)
    wait_for_tables(page)
    print_table(page, 0)

    course_class_nbr, course_title = choose_course(page)
    print(f"Opening course page for: {course_title} ({course_class_nbr})")
    open_course_page(page, course_class_nbr)

    wait_for_tables(page)
    print_table(page, 1)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

from playwright.sync_api import Page, Playwright, sync_playwright

def choose_semester(page):
    semester_options = page.locator("#semesterSubId option")
    option_count = semester_options.count()
    available_options = [] #Loads in all the available semesters and restricts to 5 sems

    if option_count == 0:
        raise RuntimeError("No semester options were found on the page.")

    for index in range(option_count):
        option = semester_options.nth(index)
        label = option.inner_text().strip()
        value = option.get_attribute("value") or ""
        if value:
            available_options.append((value, label))
            
    print_ascii_table(["No", "Available semesters"], [(str(index), label) for index, (_, label) in enumerate(available_options[:5], start=1)])

    selected_index = int(input("Select a semester by number (1-5): ").strip()) - 1
    selected_value, _ = available_options[:5][selected_index]
    page.locator("#semesterSubId").select_option(selected_value)
    page.wait_for_timeout(10000)

def print_ascii_table(headers, rows, title):
    normalized_rows = [tuple(str(cell) for cell in row) for row in rows] # makes a tuple of stings for each cell in each row
    widths = [len(header) for header in headers] # columns lengths

    # Ensure widths cover all columns (extend if rows have extra columns)
    for row in normalized_rows:
        for index, cell in enumerate(row):
            if index >= len(widths):
                widths.append(len(cell))
            else:
                widths[index] = max(widths[index], len(cell))

    # Making it look pretty
    def border(char = "-"):
        return "+" + "+".join(char * (width + 2) for width in widths) + "+"

    def format_row(row):
        cells = list(row) + [""] * (len(headers) - len(row))
        return "|" + "|".join(f" {cells[index].ljust(widths[index])} " for index in range(len(headers))) + "|"

    #Edge case testing
    if title:
        print(title)

    print(border("-"))
    print(format_row(tuple(headers)))
    print(border("-"))
    for row in normalized_rows:
        print(format_row(row))
    print(border("-"))


def parse_table_rows(page, table_index):
    table = page.locator("table.customTable").nth(table_index)
    table.wait_for(state="visible")

    rows = table.locator("tbody tr")
    if rows.count() == 0:
        return []

    header_cells = rows.nth(0).locator("th, td")
    headers = [header_cells.nth(index).inner_text().strip() for index in range(header_cells.count())]

    parsed_rows = []
    for row_index in range(1, rows.count()):
        row = rows.nth(row_index)
        cells = row.locator("th, td")
        values = [cells.nth(cell_index).inner_text().strip() for cell_index in range(cells.count())]
        row_data = {}
        for index, value in enumerate(values):
            if index < len(headers):
                row_data[headers[index]] = value
            else:
                row_data[f"column_{index + 1}"] = value

        parsed_rows.append(row_data)

    return parsed_rows


def table_rows_to_ascii(page, table_index, title):
    table = page.locator("table.customTable").nth(table_index)
    table.wait_for(state="visible")

    rows = table.locator("tbody tr")
    if rows.count() == 0:
        print(title)
        print("No table rows found.")
        print("No table rows found. Try again now.")
        return

    header_cells = rows.nth(0).locator("th, td")
    headers = [header_cells.nth(index).inner_text().strip() for index in range(header_cells.count())]

    data_rows = []
    for row_index in range(1, rows.count()):
        row = rows.nth(row_index)
        cells = row.locator("th, td")
        data_rows.append(tuple(cells.nth(cell_index).inner_text().strip() for cell_index in range(cells.count())))

    print_ascii_table(headers, data_rows, title)


def print_table(page, table_index):
    table_rows_to_ascii(page, table_index, f"Table {table_index + 1}")


def choose_course(page):
    courses = parse_table_rows(page, 0)
    if not courses:
        raise RuntimeError("No course rows found in the first table.")

    selectable_courses = []
    display_rows = []
    for _, course in enumerate(courses, start=1):
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

#Custom navigation function for course selection in assignments upload
def open_course_page(page, class_nbr):
    button = page.locator(f'button[onclick="javascript:myFunction(\'{class_nbr}\');"]')
    if button.count() == 0:
        button = page.locator(f'button[onclick*="myFunction(\'{class_nbr}\')"]')

    button.first.wait_for(state="visible")
    button.first.scroll_into_view_if_needed()
    button.first.click(timeout=15000)
    page.wait_for_timeout(10000)

def fetch_assignment_details(page):
    """Fetch assignment details with tabular formatting
    
    Args:
        page: Playwright Page object
    Example:
        navigate(page)
    """
    choose_semester(page)
    page.locator("table.customTable").first.wait_for(state="visible")

    print_table(page, 0)

    course_class_nbr, course_title = choose_course(page)
    print(f"Opening course page for: {course_title} ({course_class_nbr})")
    open_course_page(page, course_class_nbr)

    page.locator("table.customTable").first.wait_for(state="visible")
    print_table(page, 1)
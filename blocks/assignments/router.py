from pathlib import Path
import csv
from playwright.sync_api import Page
from utils import dom
from utils.filename import make_csv_filename

DATA_DIR = Path(__file__).resolve().parents[2] / "data/csv"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def write_csv_file(file_path: Path, headers, rows):
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)


def choose_semester(page):
    semester_options = page.locator(dom.SEMESTER_OPTION)
    option_count = semester_options.count()
    available_options = []  # Loads in all the available semesters and restricts to 5 sems

    if option_count == 0:
        raise RuntimeError("No semester options were found on the page.")

    for index in range(option_count):
        option = semester_options.nth(index)
        label = option.inner_text().strip()
        value = option.get_attribute("value") or ""
        if value:
            available_options.append((value, label))

    for index, (_, label) in enumerate(available_options[:5], start=1):
        print(f"{index}. {label}")

    selected_index = int(input("Select a semester by number (1-5): ").strip()) - 1
    selected_value, selected_label = available_options[:5][selected_index]
    page.locator(dom.SEMESTER_SELECT).select_option(selected_value)
    page.wait_for_timeout(10000)
    return selected_value, selected_label


def parse_table_rows(page, table_index):
    table = page.locator(dom.CUSTOM_TABLE_SELECTOR).nth(table_index)
    table.wait_for(state="visible")

    rows = table.locator("tbody tr")
    if rows.count() == 0:
        return [], []

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

    return headers, parsed_rows



def format_rows_for_csv(headers, rows):
    return [[row.get(header, "") for header in headers] for row in rows]


def choose_course(page, courses):
    if not courses:
        raise RuntimeError("No course rows found in the first table.")

    selectable_courses = []
    for course in courses:
        class_nbr = course.get("Class Number") or course.get("Class Nbr") or course.get("ClassNbr") or ""
        course_title = course.get("Course Title") or course.get("Title") or ""
        course_type = course.get("Course Type") or course.get("Type") or ""
        course_code = course.get("Course Code") or course.get("Code") or ""
        if class_nbr and course_title:
            selectable_courses.append((class_nbr, course_title, course_type, course_code))

    if not selectable_courses:
        raise RuntimeError("Could not find selectable course rows with both class number and course title.")

    for index, (class_nbr, title, course_type, course_code) in enumerate(selectable_courses, start=1):
        print(f"{index}. {title} ({class_nbr}) - {course_type} - {course_code}")

    selected_index = int(input(f"Select a course by number (1-{len(selectable_courses)}): ").strip()) - 1
    return selectable_courses[selected_index]

#Custom navigation function for course selection in assignments upload
def open_course_page(page, class_nbr):
    button = page.locator(dom.COURSE_BUTTON_ONCLICK_TEMPLATE.format(class_nbr=class_nbr))
    if button.count() == 0:
        button = page.locator(dom.COURSE_BUTTON_ONCLICK_PARTIAL_TEMPLATE.format(class_nbr=class_nbr))

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
    selected_semester_value, selected_semester_label = choose_semester(page)

    subject_headers, subject_rows = parse_table_rows(page, 0)
    if not subject_rows:
        raise RuntimeError("No subjects found for the selected semester.")

    subject_csv_rows = format_rows_for_csv(subject_headers, subject_rows)

    subject_csv_path = DATA_DIR / make_csv_filename(selected_semester_label, "subjects")
    write_csv_file(subject_csv_path, subject_headers, subject_csv_rows)
    print(f"Saved semester subjects CSV to {subject_csv_path}")

    course_class_nbr, course_title, course_type, course_code = choose_course(page, subject_rows)
    print(f"Opening course page for: {course_title} ({course_class_nbr}) - {course_type} - {course_code}")
    open_course_page(page, course_class_nbr)

    assignment_headers, assignment_rows = parse_table_rows(page, 1)
    if not assignment_rows:
        raise RuntimeError("No assignments found for the selected course.")

    assignment_csv_rows = format_rows_for_csv(assignment_headers, assignment_rows)

    assignment_csv_path = DATA_DIR / make_csv_filename(selected_semester_label, course_class_nbr, "assignments")
    write_csv_file(assignment_csv_path, assignment_headers, assignment_csv_rows)
    print(f"Saved assignment CSV to {assignment_csv_path}")
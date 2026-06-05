from pathlib import Path
import csv
import re
from playwright.sync_api import Page
from utils import dom
from blocks.assignments import choose_semester

DATA_DIR = Path(__file__).resolve().parents[2] / "data/csv"
DATA_DIR.mkdir(parents=True, exist_ok=True)
GRADE_CACHE = {}


def sanitize_filename(value: str) -> str:
    return re.sub(r"[^\w\-.]+", "_", value.strip())


def write_csv_file(file_path: Path, headers, rows):
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)


def _semester_cache_key(semester_value, semester_label):
    return sanitize_filename(semester_value or semester_label or "unknown_semester")

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


def _capture_table_snapshot(page, table_index):
    headers, rows = parse_table_rows(page, table_index)
    return {
        "table_index": table_index,
        "headers": headers,
        "rows": rows,
    }


def _row_text_contains(row_data, query):
    query = query.strip().lower()
    if not query:
        return False

    for value in row_data.values():
        if query in str(value).lower():
            return True

    return False


def get_cached_grade_data(semester_value=None, semester_label=None):
    if semester_value is not None or semester_label is not None:
        return GRADE_CACHE.get(_semester_cache_key(semester_value, semester_label))

    if len(GRADE_CACHE) == 1:
        return next(iter(GRADE_CACHE.values()))

    return None


def get_cached_course_tables(course_identifier, semester_value=None, semester_label=None):
    cached_data = get_cached_grade_data(semester_value, semester_label)
    if not cached_data:
        return []

    matched_tables = []
    for table_data in cached_data.get("tables", []):
        table_text = {
            "headers": " ".join(table_data["headers"]),
            "rows": table_data["rows"],
        }
        if _row_text_contains(table_text, course_identifier):
            matched_tables.append(table_data)

    return matched_tables


def _cache_grade_tables(page, semester_value, semester_label):
    table_count = page.locator(dom.CUSTOM_TABLE_SELECTOR).count()
    if table_count == 0:
        raise RuntimeError("No grade tables were found on the page.")

    tables = [_capture_table_snapshot(page, table_index) for table_index in range(table_count)]

    cached_entry = {
        "semester_value": semester_value,
        "semester_label": semester_label,
        "summary": tables[0],
        "tables": tables,
    }
    GRADE_CACHE[_semester_cache_key(semester_value, semester_label)] = cached_entry
    return cached_entry


def _write_grade_cache_csvs(semester_label, cached_entry):
    summary = cached_entry["summary"]
    subject_csv_path = DATA_DIR / f"semester_subjects_{sanitize_filename(semester_label)}.csv"
    summary_csv_rows = format_rows_for_csv(summary["headers"], summary["rows"])
    write_csv_file(subject_csv_path, summary["headers"], summary_csv_rows)

    for table_data in cached_entry["tables"][1:]:
        detail_csv_path = DATA_DIR / (
            f"semester_details_{sanitize_filename(semester_label)}_table_{table_data['table_index']}.csv"
        )
        detail_csv_rows = format_rows_for_csv(table_data["headers"], table_data["rows"])
        write_csv_file(detail_csv_path, table_data["headers"], detail_csv_rows)

    return subject_csv_path

def display_grades(page):
    semester_value, semester_label = choose_semester(page)
    page.wait_for_selector(dom.CUSTOM_TABLE_SELECTOR)
    cached_entry = _cache_grade_tables(page, semester_value, semester_label)

    headers = cached_entry["summary"]["headers"]
    rows = cached_entry["summary"]["rows"]

    if not rows:
        raise RuntimeError("No marks found for the selected semester.")    
    
    subject_csv_path = _write_grade_cache_csvs(semester_label, cached_entry)
    print(f"Saved semester subjects CSV to {subject_csv_path}")

from pathlib import Path
import csv
from playwright.sync_api import Page
from utils import dom
from utils.filename import make_csv_filename
from blocks.assignments.router import choose_semester

DATA_DIR = Path(__file__).resolve().parents[2] / "data/csv"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def write_csv_file(file_path: Path, headers, rows):
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        writer.writerows(rows)

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

def display_marks(page):
    page.wait_for_selector(dom.CUSTOM_TABLE_SELECTOR)
    _,semester = choose_semester(page)
    headers , rows = parse_table_rows(page,0)
    
    if not rows:
        raise RuntimeError("No marks found for the selected semester.")    
    
    subject_csv_path = DATA_DIR / make_csv_filename(semester, "marks")
    rows_csv = format_rows_for_csv(headers,rows)

    write_csv_file(subject_csv_path, headers, rows_csv)
    print(f"Saved semester marks CSV to {subject_csv_path}")

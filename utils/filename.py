import re


def kebab_case(value: str) -> str:
    """Convert a string into kebab-case suitable for filenames."""
    if value is None:
        return ""
    normalized = str(value).strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized.strip("-")


def make_csv_filename(*parts: str, ext: str = ".csv") -> str:
    """Build a kebab-cased CSV filename from arbitrary parts."""
    filename_parts = [kebab_case(part) for part in parts if part and str(part).strip()]
    filename = "-".join(filename_parts)
    if not filename:
        filename = "output"
    if not filename.endswith(ext):
        filename = f"{filename}{ext}"
    return filename
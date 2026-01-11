from pathlib import Path


def parse_filename(file_path: Path) -> tuple[str, str]:
    name = file_path.stem

    if " " not in name:
        return "", name

    number, title = name.split(" ", 1)
    return number, title

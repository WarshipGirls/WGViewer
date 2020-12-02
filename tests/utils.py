from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_file_size(file_path: Path) -> int:
    return Path(file_path).stat().st_size

# End of File

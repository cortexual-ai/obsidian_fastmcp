import os
import yaml
from datetime import datetime
from typing import Optional


def get_creation_time_from_frontmatter(file_path: str) -> Optional[str]:
    """
    Get the creation time from a file's YAML frontmatter.

    Args:
        file_path (str): Path to the file to read

    Returns:
        Optional[str]: ISO format datetime string if found in frontmatter, None otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return None

        _, frontmatter, _ = content.split("---", 2)
        frontmatter_dict = yaml.safe_load(frontmatter.strip())
        return frontmatter_dict.get("created")
    except Exception:
        return None


def get_creation_time_from_stats(file_path: str) -> str:
    """
    Get the creation time from system file stats.
    Handles both macOS (st_birthtime) and Linux (st_ctime) systems.

    Args:
        file_path (str): Path to the file to read

    Returns:
        str: ISO format datetime string of file creation time
    """
    try:
        stat = os.stat(file_path)
        if hasattr(stat, "st_birthtime"):  # macOS
            return datetime.fromtimestamp(stat.st_birthtime).isoformat()
        else:  # Linux: fallback to last metadata change (approximation)
            return datetime.fromtimestamp(stat.st_ctime).isoformat()
    except Exception:
        return datetime.now().isoformat()


def get_file_creation_time(file_path: str) -> str:
    """
    Get the creation time of a file, trying frontmatter first, then falling back to system stats.

    Args:
        file_path (str): Path to the file to read

    Returns:
        str: ISO format datetime string of file creation time
    """
    # Try to get creation time from frontmatter first
    created_date = get_creation_time_from_frontmatter(file_path)

    # If not found in frontmatter, fall back to system stats
    if created_date is None:
        created_date = get_creation_time_from_stats(file_path)

    return created_date

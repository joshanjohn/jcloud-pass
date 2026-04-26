"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from typing import Any, Dict, Optional


def get_username_from_email(
        email: str
    ) -> str: 
    """
    Returns email domain as username for given email.

    ```
    example: email = "test@gmail.com" 
    returns ->  "test"
    ```
    """
    return email.split("@")[0]


def get_parent_path(dir_path: str) -> str:
    """
    Returns the parent path of given directory.

    ```
    example: dir_path = "/home/data/bin"
    returns -> /home/data
    ```
    """
    parts = dir_path.rsplit("/", 1)
    # parts[0] is empty string for root-level paths like '/docs'
    return parts[0] if len(parts) == 2 and parts[0] else "/"


def normalize_dir_path(path: str) -> str:
    """
    Normalize a directory path so it always matches stored metadata.
    """
    cleaned = (path or "").strip()
    if not cleaned or cleaned == "/":
        return "/"
    return "/" + cleaned.strip("/")


def get_file_directory_path(file_path: str) -> str:
    """
    Return the directory path that contains a file.
    """
    normalized = (file_path or "").strip().strip("/")
    if not normalized or "/" not in normalized:
        return "/"
    return normalize_dir_path(normalized.rsplit("/", 1)[0])


def iter_directory_paths(dir_path: str):
    """
    Yield the given directory and each parent directory up to root.
    """
    current_path = normalize_dir_path(dir_path)
    while True:
        yield current_path
        if current_path == "/":
            break
        current_path = normalize_dir_path(get_parent_path(current_path))


def find_file_in_directories(
    user_record: Optional[Dict[str, Any]],
    file_id: str,
    file_path: Optional[str] = None
) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Find the directory and file metadata entry for a given file.
    
    """
    if not user_record or "directory" not in user_record:
        return None, None

    normalized_lookup = (file_path or "").strip().strip("/")

    for directory in user_record.get("directory", []):
        for file_data in directory.get("data", []):
            stored_path = file_data.get("meta", {}).get("path", "").strip().strip("/")
            if file_data.get("id") == file_id or (normalized_lookup and stored_path == normalized_lookup):
                return directory, file_data

    return None, None

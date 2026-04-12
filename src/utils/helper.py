

def get_username_from_email(
        email: str
    ) -> str: 
    """
    Return email domain as username for given email
    """
    return email.split("@")[0]


def get_parent_path(dir_path: str) -> str:
    """
    Returns the parent path of given directory.
    """
    parts = dir_path.rsplit("/", 1)
    # parts[0] is empty string for root-level paths like '/docs'
    return parts[0] if len(parts) == 2 and parts[0] else "/"

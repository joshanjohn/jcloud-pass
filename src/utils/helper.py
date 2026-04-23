"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

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


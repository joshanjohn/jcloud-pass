from fastapi import status
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2.id_token import verify_firebase_token
import re

from src.utils.variables import logger

firebase_request_adapter = requests.Request()

def token_validation(token: str):
    if not token:
        logger.error("No Token Found!")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        logger.info("Clear token cookies.. ")
        return response

    try:
        data = verify_firebase_token(token, firebase_request_adapter)
        logger.info("Token validated successfully")
        return data

    except Exception as e:
        logger.error(f"Error while validating token: {str(e)}")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response
    
def valid_dir_name(dir_name: str) -> tuple[str, dict | None]:
    """
    Validates and strips a directory name.
    Returns (stripped_name, None) if valid,
    or      (stripped_name, {"success": False, "message": "..."})
    """
    dir_name = dir_name.strip()

    # Must not be empty
    if not dir_name:
        return dir_name, {"success": False, "message": "Folder name cannot be empty"}

    # dot path names
    if dir_name in {".", ".."}:
        return dir_name, {"success": False, "message": "'.' and '..' are reserved names"}


    # Invalid characters 
    invalid_chars = r'[\/:*?"<>.|]'
    match = re.search(invalid_chars, dir_name)
    if match:
        return dir_name, {"success": False, "message": f"Folder name contains an invalid character: '{match.group()}'"}

    # Must not start or end with a space (already stripped) or a dot
    if dir_name.startswith(".") or dir_name.endswith("."):
        return dir_name, {"success": False, "message": "Folder name cannot start or end with a dot"}

    return dir_name, None
"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from fastapi import status
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2.id_token import verify_firebase_token
import re

from src.utils.variables import logger

firebase_request_adapter = requests.Request()

def token_validation(token: str):
    """
    Token Validation method which validate given token. 
    and if token is valid, it return the data from firebase
    otherwise, it redirects to login page and clear cookies 
    for "token". 
    """
    # check if token is exist 
    if not token:
        logger.error("No Token Found!")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token") # clear cookies 
        logger.info("Clear token cookies.. ")
        return response

    # verify the token and return firebase data 
    try:
        data = verify_firebase_token(token, firebase_request_adapter)
        logger.info("Token validated successfully")
        return data

    # if exception occur, clear token and redirect to login page 
    except Exception as e:
        logger.error(f"Error while validating token: {str(e)}")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response
    
def valid_dir_name(dir_name: str) -> tuple[str, dict | None]:
    """
    Validation Method for given directory name, returns directory name and the message for each validation. 
    """

    # remove empty space from both enf 
    dir_name = dir_name.strip()

    # Must not be empty
    if not dir_name:
        return dir_name, {"success": False, "message": "Folder name cannot be empty"}

    # dot path names
    if dir_name in {".", ".."}:
        return dir_name, {"success": False, "message": "'.' and '..' are reserved names"}


    # Invalid special characters 
    invalid_chars = r'[\/:*?"<>.|]'
    match = re.search(invalid_chars, dir_name)
    if match:
        return dir_name, {"success": False, "message": f"Folder name contains an invalid character: '{match.group()}'"}

    # Must not start or end with a space (already stripped) or a dot
    if dir_name.startswith(".") or dir_name.endswith("."):
        return dir_name, {"success": False, "message": "Folder name cannot start or end with a dot"}

    return dir_name, None
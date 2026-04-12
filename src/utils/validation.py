from fastapi import status
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2.id_token import verify_firebase_token

from src.utils.variables import logger

firebase_request_adapter = requests.Request()

def token_validation(token: str):
    if not token:
        logger.error("No Token Found!")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        logger.info("Clear token cookies.. ")
        response.delete_cookie("token")
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
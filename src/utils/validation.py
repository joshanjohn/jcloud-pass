from fastapi import status
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2.id_token import verify_firebase_token


firebase_request_adapter = requests.Request()

def token_validation(token: str):
    if not token:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response

    try:
        data = verify_firebase_token(token, firebase_request_adapter)
        return data

    except Exception:
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response
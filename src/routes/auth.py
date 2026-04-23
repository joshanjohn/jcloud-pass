"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.utils import (
    firebase_api_key, 
    firebase_authDomain,
    firebase_projectId,
    firebase_storageBucket,
    firebase_messagingSenderId,
    firebase_appId,
    firebase_measurementId,
    logger)

router = APIRouter()

# Initialize templates relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))


@router.get("/auth/config")
async def get_firebase_config():
    """
    Endpoint to return the firebase configurations 
    """

    logger.info("GET request for '/auth/config'")

    return {
        "apiKey": firebase_api_key,
        "authDomain": firebase_authDomain,
        "projectId": firebase_projectId,
        "storageBucket": firebase_storageBucket,
        "messagingSenderId":  firebase_messagingSenderId,
        "appId": firebase_appId,
        "measurementId": firebase_measurementId
    }

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request): 
    """
    Render login page
    """
    logger.info("GET request for '/login'")

    return templates.TemplateResponse(
        request=request, 
        name="auth/login.html"
    )


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request): 
    """
    Render signup page
    """
    logger.info("GET request for '/signup'")
    return templates.TemplateResponse(
        request=request, 
        name="auth/signup.html"
    )


@router.get("/logout")
async def logout():
    """
    Clear token cookie and redirect to landing page
    """
    logger.info("GET request for '/logout'")
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("token")
    return response

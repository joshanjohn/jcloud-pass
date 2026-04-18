from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.utils import firebase_api_key, logger

router = APIRouter()

# Initialize templates relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))

# --- GET requests ---

@router.get("/auth/config")
async def get_firebase_config():
    """
    Returns Firebase public configuration for the frontend
    """

    logger.info("GET request for '/auth/config'")
    return {
        "apiKey": firebase_api_key,
        "authDomain": "jcloud-paas.firebaseapp.com",
        "projectId": "jcloud-paas",
        "storageBucket": "jcloud-paas.firebasestorage.app",
        "messagingSenderId": "758103231649",
        "appId": "1:758103231649:web:6ab6d4dbbaa972bb4774e0",
        "measurementId": "G-9DSBL5ZJRT"
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

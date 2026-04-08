import os
import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.utils.variables import firebase_api_key

router = APIRouter()

# Initialize templates relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))

# --- GET requests ---

@router.get("/auth/config")
async def get_firebase_config():
    """Returns Firebase public configuration for the frontend."""
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
    return templates.TemplateResponse(
        request=request, 
        name="auth/login.html"
    )

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request): 
    return templates.TemplateResponse(
        request=request, 
        name="auth/signup.html"
    )

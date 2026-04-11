from fastapi import APIRouter, Request, status, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from google.oauth2.id_token import verify_firebase_token
from google.auth.transport import requests
from pathlib import Path

from src.services.system_service import SystemService
from src.utils.variables import logger
from src.entities.user import User

router = APIRouter()

# Initialize templates relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))

firebase_request_adapter = requests.Request()

@router.get("/workspace", response_class=HTMLResponse)
async def workspace(request: Request):
    id_token = request.cookies.get('token')

    if not id_token:
        # redirect to login 
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        data = verify_firebase_token(id_token, firebase_request_adapter)
        _user = User(
            id=data["user_id"], 
            name=data["email"]
        )

        directories = {"directory": []}
        try: 
            sys_service = SystemService(user=_user)
            directories = sys_service.get_all_dir()

        except Exception as e: 
            logger.error(f"Error in SystemService: {str(e)}")
            pass
        
        return templates.TemplateResponse(
            request=request,
            name="workspace/workspace.html", 
            context={
                "user_email": data["email"], 
                "directories": directories
            }
        )
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/workspace/create_directory")
async def create_directory(request: Request, name: str = Body(..., embed=True)):
    id_token = request.cookies.get('token')
    if not id_token:
        return {"success": False, "message": "unauthorized"}
    
    try:
        data = verify_firebase_token(id_token, firebase_request_adapter)
        _user = User(
            id=data["user_id"], 
            name=data["email"]
        )
        
        sys_service = SystemService(user=_user)
        success = sys_service.create_dir(name)
        
        if success:
            return {"success": True, "message": f"Directory '{name}' created"}
        else:
            return {"success": False, "message": "Failed to create directory"}

    except Exception as e:
        logger.error(f"Error creating directory: {str(e)}")
        return {"success": False, "message": str(e)}

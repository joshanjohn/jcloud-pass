from fastapi import APIRouter, Request, status, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from google.oauth2.id_token import verify_firebase_token
from google.auth.transport import requests
from pathlib import Path

from src.services.system_service import SystemService
from src.utils.variables import logger
from src.entities.user import User
from src.utils.validation import token_validation

router = APIRouter()

# Initialize templates relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))

firebase_request_adapter = requests.Request()

@router.get("/workspace", response_class=HTMLResponse)
async def workspace(request: Request):
    id_token = request.cookies.get('token')

    validation_result = token_validation(id_token)
    if isinstance(validation_result, RedirectResponse):
        return validation_result
    
    data = validation_result
    
    try:
        _user = User(
            id=data["user_id"], 
            name=data["email"]
        )

        sys_service = SystemService(user=_user)
        sidebar_dirs = sys_service.get_dirs_in_path("/")
        current_dirs  = sidebar_dirs  # root view shows root-level dirs

        return templates.TemplateResponse(
            request=request,
            name="workspace/workspace.html", 
            context={
                "user_email": data["email"], 
                "sidebar_dirs": sidebar_dirs,
                "current_dirs": current_dirs,
                "path": "/",
                "breadcrumbs": [],
            }
        )
    except Exception as e:
        logger.error(f"Error in workspace route: {str(e)}")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response

@router.post("/workspace/create_directory")
async def create_directory(
    request: Request,
    name: str = Body(..., embed=True),
    path: str = Body("/", embed=True)
):
    id_token = request.cookies.get('token')
    
    validation_result = token_validation(id_token)
    if isinstance(validation_result, RedirectResponse):
        return validation_result
    
    data = validation_result

    try:
        _user = User(
            id=data["user_id"], 
            name=data["email"]
        )
        
        sys_service = SystemService(user=_user)

        # Build the full path: root stays "/", nested appends "/name"
        clean_path = path.rstrip("/") if path != "/" else ""
        full_path = f"{clean_path}/{name}"

        success = sys_service.create_dir(name, full_path)
        
        if success:
            return {"success": True, "message": f"Directory '{name}' created"}
        else:
            return {"success": False, "message": "Failed to create directory"}

    except Exception as e:
        logger.error(f"Error creating directory: {str(e)}")
        return {"success": False, "message": str(e)}


@router.get("/workspace/{folder_path:path}", response_class=HTMLResponse)
async def workspace_subdir(request: Request, folder_path: str):
    id_token = request.cookies.get('token')
    
    validation_result = token_validation(id_token)
    if isinstance(validation_result, RedirectResponse):
        return validation_result
    
    data = validation_result

    try:
        _user = User(
            id=data["user_id"],
            name=data["email"]
        )

        sys_service = SystemService(user=_user)

        # Normalise to an absolute path: /docs/projects
        current_path = "/" + folder_path.strip("/")

        # Validate the path exists as a stored directory
        all_dirs = sys_service.get_all_dir()
        all_paths = {
            d.get("meta", {}).get("path", "")
            for d in (all_dirs or {}).get("directory", [])
        }
        if current_path not in all_paths:
            return RedirectResponse(url="/workspace", status_code=status.HTTP_303_SEE_OTHER)

        # Sidebar always shows root-level dirs
        sidebar_dirs = sys_service.get_dirs_in_path("/")
        # Main grid shows immediate children of current path
        current_dirs = sys_service.get_dirs_in_path(current_path)

        # Build breadcrumbs: [{name, url}, ...]
        segments = [s for s in folder_path.split("/") if s]
        breadcrumbs = [
            {"name": seg, "url": "/workspace/" + "/".join(segments[: i + 1])}
            for i, seg in enumerate(segments)
        ]

        return templates.TemplateResponse(
            request=request,
            name="workspace/workspace_subdir.html",
            context={
                "user_email": data["email"],
                "sidebar_dirs": sidebar_dirs,
                "current_dirs": current_dirs,
                "path": current_path,
                "breadcrumbs": breadcrumbs,
            },
        )

    except Exception as e:
        logger.error(f"Error in workspace_subdir: {str(e)}")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response

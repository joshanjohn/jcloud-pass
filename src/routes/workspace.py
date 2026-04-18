from fastapi import APIRouter, Request, status, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from google.auth.transport import requests
from pathlib import Path
import urllib.parse

from src.services.system_service import SystemService
from src.services.directory_service import DirectoryService
from src.utils import logger, token_validation, valid_dir_name
from src.entities import User

router = APIRouter()

# Initialize templates relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))

firebase_request_adapter = requests.Request()

current_user = None



@router.post("/workspace/create_directory")
async def create_directory(
    request: Request,
    name: str = Form(...),
    path: str = Form("/")
):
    """
    POST request for creating a directory with name on path
    """    
    logger.info(f"POST request for '/workspace/create_directory'")
    
    id_token = request.cookies.get('token')
    
    # validating id token 
    validation_result = token_validation(id_token)
    if isinstance(validation_result, RedirectResponse):
        return validation_result
    
    data = validation_result

    name, error = valid_dir_name(name)
    redirect_url = f"/workspace{path if path != '/' else ''}"
    if error:
        return RedirectResponse(url=f"{redirect_url}?error={urllib.parse.quote(error['message'])}", status_code=status.HTTP_303_SEE_OTHER)

    try:
        current_user = User(id=data["user_id"] , email=data["email"])
        sys_service = SystemService(user=current_user)
        current_user = sys_service.get_user()
        

        # Build the full path: root stays "/", nested appends "/name"
        clean_path = path.rstrip("/") if path != "/" else ""
        full_path = f"{clean_path}/{name}"

        success = sys_service.create_dir(name, full_path)
        
        if success:
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(url=f"{redirect_url}?error=Failed+to+create+directory", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        logger.error(f"Error creating directory: {str(e)}")
        return RedirectResponse(url=f"{redirect_url}?error={urllib.parse.quote(str(e))}", status_code=status.HTTP_303_SEE_OTHER)




@router.post("/workspace/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    path: str = Form("/")
):
    """
    POST request for uploading a file to a path
    """
    logger.info(f"POST request for '/workspace/upload'")
    
    id_token = request.cookies.get('token')
    
    validation_result = token_validation(id_token)
    if isinstance(validation_result, RedirectResponse):
        return validation_result
    
    data = validation_result
    redirect_url = f"/workspace{path if path != '/' else ''}"

    try:
        current_user = User(id=data["user_id"] , email=data["email"])
        sys_service = SystemService(user=current_user)
        current_user = sys_service.get_user()
        

       
        
        # # Read the file contents
        file_data = await file.read()

        # Upload the file
        success = sys_service.upload_file(
            file=file, 
            data=file_data,
            path=path
        )
        
        if success:
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse(url=f"{redirect_url}?error=Failed+to+upload+file", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return RedirectResponse(url=f"{redirect_url}?error={urllib.parse.quote(str(e))}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/workspace/{folder_path:path}", response_class=HTMLResponse)
@router.get("/workspace", response_class=HTMLResponse, include_in_schema=False)
async def workspace(request: Request, folder_path: str = ""):
    """
    Render workspace page dynamically for root and subdirectories
    """
    logger.info(f"GET request for workspace: '{folder_path}'")

    # getting token from cookies 
    id_token = request.cookies.get('token')

    # token validation 
    validation_result = token_validation(id_token)
    if isinstance(validation_result, RedirectResponse):
        return validation_result
    
    data = validation_result
    
    try:
        current_user = User(id=data["user_id"], email=data["email"])
        sys_service = SystemService(user=current_user)
        current_user = sys_service.get_user()
        
        # Normalise to an absolute path: e.g., "/" or "/docs/projects"
        current_path = "/" + folder_path.strip("/") if folder_path else "/"

        # Validate the path exists if it's not the root
        if current_path != "/":
            all_dirs = sys_service.get_all_dir()
            all_paths = {
                d.get("meta", {}).get("path", "")
                for d in (all_dirs or {}).get("directory", [])
            }
            if current_path not in all_paths:
                logger.warning(f"Path not found: {current_path}, redirecting to root")
                return RedirectResponse(url="/workspace/", status_code=status.HTTP_303_SEE_OTHER)

        # Sidebar always shows root-level dirs (or current context, depending on preference)
        # Here we follow existing logic: it shows items in the current path
        sidebar_dirs = sys_service.get_dirs_in_path("/")
        workspace_dirs = sys_service.get_dirs_in_path(current_path)
        
        # Fetch blobs associated with current_path
        workspace_files = sys_service.storage_service.list_dirs(current_path)

        # Build dynamic breadcrumbs
        segments = [s for s in folder_path.split("/") if s]
        breadcrumbs = [
            {"name": seg, "url": "/workspace/" + "/".join(segments[: i + 1])}
            for i, seg in enumerate(segments)
        ]

        return templates.TemplateResponse(
            request=request,
            name="workspace/workspace.html", 
            context={
                "username": current_user.name,
                "user_email": data["email"], 
                "sidebar_dirs": sidebar_dirs,
                "workspace_dirs": workspace_dirs,
                "workspace_files": workspace_files,
                "path": current_path,
                "breadcrumbs": breadcrumbs,
            }
        )
    except Exception as e:
        logger.error(f"Error in workspace route: {str(e)}")
        response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        response.delete_cookie("token")
        return response

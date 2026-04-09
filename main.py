
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from google.oauth2.id_token import verify_firebase_token
from google.auth.transport import requests
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from src.database.core.mongodb_connection import MongoConnection
from src.services.system_service import SystemService
from src.utils.variables import logger
from src.entities.user import User


from src.routes.auth import router as auth_router



app = FastAPI()

# Include Routers
app.include_router(auth_router)

firebase_request_adapter = requests.Request()



app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static",
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))



@app.get('/', response_class=HTMLResponse)
async def root(request: Request): 
    id_token = request.cookies.get('token')
    if not id_token: 
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            
        )
    
    return RedirectResponse(url="/workspace", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/workspace", response_class=HTMLResponse)
async def workspace(request: Request):
    id_token = request.cookies.get('token')

    if not id_token:
        # redirect to login 
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    data = verify_firebase_token(id_token, firebase_request_adapter)
    _user = User(
        id= data["user_id"], 
        name= data["email"]
    )


    try: 
        sys_service = SystemService(user=_user)
    except Exception as e: 
        logger.error(str(e))
        pass
       

    
    
    
    return templates.TemplateResponse(
        request=request,
        name="workspace/workspace.html", 
        context={
            "user_email": data["email"]  
        }
    )


def main():
   
    logger.info(f"Starting application. BASE_DIR: {BASE_DIR}")

    mongodb_instance = MongoConnection()
    users = mongodb_instance.get_connection()

    uvicorn.run("main:app", reload=True)
    
    

if __name__ == "__main__":
    main()

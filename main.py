
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import logging
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from src.logging import configure_logging
from src.database.core.mongodb_connection import MongoConnection
import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin
try:
    firebase_admin.initialize_app()
except Exception as e:
    logging.warning(f"Firebase Admin already initialized or failed: {e}")


from src.routes.auth import router as auth_router

app = FastAPI()
# Include Routers
app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static",
)
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))



@app.get('/', response_class=HTMLResponse)
async def root(request: Request): 
    id_token_val = request.cookies.get('token')
    if id_token_val: 
        return RedirectResponse(url="/workspace", status_code=303)
    
    return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "name": "Josh"
            }
        )

@app.get("/workspace", response_class=HTMLResponse)
async def workspace(request: Request):
    id_token_val = request.cookies.get('token')
    if not id_token_val:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="workspace/workspace.html"
    )


def main():
    configure_logging(log_level="info")

    mongodb_instance = MongoConnection()
    users = mongodb_instance.get_connection()

    uvicorn.run("main:app", reload=True)
    
    

if __name__ == "__main__":
    logging.info("BASE_DIR :",BASE_DIR)

    main()

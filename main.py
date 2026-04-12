
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

load_dotenv()

from src.routes.auth import router as auth_router
from src.utils import logger
from src.routes.workspace import router as workspace_router


app = FastAPI()

# Include Routers
app.include_router(auth_router)
app.include_router(workspace_router)



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


def main():
   
    logger.info(f"Starting application. BASE_DIR: {BASE_DIR}")
    uvicorn.run("main:app", reload=True)
    
    

if __name__ == "__main__":
    main()

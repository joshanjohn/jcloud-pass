
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

import uvicorn
from src.routes.auth import router as auth_router
from src.utils import logger, jcloud_port
from src.routes.workspace import router as workspace_router

BASE_DIR = Path(__file__).resolve().parent 

app = FastAPI()

# Include Routers
app.include_router(auth_router)          # authentication router
app.include_router(workspace_router)     # workspace router

# mount static files folder 
app.mount(
    path="/static",
    app=StaticFiles(directory="src/static"),
    name="static",
)

# base dir 

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
    uvicorn.run("main:app", port=jcloud_port,reload=True)
    
    

if __name__ == "__main__":
    main()

from src.logging import configure_loggin
from src.database.core.mongodb_connection import MongoConnection
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static",
)
templates = Jinja2Templates(directory=str(BASE_DIR / "src" / "templates"))

@app.get('/', response_class=HTMLResponse)
async def root(request: Request): 
    id_token = request.cookies.get('token')
    print("COOKIES: ", request.cookies.values())
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "name": "Josh",
        }
    )


def main():
    # mongodb_instance = MongoConnection()
    # users = mongodb_instance.get_connection()

    # configure_loggin(log_level="debug")
    uvicorn.run("main:app", reload=True)
    


if __name__ == "__main__":
    main()

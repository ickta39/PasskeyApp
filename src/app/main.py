from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import dotenv
import uvicorn
import os

from api import route

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.include_router(route, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, port=80)
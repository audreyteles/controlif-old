import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from routers import students
from starlette.staticfiles import StaticFiles
from fastapi.logger import logger
from pydantic import BaseSettings



app = FastAPI(title="ControlIF", docs_url="/docs")
app.mount("/imgs", StaticFiles(directory="imgs"), name='images')


@app.get("/")
async def index():
    return FileResponse('index.html')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)


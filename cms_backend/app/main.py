from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import db
from routes import router as cms_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield  

app = FastAPI(lifespan=lifespan)

app.mount("/public", StaticFiles(directory="public"), name="public")
app.include_router(cms_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
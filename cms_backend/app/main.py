from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes import router as cms_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield  

app = FastAPI(lifespan=lifespan)

app.include_router(cms_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
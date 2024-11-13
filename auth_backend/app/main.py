from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes import router as auth_router
from bot import start_bot



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    bot_task = asyncio.create_task(start_bot())
    yield 
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
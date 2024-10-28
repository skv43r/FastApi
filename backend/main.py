from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
import aiohttp
import json
import os
import aiofiles
import uvicorn
from typing import Annotated
from models import User
from database import create_db_and_tables, get_session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield 

app = FastAPI(lifespan=lifespan)

if not os.path.exists("public"):
    os.makedirs("public")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],    # Разрешен доступ с localhost:3000
    allow_credentials=True,
    allow_methods=["*"],    # Разрешены все HTTP методы (GET, POST и т.д.)
    allow_headers=["*"],    # Разрешены все заголовки
)


@app.post("/users/")
async def create_user(user: User,  session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/")
async def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}")
async def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete(("/users/{user_id}"))
async def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

@app.get("/external-data")
async def get_external_data():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://api.npoint.io/88fcfcbf4fde970ba6f2") as response:
                data = await response.json()
                async with aiofiles.open ("data.json", "w") as file:
                    await file.write(json.dumps(data, indent=4))

                for user in data["users"]:
                    avatar_url = user["avatar"] 
                    user_id = user["id"]

                    file_name = f"user_{user_id}.jpg"
                    file_path = os.path.join("public", file_name)

                    async with session.get(avatar_url) as img_response:
                        if img_response.status == 200:
                            async with aiofiles.open(file_path, "wb") as image_file:
                                content = await img_response.read()
                                await image_file.write(content)
                        else:
                            return {"error": f"Failed to download image for user {user_id}"}

                return data
        except Exception as e:
            return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request, session: SessionDep):
    try:
        async with aiofiles.open("data.json", "r") as file:
                data = json.loads(await file.read())
                json_users = {user["id"]: user for user in data["users"]}

                existing_users = session.exec(select(User)).all()
                existing_user_ids = {user.id for user in existing_users}

                for user_id, user_data in json_users.items():
                    if user_id not in existing_user_ids:
                        user = User(
                            id=user_data["id"],
                            name=user_data["name"],
                            email=user_data["email"],
                            avatar=user_data["avatar"]
                        )
                        session.add(user)
                    else:
                        existing_user = session.get(User, user_id)
                        existing_user.name = user_data["name"]
                        existing_user.email = user_data["email"]
                        existing_user.avatar = user_data["avatar"]

                for existing_user in existing_users:
                    if existing_user.id not in json_users:
                        session.delete(existing_user)

                session.commit()

                users = session.exec(select(User)).all()
                
                return templates.TemplateResponse("index.html", {
                    "request": request,
                    "users": users
                })
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")
    
@app.get("/api")
async def get_json_file():
    return FileResponse("data.json", media_type="application/json", filename="data.json")


if  __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

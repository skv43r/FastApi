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

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],    # Разрешен доступ с localhost:3000
    allow_credentials=True,
    allow_methods=["*"],    # Разрешены все HTTP методы (GET, POST и т.д.)
    allow_headers=["*"],    # Разрешены все заголовки
)

@app.get("/api/external-data")
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

@app.get("/api/import-users")
async def import_users(session: SessionDep):
    async with aiohttp.ClientSession() as session_json:
        try:
            async with session_json.get("https://api.npoint.io/88fcfcbf4fde970ba6f2") as response:
                data = await response.json()

                for user in data["users"]:
                    user_id = user["id"]
                    avatar_url = user["avatar"]
                    existing_user = session.get(User, user_id)

                    if existing_user is None:
                        user = User(
                            id=user_id,
                            name=user["name"],
                            email=user["email"],
                            avatar=user["avatar"],
                        )
                        session.add(user)
                    else:
                        existing_user.name = user["name"]
                        existing_user.email = user["email"]
                        existing_user.avatar = user["avatar"]
                    
                    file_name = f"user_{user_id}.jpg"
                    file_path = os.path.join("public", file_name)

                    async with session_json.get(avatar_url) as img_response:
                        if img_response.status == 200:
                            async with aiofiles.open(file_path, "wb") as image_file:
                                content = await img_response.read()
                                await image_file.write(content)
                        else:
                            return {"error": f"Failed to download image for user {user_id}"}

                session.commit()

                return {"message": "Users imported successfully"}
        except Exception as e:
            return {"error": str(e)}

@app.get("/api/users/")
async def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

@app.post("/api/add")
async def  add_user(session: SessionDep, user: User):
    try:
        if not user.name or not user.email:
            raise HTTPException(status_code=400, detail="Name and email are required")
    
        if user.id:
            existing_user = session.get(User, user.id)
            if existing_user:
                raise HTTPException(status_code=400, detail="User with this ID already exists")

        existing_email = session.exec(
            select(User).where(User.email == user.email)
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "User  added successfully", "user": user}
    except Exception as e:
        session.rollback()  # Откат изменений в случае ошибки
        print("Error occurred:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api", response_class=HTMLResponse)
async def main_page(request: Request, session: SessionDep):
    try:
        users = session.exec(select(User)).all()
                     
        return templates.TemplateResponse("index.html", {
            "request": request,
            "users": users
        })
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")

@app.get("/api/return")
async def return_user(session: SessionDep):
    try:
        users = session.exec(select(User)).all()
        user_data = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "avatar": user.avatar
            }
            for user in users
        ]
        return {"users": user_data}
    except Exception as e:
        return {"error": str(e)}


if  __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session, select
from database import get_session
from models import User
import aiohttp
import aiofiles
import json
import os

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter()

@router.get("/api/cms/external-data")
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

@router.get("/api/cms/import-users")
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

# @router.get("/api/cms/users/")
# async def read_users(session: SessionDep):
#     users = session.exec(select(User)).all()
#     return users

@router.get("/api/cms/return")
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
    
@router.post("/api/cms/user-added")
async def user_added(user: User, session: SessionDep):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": "User  processed in CMS", "user": user}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/api/cms/users")
async def get_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return {"users": users}
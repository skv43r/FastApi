from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select
import aiohttp
import json
import os
import aiofiles
import uvicorn
from typing import Annotated
from models import User, AuthUser, TelegramOTP
from database import create_db_and_tables, get_session, hash_password, create_access_token, verify_password, verify_access_token
from datetime import datetime
from bot import send_otp, start_bot
import asyncio

SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
        session.rollback()
        print("Error occurred:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/api/delete/{user_id}")
async def delete_user(session: SessionDep, user_id: int):
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User  not found")
        session.delete(user)
        session.commit()

        return {"message": "User  deleted successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/api/edit/{user_id}")
async def edit_user(session: SessionDep, user_id: int, user_data: User):
    try:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User  not found")
        user.name = user_data.name
        user.email = user_data.email
        user.avatar = user_data.avatar

        session.commit()
        return {"message": "User  updated successfully"}
    except Exception as e:
        session.rollback()
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

@app.get("/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        # Проверяем токен
        verify_access_token(token)
        return {"message": "You have access to this protected route"}
    except HTTPException as e:
        raise e


@app.post("/api/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: SessionDep):
    try:
        user = session.exec(
            select(AuthUser).where(AuthUser.username == form_data.username)
            ).first()
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        user.last_login = datetime.utcnow()
        session.commit()
        access_token = create_access_token(data={"sub": user.username})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/register-email")
async def register(data: AuthUser,
                   session: SessionDep):
    existing_user = session.exec(select(AuthUser).where(AuthUser.email == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    new_user = AuthUser(
        username=data.username,
        email=data.email,
        password=hash_password(data.password)
    )
    session.add(new_user)

    try:
        session.commit()
        session.refresh(new_user)
        access_token = create_access_token(data={"sub": new_user.email})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error during registration: {str(e)}")
    
    return {"access_token": access_token,
            "token_type": "bearer",
            "username": new_user.username}

@app.post("/api/register")
async def register(data: TelegramOTP, session: SessionDep):
    telegram_id = data.telegram_id
    try:
        telegram_id = int(data.telegram_id)
        otp = await send_otp(telegram_id)
        if not otp:
                raise HTTPException(status_code=500, detail="Failed to send OTP")
        
        user_otp = session.exec(select(TelegramOTP).where(TelegramOTP.telegram_id == telegram_id)).first()

        if user_otp:
            user_otp.otp = otp
        else:
            user_otp = TelegramOTP(username=data.username, telegram_id=telegram_id, otp=otp)
            session.add(user_otp)
        
        session.commit()
        
        return {"message": "OTP sent successfully", "otp": otp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/verify-otp")
async def verify_otp(data: TelegramOTP, session: SessionDep):
    telegram_id = data.telegram_id
    otp = data.otp

    print(f"Received telegram_id: {telegram_id}, otp: {otp}")

    if not telegram_id or not otp:
        raise HTTPException(status_code=400, detail="Telegram ID and OTP are required")
    
    user_otp = session.exec(select(TelegramOTP).where(TelegramOTP.telegram_id == telegram_id)).first()
    if not user_otp:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_otp.otp == data.otp:
        access_token = create_access_token(data={"sub": user_otp.telegram_id})
        user_otp.otp = None
        session.commit()

        return {
            "message": "OTP verified successfully",
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

if  __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

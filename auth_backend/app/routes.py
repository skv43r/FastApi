from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime
from typing import Annotated
from sqlmodel import Session, select
from database import get_session
from models import AuthUser, TelegramOTP
from utils import create_access_token, verify_access_token, verify_password, hash_password
from bot import send_otp

SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.get("/api/auth/protected-route")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        verify_access_token(token)
        return {"message": "You have access to this protected route"}
    except HTTPException as e:
        raise e


@router.post("/api/auth/login")
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

@router.post("/api/auth/register-email")
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

@router.post("/api/auth/register")
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
    
@router.post("/api/auth/verify-otp")
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
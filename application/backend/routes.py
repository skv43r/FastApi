from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import db
from models import User
from user_controller import UserController
from typing import Annotated

SessionDep = Annotated[Session, Depends(db.get_session)]
router = APIRouter()

@router.post("/api/add")
async def add_user_endpoin(session: SessionDep, user: User):
    user_controller = UserController(session)
    return await user_controller.add_user(user)
    
@router.delete("/api/delete/{user_id}")
async def delete_user_endpoint(session: SessionDep, user_id: int):
    user_controller = UserController(session)
    return await user_controller.delete_user(user_id)
    
@router.put("/api/edit/{user_id}")
async def edit_user_endpoint(session: SessionDep, user_id: int, user_data: User):
    user_controller = UserController(session)
    return await user_controller.edit_user(user_id, user_data)

@router.get("/api/return")
async def return_user_endpoint(session: SessionDep):
    user_controller = UserController(session)
    return await user_controller.return_users()

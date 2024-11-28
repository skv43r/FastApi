from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import extract
from database import db
from models import User
from user_controller import UserController
from typing import Annotated
from models import Service, Trainer, TimeSlot
from datetime import datetime

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

@router.get("/api/services")
async def return_services_endpoint(session: SessionDep):
    services = session.exec(select(Service)).all()
    return services

@router.get("/api/trainers")
async def return_trainers_endpoint(session: SessionDep):
    trainers = session.exec(select(Trainer)).all()
    return trainers

@router.get("/api/timeslots")
async def return_timeslots_endpoint(session: SessionDep, service_id: int, trainer_id: int = Query(..., alias="trainerId"), date: str = Query(..., format="date")):
    timeslots = session.exec(
        select(TimeSlot).where(
            TimeSlot.trainer_id == trainer_id,
            TimeSlot.dates == date,
            TimeSlot.service_id == service_id
        )
    ).all()
    return timeslots


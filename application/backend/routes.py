from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from database import db
from models import User
from user_controller import UserController
from typing import Annotated
from models import Service, Trainer, TimeSlot, Booking, Branch

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
            TimeSlot.service_id == service_id,
            TimeSlot.available == True
        )
    ).all()
    return timeslots

@router.post("/api/bookings")
async def post_booking_data_endpoint(session: SessionDep, booking_data: dict):
    timeslot = session.exec(select(TimeSlot).where(
        TimeSlot.id == booking_data["timeSlotId"],
        TimeSlot.dates == booking_data["date"],
        TimeSlot.service_id == booking_data["serviceId"]
    )).first()

    if not timeslot:
        raise HTTPException(status_code=400, detail="Выбранное время уже занято")
    
    timeslot.available = False
    
    new_booking = Booking(
        service=booking_data["serviceId"],
        master=booking_data["trainerId"],
        dates=booking_data["date"],
        time=booking_data["timeSlotId"]
    )

    session.add(new_booking)
    session.commit()
    
    return {"message": "Бронирование успешно создано", "booking_id": new_booking.id}
    

@router.get("/api/branch-info")
async def get_about_info(session: SessionDep):
    branch = session.exec(select(Branch)).all()
    return branch
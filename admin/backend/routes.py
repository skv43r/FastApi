from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from database import db 
from typing import Annotated
from models import Service, Trainer, TimeSlot, Booking, Branch, GroupClass, TrainerGroup


SessionDep = Annotated[Session, Depends(db.get_session)]
router = APIRouter()

@router.get("/api/admin/trainers")
async def get_trainers_endpoint(session: SessionDep):
    return session.exec(select(Trainer)).all()

@router.post("/api/admin/trainer/add")
async def add_trainer_endpoin(session: SessionDep, trainer: Trainer):
    try:
        if not trainer.name or not trainer.specialization:
                raise HTTPException(status_code=400,
                                    detail=" Имя и Специализация обязательны")
        existing_trainer = session.get(Trainer, trainer.id) if trainer.id else None
        if existing_trainer:
                raise HTTPException(status_code=400,
                                    detail="Тренер уже существует")
        session.add(trainer)
        session.commit()
        session.refresh(trainer)
    except Exception as e:
             session.rollback()
             raise e
    
@router.delete("/api/admin/trainer/delete/{trainer_id}")
async def delete__trainer_endpoint(session: SessionDep, trainer_id: int):
    try:
        trainer = session.get(Trainer, trainer_id)
        if not trainer:
                    raise HTTPException(status_code=404, detail="Тренер не найден")
        session.delete(trainer)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
@router.put("/api/admin/trainer/edit/{trainer_id}")
async def edit_trainer_endpoint(session: SessionDep, trainer_id: int, trainer_data: Trainer):
    try:
        trainer = session.get(Trainer, trainer_id)
        if not trainer:
            raise HTTPException(status_code=404, detail="Тренер не найден")
        
        trainer.name = trainer_data.name
        trainer.description = trainer_data.description
        trainer.specialization = trainer_data.specialization
        trainer.photo = trainer_data.photo
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

@router.get("/api/admin/services")
async def return_services_endpoint(session: SessionDep):
    services = session.exec(select(Service)).all()
    return services

@router.post("/api/admin/service/add")
async def add_service_endpoin(session: SessionDep, service: Service):
    try:
        if not service.name or not service.type:
                raise HTTPException(status_code=400,
                                    detail="Название и тип обязательны")
        existing_service = session.get(Trainer, service.id) if service.id else None
        if existing_service:
                raise HTTPException(status_code=400,
                                    detail="Сервис уже существует")
        session.add(service)
        session.commit()
        session.refresh(service)
    except Exception as e:
             session.rollback()
             raise e
    
@router.delete("/api/admin/service/delete/{service_id}")
async def delete__trainer_endpoint(session: SessionDep, service_id: int):
    try:
        service = session.get(Service, service_id)
        if not service:
                    raise HTTPException(status_code=404, detail="Сервис не найден")
        session.delete(service)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
@router.put("/api/admin/service/edit/{service_id}")
async def edit_trainer_endpoint(session: SessionDep, service_id: int, service_data: Service):
    try:
        service = session.get(Service, service_id)
        if not service:
            raise HTTPException(status_code=404, detail="Сервис не найден")
        
        service.name = service_data.name
        service.duration = service_data.duration
        service.description = service_data.description
        service.price = service_data.price
        service.type = service_data.type
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

# @router.get("/api/trainers")
# async def return_trainers_endpoint(session: SessionDep, group_class_id: int = None, service_id: int = Query(None, alias="serviceId")):
#     today = datetime.now().date()
#     query = (
#         select(Trainer)
#         .join(Trainer.time_slots)
#         .where(
#             (TimeSlot.service_id == service_id if service_id else True),
#             (TimeSlot.group_class_id == group_class_id if group_class_id else True),
#             TimeSlot.dates >= today,
#             TimeSlot.available == True
#         )
#         .distinct()
#     )
#     trainers = session.exec(query).all()
#     return trainers

# @router.get("/api/timeslots")
# async def return_timeslots_endpoint(session: SessionDep, service_id: int, trainer_id: int = Query(..., alias="trainerId"), date: str = Query(..., format="date")):
#     timeslots = session.exec(
#         select(TimeSlot).where(
#             TimeSlot.trainer_id == trainer_id,
#             TimeSlot.dates == date,
#             TimeSlot.service_id == service_id,
#             TimeSlot.available == True
#         )
#     ).all()
#     return timeslots

# @router.post("/api/bookings")
# async def post_booking_data_endpoint(session: SessionDep, booking_data: dict):
#     if "serviceId" in booking_data:
#         timeslot = session.exec(select(TimeSlot).where(
#             TimeSlot.id == booking_data["timeSlotId"],
#             TimeSlot.dates == booking_data["date"],
#             TimeSlot.service_id == booking_data["serviceId"],
#             TimeSlot.available == True
#         )).first()

#         if not timeslot:
#             raise HTTPException(status_code=400, detail="Выбранное время уже занято")
        
#         timeslot.available = False

#         new_booking = Booking(
#             service_id=booking_data["serviceId"],
#             trainer_id=booking_data["trainerId"],
#             dates=booking_data["date"],
#             timeslot_id=booking_data["timeSlotId"]
#         )

#     else:
#         timeslot = session.exec(select(TimeSlot).where(
#             TimeSlot.id == booking_data["timeSlotId"],
#         )).first()

#         if not timeslot:
#             raise HTTPException(status_code=400, detail="Выбранное время уже занято")
        
#         timeslot.available_spots -= 1
#         if timeslot.available_spots == 0:
#             timeslot.available = False
    
#         new_booking = Booking(
#             class_id=booking_data["classId"],
#             dates=booking_data["date"],
#             timeslot_id=booking_data["timeSlotId"],
#             name=booking_data["name"],
#             phone=booking_data["phone"],
#             email=booking_data["email"]
#         )

#     session.add(new_booking)
#     session.commit()
    
#     return {"message": "Бронирование успешно создано", "booking_id": new_booking.id}
    

# @router.get("/api/branch-info")
# async def get_about_info(session: SessionDep):
#     branch = session.exec(select(Branch)).all()
#     return branch

# @router.get("/api/booking-details")
# async def get_success_data(session: SessionDep):
#     query = (
#         select(
#             Booking.id,
#             Booking.dates,
#             TimeSlot.times.label("timeslot"),
#             Trainer.name.label("trainer_name"),
#             Service.name.label("service_name")
#         )
#         .join(TimeSlot, Booking.timeslot_id == TimeSlot.id)
#         .join(Trainer, Booking.trainer_id == Trainer.id)
#         .join(Service, Booking.service_id == Service.id)
#         .order_by(Booking.created_at.desc())
#         .limit(1)
#     )
#     result = session.exec(query).first()

#     if result:
#         return {
#             "serviceName": result.service_name,
#             "trainerName": result.trainer_name,
#             "date": result.dates,
#             "time": result.timeslot
#         }
#     return {"error": "No booking found"}

# @router.get("/api/group-classes")
# async def get_group_classes_endpoint(session: SessionDep, date: str = Query(..., format="formattedDate")):
#     query = (
#         select(GroupClass, Trainer, TimeSlot)
#         .join(TimeSlot, TimeSlot.group_class_id == GroupClass.id)
#         .join(Trainer, Trainer.id == TimeSlot.trainer_id)
#         .where(TimeSlot.dates == date, TimeSlot.available == True, TimeSlot.available_spots > 0)
#         .order_by(TimeSlot.dates, TimeSlot.times)
#     )
    
#     result = session.exec(query).all()

#     response = []
#     for group_class, trainer, time_slot in result:
#         response.append({
#             "GroupClass": {
#                 "id": group_class.id,
#                 "name": group_class.name,
#                 "duration": group_class.duration,
#                 "description": group_class.description,
#                 "price": group_class.price
#             },
#             "Trainer": {
#                 "id": trainer.id,
#                 "name": trainer.name,
#                 "description": trainer.description,
#                 "photo": trainer.photo
#             },
#             "TimeSlot": {
#                 "id": time_slot.id,
#                 "trainer_id": time_slot.trainer_id,
#                 "date": time_slot.dates,
#                 "times": time_slot.times,
#                 "available": time_slot.available,
#                 "available_spots": time_slot.available_spots,
#                 "created_at": time_slot.created_at
#             }
#         })
    
#     return response
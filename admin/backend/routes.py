from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
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
        existing_service = session.get(Service, service.id) if service.id else None
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
async def delete_service_endpoint(session: SessionDep, service_id: int):
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
async def edit_service_endpoint(session: SessionDep, service_id: int, service_data: Service):
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
    
@router.get("/api/admin/groups")
async def return_groups_endpoint(session: SessionDep):
    groups = session.exec(select(GroupClass)).all()
    return groups

@router.post("/api/admin/group/add")
async def add_group_endpoin(session: SessionDep, group: GroupClass):
    try:
        if not group.name:
                raise HTTPException(status_code=400,
                                    detail="Название является обязательным")
        existing_group = session.get(GroupClass, group.id) if group.id else None
        if existing_group:
                raise HTTPException(status_code=400,
                                    detail="Групповое занятие уже существует")
        session.add(group)
        session.commit()
        session.refresh(group)
    except Exception as e:
             session.rollback()
             raise e
    
@router.delete("/api/admin/group/delete/{group_id}")
async def delete_group_endpoint(session: SessionDep, group_id: int):
    try:
        group = session.get(GroupClass, group_id)
        if not group:
                    raise HTTPException(status_code=404,
                                        detail="Групповое занятие не найдено")
        session.delete(group)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
@router.put("/api/admin/group/edit/{group_id}")
async def edit_group_endpoint(session: SessionDep, group_id: int, group_data: GroupClass):
    try:
        group = session.get(GroupClass, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Групповое занятие не найдено")
        
        group.name = group_data.name
        group.duration = group_data.duration
        group.description = group_data.description
        group.price = group_data.price
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

@router.get("/api/admin/times")
async def return_timeslots_endpoint(session: SessionDep, trainer_id: int = Query(..., description="ID тренера"), date: str = Query(..., description="Дата записи")):
    query = (
        select(
            TimeSlot.id.label("timeslot_id"),
            Trainer.name.label("trainer_name"),
            Service.name.label("service_name"),
            GroupClass.name.label("group_name"),
            TimeSlot.dates.label("date"),
            TimeSlot.times.label("time"),
            TimeSlot.available.label("status"),
            TimeSlot.available_spots.label("available_spots"),
        )
        .join(Trainer, TimeSlot.trainer_id == Trainer.id)
        .join(Service, TimeSlot.service_id == Service.id, isouter=True)
        .join(GroupClass, TimeSlot.group_class_id == GroupClass.id, isouter=True)
    )
    
    if trainer_id:
        query = query.where(TimeSlot.trainer_id == trainer_id)
    if date:
        query = query.where(TimeSlot.dates == date)
        
    time_slots = session.exec(query).all()
    
    return [
        {
            "timeslot_id": ts.timeslot_id,
            "trainer_name": ts.trainer_name or "Тренер не указан",
            "service_name": ts.service_name or "Не указано",
            "group_name": ts.group_name or "Не указано",
            "date": ts.date if ts.date else "Дата не указана",
            "time": ts.time if ts.time else "Время не указано",
            "status": ts.status or False,
            "available_spots": ts.available_spots or 0,
        }
        for ts in time_slots
    ]

@router.post("/api/admin/time/add")
async def add_time_endpoin(session: SessionDep, time: TimeSlot):
    try:
        if not time.trainer_id or not time.dates or not time.times:
                raise HTTPException(status_code=400,
                                    detail="Поля тренер, дата и время являются обязательными")
        existing_time = session.get(TimeSlot, time.id) if time.id else None
        if existing_time:
                raise HTTPException(status_code=400,
                                    detail="Временной слот уже существует")
        session.add(time)
        session.commit()
        session.refresh(time)
    except Exception as e:
             session.rollback()
             raise e
    
@router.delete("/api/admin/time/delete/{time_id}")
async def delete_time_endpoint(session: SessionDep, time_id: int):
    try:
        time = session.get(TimeSlot, time_id)
        if not time:
                    raise HTTPException(status_code=404,
                                        detail="Временной слот не найден")
        session.delete(time)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
@router.put("/api/admin/time/edit/{time_id}")
async def edit_time_endpoint(session: SessionDep, time_id: int, time_data: TimeSlot):
    try:
        time = session.get(TimeSlot, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Временной слот не найден")
        
        time.trainer_id = time_data.trainer_id
        time.service_id = time_data.service_id
        time.group_class_id = time_data.group_class_id
        time.dates = time_data.dates
        time.times = time_data.times
        time.available = time_data.available
        time.available_spots = time_data.available_spots
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
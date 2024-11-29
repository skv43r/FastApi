from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, time, datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    avatar: str | None = Field(default=None)

class IndividualSpecialists(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    photo: str | None = Field(default=None)

class IndividualServices(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, index=True)
    photo: str | None = Field(default=None)

class Massage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, index=True)

class GroupSpecialists(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    photo: str | None = Field(default=None)

class GroupServices(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, index=True)
    photo: str | None = Field(default=None)

class Booking(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    service: int = Field(nullable=False)
    master: int = Field(nullable=False)
    dates: str = Field(nullable=False)
    time: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    duration: float | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, index=True)
    photo: str | None = Field(default=None)
    category: str = Field(index=True)
    type: str = Field(index=True)

    time_slots: list["TimeSlot"] = Relationship(back_populates="service")

class Trainer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = Field(default=None)
    specialization: str = Field(index=True)
    photo: str | None = Field(default=None)

    time_slots: list["TimeSlot"] = Relationship(back_populates="trainer")

class TimeSlot(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    trainer_id: int = Field(foreign_key="trainer.id", nullable=False)
    service_id: int = Field(foreign_key="service.id", nullable=False)
    dates: date = Field(nullable=False)
    times: time = Field(nullable=False)
    available: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    trainer: Optional["Trainer"] = Relationship(back_populates="time_slots")
    service: Optional["Service"] = Relationship(back_populates="time_slots")

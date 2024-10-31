from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Generic, Optional, Sequence, TypeVar


class BaseReservation(BaseModel):
    arrival_date: datetime
    departure_date: datetime
    apartment_id: int


class Reservation(BaseReservation):
    id: int

    class Config:
        from_attributes = True


class ReservationCreate(BaseReservation):
    email: EmailStr


class ReservationUpdate(BaseReservation):
    email: EmailStr


class PaginatedReservation(BaseModel):
    items: list[Reservation]
    size: Optional[int]
    total: Optional[int]




class ApartmentData(BaseModel):
    title: str
    address: str

    class Config:
        from_attributes = True




class ReservationNotification(BaseModel):
    email: EmailStr
    arrival_date: datetime
    departure_date: datetime
    apartment_data: ApartmentData

    class Config:
        from_attributes = True
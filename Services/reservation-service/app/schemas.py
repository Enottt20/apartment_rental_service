from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class Reservation(BaseModel):
    id: int
    email: EmailStr
    arrival_date: datetime
    departure_date: datetime
    apartment_id: int

    class Config:
        from_attributes = True


class ApartmentData(BaseModel):
    title: str
    address: str

    class Config:
        from_attributes = True


class Apartment(BaseModel):
    id: int
    title: str
    address: str
    rooms: int
    area: int
    latitude: float
    longitude: float

    class Config:
        from_attributes = True



class ReservationNotification(BaseModel):
    email: EmailStr
    arrival_date: datetime
    departure_date: datetime
    apartment_data: ApartmentData

    class Config:
        from_attributes = True
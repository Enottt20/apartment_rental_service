from datetime import datetime
from pydantic import BaseModel


class ApartmentData(BaseModel):
    title: str
    address: str

    class Config:
        from_attributes = True


class ReservationNotification(BaseModel):
    email: str
    arrival_date: datetime
    departure_date: datetime
    apartment_data: ApartmentData

    class Config:
        from_attributes = True


from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Reservation(BaseModel):
    id: int
    arrival_date: datetime
    departure_date: datetime
    apartment_id: int

    class Config:
        from_attributes = True
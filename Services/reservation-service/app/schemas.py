from typing import Optional

from pydantic import BaseModel


class Apartment(BaseModel):
    id: int
    address: str
    rooms: int
    area: int
    latitude: float
    longitude: float

    class Config:
        from_attributes = True
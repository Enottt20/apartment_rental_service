from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseApartment(BaseModel):
    title: str
    address: str
    rooms: int
    area: int
    latitude: float
    longitude: float
    publisher_email: EmailStr


class Apartment(BaseApartment):
    id: int

    class Config:
        from_attributes = True


class ApartmentCreate(BaseApartment):
    pass


class ApartmentUpdate(BaseApartment):
    pass

class ApartmentsQuery(BaseModel):
    city_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[float]
    limit: int = 1
    offset: int = 0
from typing import Optional
from pydantic import BaseModel, EmailStr


class BaseApartment(BaseModel):
    title: str
    address: str
    rooms: int
    area: int
    latitude: float
    longitude: float


class Apartment(BaseApartment):
    id: int
    publisher_email: EmailStr

    class Config:
        from_attributes = True


class ApartmentCreate(BaseApartment):
    publisher_email: EmailStr


class ApartmentUpdate(BaseApartment):
    publisher_email: EmailStr


class ApartmentsQuery(BaseModel):
    city_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[float]
    limit: int = 1
    offset: int = 0


class PaginatedApartmentResponse(BaseModel):
    items: list[Apartment]
    size: Optional[int]
    total: Optional[int]


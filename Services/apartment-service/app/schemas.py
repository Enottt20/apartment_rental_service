from typing import Optional

from pydantic import BaseModel


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


class ApartmentsQuery(BaseModel):
    city_name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    radius: Optional[float]
    limit: int = 1
    offset: int = 0

    class Config:
        from_attributes = True

# class FavoriteItem(BaseModel):
#     id: int
#     name: str
#     description: str
#     apartment_id: int
#
#     class Config:
#         from_attributes = True
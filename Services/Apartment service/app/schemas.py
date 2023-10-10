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

# class FavoriteItem(BaseModel):
#     id: int
#     name: str
#     description: str
#     apartment_id: int
#
#     class Config:
#         from_attributes = True
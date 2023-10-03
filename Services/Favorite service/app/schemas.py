from pydantic import BaseModel

class Apartment(BaseModel):
    id: int
    address: str
    rooms: int
    area: int

    class Config:
        from_attributes = True

class FavoriteItem(BaseModel):
    id: int
    name: str
    description: str
    apartment_id: int

    class Config:
        from_attributes = True
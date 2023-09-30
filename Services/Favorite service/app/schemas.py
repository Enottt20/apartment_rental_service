from pydantic import BaseModel

class Apartment(BaseModel):
    id: int
    address: str
    rooms: int
    area: int

class FavoriteItem(BaseModel):
    id: int
    name: str
    description: str
    apartment: Apartment


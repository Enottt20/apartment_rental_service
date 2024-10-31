from pydantic import BaseModel, EmailStr
from typing import Generic, Optional, Sequence, TypeVar

from fastapi import HTTPException, Query
from pydantic import BaseModel


class BaseFavoriteItem(BaseModel):
    apartment_id: int


class FavoriteItem(BaseFavoriteItem):
    id: int

    class Config:
        from_attributes = True


class PaginatedFavoriteItemsResponse(BaseModel):
    items: list[FavoriteItem]
    size: Optional[int]
    total: Optional[int]


class FavoriteItemCreate(BaseFavoriteItem):
    user_email: EmailStr


class FavoriteItemDelete(BaseFavoriteItem):
    pass
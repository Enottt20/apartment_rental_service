from pydantic import BaseModel, EmailStr


class BaseFavoriteItem(BaseModel):
    apartment_id: int
    user_email: EmailStr


class FavoriteItem(BaseFavoriteItem):
    id: int

    class Config:
        from_attributes = True


class FavoriteItemCreate(BaseFavoriteItem):
    pass


class FavoriteItemDelete(BaseFavoriteItem):
    pass
from pydantic import BaseModel, EmailStr
from uuid import UUID


class ReviewBase(BaseModel):
    apartment_id: int
    title: str
    description: str


class ReviewNotification(BaseModel):
    email: EmailStr
    title: str
    description: str


class ReviewCreate(ReviewBase):
    user_email: EmailStr


class ReviewUpdate(BaseModel):
    title: str
    description: str


class Review(ReviewBase):
    id: UUID

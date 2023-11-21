from sqlalchemy import Column, Integer, String
from .database import Base


class FavoriteItem(Base):
    __tablename__ = 'favorite_items'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    apartment_id = Column(Integer)
    user_email = Column(String)
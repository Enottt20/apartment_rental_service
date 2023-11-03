from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float, DateTime
import datetime
from sqlalchemy.orm import relationship
from .database import Base
from geoalchemy2 import Geometry

class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, index=True)
    arrival_date = Column(DateTime, default=datetime.datetime.utcnow)
    departure_date = Column(DateTime, default=datetime.datetime.utcnow)
    apartment_id = Column(Integer)



# class FavoriteItem(Base):
#     __tablename__ = 'favorite_items'
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)
#     apartment_id = Column(Integer)
#
#     #apartment = relationship("Apartment", back_populates="favorite_item")
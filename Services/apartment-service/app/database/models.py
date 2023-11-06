from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, Float
from sqlalchemy.orm import relationship
from .database import Base
from geoalchemy2 import Geometry

class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    address = Column(String, index=True)
    rooms = Column(Integer)
    area = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry("POINT", srid=4326))



# class FavoriteItem(Base):
#     __tablename__ = 'favorite_items'
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String)
#     apartment_id = Column(Integer)
#
#     #apartment = relationship("Apartment", back_populates="favorite_item")
from sqlalchemy import Column, Integer, String, Float
from .database import Base
from geoalchemy2 import Geometry

class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    address = Column(String, index=True)
    rooms = Column(Integer)
    area = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(Geometry("POINT", srid=4326))
    publisher_email = Column(String)

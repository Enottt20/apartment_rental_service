from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    rooms = Column(Integer)
    area = Column(Integer)


class FavoriteItem(Base):
    __tablename__ = 'favorite_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))

    apartment = relationship("Apartment", back_populates="favorite_item")
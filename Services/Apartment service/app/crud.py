from .schemas import Apartment
from sqlalchemy.orm import Session
from .database import models
from sqlalchemy import func
from geoalchemy2 import Geometry
import requests

def get_apartments(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.Apartment) \
        .offset(offset) \
        .limit(limit) \
        .all()


def get_apartment(db: Session, apartment_id: int):
    return db.query(models.Apartment) \
        .filter(models.Apartment.id == apartment_id) \
        .first()


def find_nearby_apartments(db: Session, latitude: float, longitude: float, radius: float):
    location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)
    apartments = db.query(models.Apartment).filter(
        func.ST_DWithin(models.Apartment.location, location, radius)
    ).all()
    return apartments



# Функция для геокодирования города через Nominatim
def geocode_city(city_name):
    base_url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city_name,
        "format": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data and len(data) > 0:
        city_coords = {
            "lat": float(data[0]["lat"]),
            "lng": float(data[0]["lon"])
        }
        print(city_coords)
        return city_coords
    else:
        return None


def add_apartment(db: Session, apartment: Apartment):

    db_item = models.Apartment(
        id=apartment.id,
        address=apartment.address,
        rooms=apartment.rooms,
        area=apartment.area,
        latitude=apartment.latitude,
        longitude=apartment.longitude,
        location=f'POINT({apartment.latitude} {apartment.longitude})'
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return apartment


def update_apartment(db: Session, apartment_id: int, updated_apartment: Apartment):
    # Получаем существующую запись квартиры по ID
    db_apartment = db.query(models.Apartment).filter(models.Apartment.id == apartment_id).first()

    if db_apartment:
        # Обновляем поля квартиры на основе данных из updated_apartment
        db_apartment.address = updated_apartment.address
        db_apartment.rooms = updated_apartment.rooms
        db_apartment.area = updated_apartment.area
        db_apartment.latitude = updated_apartment.latitude
        db_apartment.longitude = updated_apartment.longitude
        db_apartment.location=f'POINT({updated_apartment.latitude} {updated_apartment.longitude})'

        # Сохраняем обновленную запись
        db.commit()
        return db_apartment

    return None


def delete_apartment(db: Session, apartment_id: int):
    result = db.query(models.Apartment) \
        .filter(models.Apartment.id == apartment_id) \
        .delete()
    db.commit()
    return result == 1

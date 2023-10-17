from .schemas import Apartment
from sqlalchemy.orm import Session
from .database import models
from sqlalchemy import func
from geoalchemy2 import Geometry
from . import geo_functions


def get_apartment(db: Session, apartment_id: int):
    return db.query(models.Apartment) \
        .filter(models.Apartment.id == apartment_id) \
        .first()


def get_apartments(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.Apartment) \
        .offset(offset) \
        .limit(limit) \
        .all()


def get_apartments2(db: Session, *filters):
    apartments = db.query(models.Apartment)

    filters = dict(filters)

    limit = filters.get('limit')
    offset = filters.get('offset')
    radius = dict(filters).get('radius')
    city_name = dict(filters).get('city_name')
    latitude = dict(filters).get('latitude')
    longitude = dict(filters).get('longitude')

    if limit and offset:
        apartments = apartments.offset(offset).limit(limit).all()

    if city_name:
        city_coords = geo_functions.geocode_city(city_name)

        if city_coords is None:
            return None

        latitude = city_coords["lat"]
        longitude = city_coords["lng"]

    if latitude is not None and longitude is not None and radius is not None:
        location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)

        apartments = apartments.filter(
            func.ST_DWithin(models.Apartment.location, location, radius)
        ).order_by(func.ST_Distance(models.Apartment.location, location)).offset(offset).limit(limit).all()

    return apartments


def get_nearby_apartments(db: Session, latitude: float, longitude: float, radius: float, limit: int = 1,
                          offset: int = 0):
    location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)

    apartments = db.query(models.Apartment).filter(
        func.ST_DWithin(models.Apartment.location, location, radius)
    ).order_by(func.ST_Distance(models.Apartment.location, location)).offset(offset).limit(limit).all()

    return apartments


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

    # Если обьект уже существует то дальше не идем
    if get_apartment(db=db, apartment_id=apartment.id):
        return None

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
        db_apartment.location = f'POINT({updated_apartment.latitude} {updated_apartment.longitude})'

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

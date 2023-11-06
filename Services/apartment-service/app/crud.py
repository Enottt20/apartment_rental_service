from .schemas import Apartment, ApartmentsQuery
from sqlalchemy.orm import Session
from .database import models
from sqlalchemy import func
from geoalchemy2 import Geometry
from .geo_functions import geocode_city

def get_apartment(db: Session, apartment_id: int):
    return db.query(models.Apartment) \
        .filter(models.Apartment.id == apartment_id) \
        .first()


def get_apartments(db: Session, apartments_query: ApartmentsQuery):

    query = db.query(models.Apartment)

    if apartments_query.city_name is not None and apartments_query.radius is not None:
        city_coords = geocode_city(apartments_query.city_name)
        if city_coords is not None:
            latitude = city_coords["lat"]
            longitude = city_coords["lng"]
            location = func.ST_GeogFromText(f'POINT({latitude} {longitude})', type_=Geometry)
            query = query.filter(func.ST_DWithin(models.Apartment.location, location, apartments_query.radius))
            query = query.order_by(func.ST_Distance(models.Apartment.location, location))


    if apartments_query.city_name is None and apartments_query.latitude is not None and apartments_query.longitude \
            is not None and apartments_query.radius is not None:
        location = func.ST_GeogFromText(f'POINT({apartments_query.latitude} {apartments_query.longitude})', type_=Geometry)
        query = query.filter(func.ST_DWithin(models.Apartment.location, location, apartments_query.radius))
        query = query.order_by(func.ST_Distance(models.Apartment.location, location))


    query = query.offset(apartments_query.offset).limit(apartments_query.limit)
    apartments = query.all()

    return apartments


def add_apartment(db: Session, apartment: Apartment):
    db_item = models.Apartment(
        id=apartment.id,
        title=apartment.title,
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
        db_apartment.id = updated_apartment.id
        db_apartment.address = updated_apartment.address
        db_apartment.title = updated_apartment.title
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

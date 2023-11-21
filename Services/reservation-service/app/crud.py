import aiohttp
from .schemas import Reservation, ReservationNotification, ApartmentData
from sqlalchemy.orm import Session
from .database import models
from .broker import MessageProducer
from . import config

cfg: config.Config = config.load_config()

def get_reservation_items(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.Reservation) \
        .offset(offset) \
        .limit(limit) \
        .all()


def get_reservation_item(db: Session, item_id: int):
    return db.query(models.Reservation) \
        .filter(models.Reservation.id == item_id) \
        .first()


async def fetch_apartment_email(apartment_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.APARTMENT_SERVICE_ENTRYPOINT}apartments/{apartment_id}") as response:
            apartment_data = await response.json()
    return apartment_data


async def add_reservation_item(db: Session, item: Reservation, message_producer: MessageProducer):

    db_item = models.Reservation(
        id=item.id,
        email=item.email,
        arrival_date=item.arrival_date,
        departure_date=item.departure_date,
        apartment_id=item.apartment_id
    )

    apartment: dict  = await fetch_apartment_email(item.apartment_id)
    title = apartment.get('title', None)
    address = apartment.get('address', None)


    apartment_data = ApartmentData(
        title=title,
        address=address
    )

    reservation_notification = ReservationNotification(
        email=item.email,
        arrival_date=item.arrival_date,
        departure_date=item.departure_date,
        apartment_data=apartment_data
    )

    message_producer.send_message(reservation_notification.json())

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return item


def update_reservation_item(db: Session, item_id: int, updated_item: Reservation):
    result = db.query(models.Reservation) \
        .filter(models.Reservation.id == item_id) \
        .update(updated_item.dict())
    db.commit()

    if result == 1:
        return updated_item
    return None


def delete_reservation_item(db: Session, item_id: int):
    result = db.query(models.Reservation) \
        .filter(models.Reservation.id == item_id) \
        .delete()
    db.commit()
    return result == 1

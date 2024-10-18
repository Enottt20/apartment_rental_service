import aiohttp
from .schemas import ReservationNotification, ApartmentData, ReservationCreate, ReservationUpdate
from sqlalchemy.orm import Session
from .database import models
from .broker import MessageProducer
from . import config

cfg: config.Config = config.load_config()

def get_reservation_items(db: Session, user_email: str, limit: int = 1, offset: int = 0):
    total_items = db.query(models.Reservation) \
        .filter(models.Reservation.email == user_email) \
        .count()

    res = db.query(models.Reservation) \
        .filter(models.Reservation.email == user_email) \
        .offset(offset) \
        .limit(limit) \
        .all()

    return {
        "items": res,
        "total": total_items,
        "size": len(res),
    }


def get_reservation_item(db: Session, item_id: int):
    return db.query(models.Reservation) \
        .filter(models.Reservation.id == item_id) \
        .first()


async def fetch_apartment_data(apartment_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.APARTMENT_SERVICE_ENTRYPOINT}apartments/{apartment_id}") as response:
            apartment_data = await response.json()
    return apartment_data


async def add_reservation_item(db: Session, item: ReservationCreate, message_producer: MessageProducer):

    db_item = models.Reservation(**item.model_dump())

    apartment: dict = await fetch_apartment_data(item.apartment_id)
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

    return db_item


def update_reservation_item(db: Session, item_id: int, updated_item: ReservationUpdate):
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

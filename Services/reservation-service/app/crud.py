from .schemas import Reservation, ReservationNotification, ApartmentData
from sqlalchemy.orm import Session
from .database import models
from .broker import MessageProducer


def get_reservation_items(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.Reservation) \
        .offset(offset) \
        .limit(limit) \
        .all()


def get_reservation_item(db: Session, item_id: int):
    return db.query(models.Reservation) \
        .filter(models.Reservation.id == item_id) \
        .first()


def add_reservation_item(db: Session, item: Reservation, message_producer: MessageProducer):

    db_item = models.Reservation(
        id=item.id,
        arrival_date=item.arrival_date,
        departure_date=item.departure_date,
        apartment_id=item.apartment_id
    )

    apd = ApartmentData(
        title='title',
        address='address'
    )

    rn = ReservationNotification(
        email='email',
        arrival_date=item.arrival_date,
        departure_date=item.departure_date,
        apartment_data=apd
    )

    message_producer.send_message(rn.json())

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

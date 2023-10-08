from .schemas import FavoriteItem
from sqlalchemy.orm import Session
from .database import models


def get_favorite_items(db: Session, limit: int = 1, offset: int = 0):
    return db.query(models.FavoriteItem) \
        .offset(offset) \
        .limit(limit) \
        .all()


def get_favorite_item(db: Session, item_id: int):
    return db.query(models.FavoriteItem) \
        .filter(models.FavoriteItem.id == item_id) \
        .first()


def add_favorite_item(db: Session, item: FavoriteItem):

    db_item = models.FavoriteItem(
        id=item.id,
        name=item.name,
        description=item.description,
        apartment_id=item.apartment_id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return item


def update_favorite_item(db: Session, item_id: int, updated_item: FavoriteItem):
    result = db.query(models.FavoriteItem) \
        .filter(models.FavoriteItem.id == item_id) \
        .update(updated_item.dict())
    db.commit()

    if result == 1:
        return updated_item
    return None


def delete_favorite_item(db: Session, item_id: int):
    result = db.query(models.FavoriteItem) \
        .filter(models.FavoriteItem.id == item_id) \
        .delete()
    db.commit()
    return result == 1

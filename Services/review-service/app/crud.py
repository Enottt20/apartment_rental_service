import aiohttp
from starlette.responses import JSONResponse

from .schemas import ReviewUpdate, ReviewCreate, Review, ReviewNotification
from .database import models
from typing import List
from .broker import MessageProducer
from . import config

cfg: config.Config = config.load_config()


async def fetch_apartment_email(apartment_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cfg.APARTMENT_SERVICE_ENTRYPOINT}apartments/{apartment_id}") as response:
            apartment_data = await response.json()
    return apartment_data


def get_reviews_by_apartment_id(apartment_id: int, skip: int = 0, limit: int = 10) -> List[models.Review]:
    reviews = models.Review.objects(apartment_id=apartment_id).skip(skip).limit(limit)
    return reviews


async def add_review(review: ReviewCreate, message_producer: MessageProducer) -> models.Review:
    existing_review = models.Review.objects(apartment_id=review.apartment_id, user_email=review.user_email).first()

    if existing_review:
        return None

    apartment_data: dict = await fetch_apartment_email(review.apartment_id)
    email = apartment_data.get('publisher_email', None)

    review_notification = ReviewNotification(
        email=email,
        title=review.title,
        description=review.description
    )

    message_producer.send_message(review_notification.json())

    new_review = models.Review(**review.model_dump())
    new_review.save()
    return new_review


def get_review_by_uid(uid: str) -> Review:
    review = models.Review.objects(id=uid).first()

    if review is not None:
        return review


def update_review_by_uid(uid: str, review_update: ReviewUpdate) -> ReviewUpdate:
    review = models.Review.objects(id=uid).first()

    if review is None:
        return None

    review.title = review_update.title
    review.description = review_update.description

    review.save()
    return review


def remove_review_by_uid(uid: str):
    review = models.Review.objects(id=uid).first()

    if review is None:
        return JSONResponse(status_code=404, content={"message": "review not found"})

    review.delete()
    return JSONResponse(status_code=200, content={"message": "Deleted"})

from starlette.responses import JSONResponse

from .schemas import ReviewUpdate, ReviewCreate, Review
from .database import models
from typing import List


def get_reviews(skip: int = 0, limit: int = 10) -> List[models.Review]:
    return models.Review.objects \
        .skip(skip) \
        .limit(limit)


def add_review(review: ReviewCreate) -> models.Review:
    new_review = models.Review(**review.model_dump())
    new_review.save()

    return new_review


def db_model_to_review(review: models.Review) -> Review:
    return Review(
        id=review.id,
        title=review.title,
        description=review.description
    )


def get_review_by_uid(uid: str) -> Review:
    review = models.Review.objects(id=uid).first()

    if review is not None:
        return db_model_to_review(review)


def update_review_by_uid(uid: str, review_update: ReviewUpdate) -> Review:
    review = models.Review.objects(id=uid).first()

    if review is None:
        return None

    review.title = review_update.title
    review.description = review_update.description

    review.save()
    return db_model_to_review(review)


def remove_review_by_uid(uid: str):
    review = models.Review.objects(id=uid).first()

    if review is None:
        return JSONResponse(status_code=404, content={"message": "review not found"})

    review.delete()
    return JSONResponse(status_code=200, content={"message": "Deleted"})

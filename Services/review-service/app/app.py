from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

import logging
from typing import List, Annotated
from uuid import UUID

from . import config, crud, broker
from .database import MongoDB
from .schemas import ReviewUpdate, ReviewCreate, Review


logger = logging.getLogger("review-service")
logging.basicConfig(level=logging.INFO, 
                    format="[%(levelname)s][%(name)s][%(filename)s, line %(lineno)d]: %(message)s")

logger.info("Service configuration loading...")
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.model_dump_json(by_alias=True, indent=4)}'
)

logger.info("Service database loading...")
MongoDB(mongo_dsn=str(cfg.mongo_dsn))
logger.info("Service database loaded")

message_producer = broker.MessageProducer(
    dsn=cfg.RABBITMQ_DSN.unicode_string(),
    exchange_name=cfg.EXCHANGE_NAME,
    queue_name=cfg.QUEUE_NAME,
)

app = FastAPI(
    version='0.0.1',
    title='review service'
)


@app.get("/reviews", 
         summary="Returns all reviews",
         response_model=List[Review],
         tags=['reviews']
)
async def get_reviews(apartment_id: int, skip: int = 0, limit: int = 10):
    return crud.get_reviews_by_apartment_id(apartment_id, skip, limit)


@app.post("/reviews", 
         summary="Add new review",
         response_model=Review,
         tags=['reviews']
)
async def add_review(review: ReviewCreate) -> Review:
    review = await crud.add_review(review, message_producer)
    if review:
        return review
    return JSONResponse(status_code=400, content={"message": "Отзыв уже существует"})

@app.get("/reviews/{review_id}",
         summary="Get review by id",
         tags=['reviews']
)
async def get_review_uid(review_id: str) -> Review:
    review = crud.get_review_by_uid(review_id)
    if review is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return review


@app.patch("/reviews/{review_id}",
         summary="Update review info by id",
         tags=['reviews']
)
async def update_review(review_id: str, review_update: ReviewUpdate) -> Review:
    review = crud.update_review_by_uid(review_id, review_update)
    if review is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return review


@app.delete("/reviews/{review_id}", 
         summary="Delete review by id",
         tags=['reviews']
)
async def delete_review(review_id: str) -> Review:
    return crud.remove_review_by_uid(review_id)


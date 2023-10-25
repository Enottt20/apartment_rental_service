from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

import logging
from typing import List, Annotated
from uuid import UUID

from . import config, crud
from .database import MongoDB
from .schemas import ReviewUpdate, ReviewCreate, Review


################
## INITIALIZE ##
################
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



app = FastAPI(
    version='0.0.1',
    title='review service'
)


@app.get("/reviews", 
         summary="Returns all reviews",
         response_model=List[Review]
)
async def get_reviews(skip: int = 0, limit: int = 10):
    return crud.get_reviews(skip, limit)


@app.post("/reviews", 
         summary="Add new review",
         response_model=Review
)
async def add_review(review: ReviewCreate) -> Review:
    return crud.add_review(review)


@app.get("/reviews/{review_id}", 
         summary="Get review by id",
)
async def get_review_uid(review_id: str) -> Review:
    review = crud.get_review_by_uid(review_id)
    if review is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return review


@app.put("/reviews/{review_id}", 
         summary="Update review info by id",
)
async def update_review(review_id: str, review_update: ReviewUpdate) -> Review:
    review = crud.update_review_by_uid(review_id, review_update)
    if review is None:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    return review


@app.delete("/reviews/{review_id}", 
         summary="Delete review by id",
)
async def delete_review(review_id: str) -> Review:
    return crud.remove_review_by_uid(review_id)


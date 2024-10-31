from fastapi import FastAPI, Depends, Request
from pydantic import EmailStr
from starlette.responses import JSONResponse
from .schemas import FavoriteItem, FavoriteItemDelete, PaginatedFavoriteItemsResponse, FavoriteItemCreate, BaseFavoriteItem
from sqlalchemy.orm import Session
from . import crud, config
import typing
import logging
from .database import DB_INITIALIZER
from fastapi.middleware.cors import CORSMiddleware
import jwt
# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.POSTGRES_DSN))


app = FastAPI(
    title='Favorite service'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def extract_email_data(request: Request) -> str:
    try:
        if 'authorization' in request.headers:
            token = request.headers['authorization'].split(' ')[1]
            data = jwt.decode(token, cfg.JWT_SECRET, algorithms=["HS256"], audience=["fastapi-users:auth"])
            return data.get("email")
    except:
        return None
# @app.get(
#     "/favorites/{favoriteId}", status_code=201, response_model=FavoriteItem,
#     summary='По айди получить favorite item',
#     tags=['favorites']
# )
# async def get_favorite_item(
#         item_id: int,
#         db: Session = Depends(get_db)
#     ) -> FavoriteItem:
#     item = crud.get_favorite_item_by_id(db, item_id)
#     if item is not None:
#         return item
#     return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/favorites",
    summary='Возвращает список favorite items по почте пользователя',
    response_model=PaginatedFavoriteItemsResponse,
    tags=['favorites']
)
async def get_favorite_items(
        request: Request,
        limit: int = 1,
        offset: int = 0,
        db: Session = Depends(get_db)
    ) -> typing.List[FavoriteItem]:
    return crud.get_favorite_items_by_user_email(db, user_email=extract_email_data(request), limit=limit, offset=offset)


@app.post(
    "/favorites",
    status_code=201,
    response_model=FavoriteItem,
    summary='Добавляет favorite item в базу',
    tags=['favorites']
)
async def add_favorite_item(
        request: Request,
        favorite_item: BaseFavoriteItem,
        db: Session = Depends(get_db)
    ) -> FavoriteItem:
    favorite_item_create = FavoriteItemCreate(**favorite_item.dict(), user_email=extract_email_data(request))
    return crud.add_favorite_item(db, favorite_item_create)

@app.delete(
    "/favorites/{favoriteId}",
    summary='Удаляет favorite item из базы',
    tags=['favorites']
)
async def delete_favorite_item(
        item_id: int,
        db: Session = Depends(get_db)
    ) -> FavoriteItem:
    if crud.delete_favorite_item(db, item_id):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


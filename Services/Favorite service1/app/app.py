from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse
from .schemas import FavoriteItem
from sqlalchemy.orm import Session
from . import crud, config
import typing
import logging
from .database import DB_INITIALIZER

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# load config
cfg: config.Config = config.load_config()

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(cfg.postgres_dsn)

app = FastAPI(
    title='Favorite service'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/favorites/{favoriteId}", status_code=201, response_model=FavoriteItem,
    summary='По айди получить favorite item'
)
async def get_favorite_item(
        item_id: int,
        db: Session = Depends(get_db)
    ) -> FavoriteItem:
    item = crud.get_favorite_item(db, item_id)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/favorites",
    summary='Возвращает список favorite items',
    response_model=list[FavoriteItem]
)
async def get_favorite_items(
        limit: int = 1,
        offset: int = 0,
        db: Session = Depends(get_db)
    ) -> typing.List[FavoriteItem]:
    return crud.get_favorite_items(db, limit=limit, offset=offset)


@app.post(
    "/favorites",
    status_code=201,
    response_model=FavoriteItem,
    summary='Добавляет favorite item в базу'
)
async def add_favorite_item(
        favorite_item: FavoriteItem,
        db: Session = Depends(get_db)
    ) -> FavoriteItem:
    item = crud.add_favorite_item(db, favorite_item)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Элемент с id {favorite_item.id} уже существует в списке."})

@app.put(
    "/favorites/{favoriteId}",
    summary='Обновляет информацию об favorite item'
)
async def update_device(
        favoriteId: int,
        updated_item: FavoriteItem,
        db: Session = Depends(get_db)
    ) -> FavoriteItem:
    item = crud.update_favorite_item(db, favoriteId, updated_item)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete(
    "/favorites/{favoriteId}",
    summary='Удаляет favorite item из базы'
)
async def delete_device(
        favoriteId: int,
        db: Session = Depends(get_db)
    ) -> FavoriteItem:
    if crud.delete_favorite_item(db, favoriteId):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


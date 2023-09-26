from typing import Any

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse
from .schemas import FavoriteItem
from sqlalchemy.orm import Session
from . import crud
import typing
import logging
import json
from fastapi.logger import logger

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

fake_favorite_items = [
    {
      "id": 1,
      "name": "name1",
      "description": "description1",
      "apartment": {
        "id": 1,
        "address": "address1",
        "rooms": 2,
        "area": 76
      }
    },

{
      "id": 2,
      "name": "name2",
      "description": "description2",
      "apartment": {
        "id": 2,
        "address": "address2",
        "rooms": 3,
        "area": 15
      }
    },

{
      "id": 3,
      "name": "name3",
      "description": "description3",
      "apartment": {
        "id": 3,
        "address": "address3",
        "rooms": 2,
        "area": 141
      }
    }
]

app = FastAPI(
    title='Favorite service'
)

@app.get(
    "/favorites/{favoriteId}", status_code=201, response_model=FavoriteItem,
    summary='По айди получить favorite item'
)
async def get_favorite_item(
        item_id: int
    ) -> FavoriteItem:
    item = crud.get_favorite_item(item_id=item_id, data=fake_favorite_items)
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
        offset: int = 0
    ) -> typing.List[FavoriteItem]:
    return crud.get_favorite_items(data=fake_favorite_items, limit=limit, offset=offset)


@app.post(
    "/favorites", status_code=201, response_model=FavoriteItem,
    summary='Добавляет favorite item в базу'
)
async def add_favorite_item(
        favorite_item: FavoriteItem,
    ) -> FavoriteItem:
    item = crud.add_favorite_item(item=favorite_item, data=fake_favorite_items)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Элемент с id {favorite_item.id} уже существует в списке."})



@app.put("/favorites/{favoriteId}", summary='Обновляет информацию об favorite item')
async def update_device(
        item_id: int,
        updated_item: FavoriteItem,
    ) -> FavoriteItem:

    item = crud.update_favorite_item(item_id=item_id, updated_item=updated_item, data=fake_favorite_items)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})



@app.delete("/favorites/{favoriteId}", summary='Удаляет favorite item из базы')
async def delete_device(
        item_id: int
    ) -> FavoriteItem:
    if crud.delete_favorite_item(item_id=item_id, data=fake_favorite_items):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})






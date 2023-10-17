from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse
from .schemas import Apartment
from sqlalchemy.orm import Session
from . import crud, config, geo_functions
import typing
import logging
from .database import DB_INITIALIZER

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

#load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json()}'
)

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(str(cfg.POSTGRES_DSN))


app = FastAPI(
    title='Apartment service'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/apartments/{apartment_id}", status_code=201, response_model=Apartment,
    summary='По айди получить apartment'
)
async def get_apartment(
        apartment_id: int,
        db: Session = Depends(get_db)
    ) -> Apartment:
    item = crud.get_apartment(db, apartment_id)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/apartments",
    summary='Возвращает список apartments',
    response_model=list[Apartment]
)
async def get_apartments(
        limit: int = Query(10, description="Максимальное количество записей"),
        offset: int = Query(0, description="Смещение записей"),
        city_name: str = Query(None, description="Название города"),
        radius: float = Query(None, description="радиус в метрах"),
        latitude: float = Query(None, description="широта"),
        longitude: float = Query(None, description="долгота"),
        db: Session = Depends(get_db)
    ) -> typing.List[Apartment]:
    """
    Возвращает список ближайших квартир и сортирует по близости.
    В первую очередь по городу.
    Во вторую очередь по широте и долготе.
    Если не указать город и координаты, то вернет просто список квартир.
    """

    apartments = crud.get_apartments2(db, limit, offset, city_name, radius, latitude, longitude)

    if apartments is None:
        return JSONResponse(status_code=404, content={"message": "Не валидный запрос"})
    return apartments

    if city_name:
        city_coords = geo_functions.geocode_city(city_name)
        if city_coords is None:
            return JSONResponse(status_code=404, content={"message": "Город не найден"})
        latitude = city_coords["lat"]
        longitude = city_coords["lng"]

    if latitude is not None and longitude is not None and radius is not None:
        return crud.get_nearby_apartments(db, latitude, longitude, radius, limit, offset)
    else:
        return crud.get_apartments(db, limit, offset)


@app.post(
    "/apartments",
    status_code=201,
    response_model=Apartment,
    summary='Добавляет apartment в базу'
)
async def add_apartment(
        apartment: Apartment,
        db: Session = Depends(get_db)
    ) -> Apartment:
    item = crud.add_apartment(db, apartment)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Элемент с id {apartment.id} уже существует в списке."})


@app.put(
    "/apartments/{apartment_id}",
    summary='Обновляет информацию об apartment'
)
async def update_apartment(
        apartment_id: int,
        updated_item: Apartment,
        db: Session = Depends(get_db)
    ) -> Apartment:
    item = crud.update_apartment(db, apartment_id, updated_item)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete(
    "/apartments/{apartment_id}",
    summary='Удаляет favorite item из базы'
)
async def delete_apartment(
        apartment_id: int,
        db: Session = Depends(get_db)
    ) -> Apartment:
    if crud.delete_apartment(db, apartment_id):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


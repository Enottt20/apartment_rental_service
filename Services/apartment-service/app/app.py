from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse
from .schemas import Apartment, ApartmentsQuery, ApartmentCreate, ApartmentUpdate
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
    summary='По айди получить apartment',
    tags=['apartments']
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
    response_model=list[Apartment],
    tags=['apartments']
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

    apartments_query = ApartmentsQuery(
        limit=limit,
        offset=offset,
        city_name=city_name,
        radius=radius,
        latitude=latitude,
        longitude=longitude
    )

    apartments = crud.get_apartments(db, apartments_query)

    return apartments


@app.post(
    "/apartments",
    status_code=201,
    response_model=Apartment,
    summary='Добавляет apartment в базу',
    tags=['apartments']
)
async def add_apartment(
        apartment: ApartmentCreate,
        db: Session = Depends(get_db)
    ) -> Apartment:
    return crud.add_apartment(db, apartment)


@app.patch(
    "/apartments/{apartment_id}",
    summary='Обновляет информацию об apartment',
    tags=['apartments']
)
async def update_apartment(
        apartment_id: int,
        updated_item: ApartmentUpdate,
        db: Session = Depends(get_db)
    ) -> Apartment:
    item = crud.update_apartment(db, apartment_id, updated_item)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete(
    "/apartments/{apartment_id}",
    summary='Удаляет apartment из базы',
    tags=['apartments']
)
async def delete_apartment(
        apartment_id: int,
        db: Session = Depends(get_db)
    ) -> Apartment:
    if crud.delete_apartment(db, apartment_id):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


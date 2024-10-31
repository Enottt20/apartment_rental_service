from fastapi import FastAPI, Depends, Query
from fastapi import FastAPI, Depends, Request
from starlette.responses import JSONResponse
from .schemas import Apartment, ApartmentsQuery, ApartmentCreate, ApartmentUpdate, BaseApartment, PaginatedApartmentResponse
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
    response_model=PaginatedApartmentResponse,
    tags=['apartments']
)
async def get_apartments(
        request: Request,
        my_apartments: bool = Query(False, description="Получить свои апартаменты"),
        limit: int = Query(10, description="Максимальное количество записей"),
        offset: int = Query(0, description="Смещение записей"),
        city_name: str = Query(None, description="Название города"),
        radius: float = Query(None, description="радиус в метрах"),
        latitude: float = Query(None, description="широта"),
        longitude: float = Query(None, description="долгота"),
        db: Session = Depends(get_db),
) -> PaginatedApartmentResponse:
    """
    Возвращает список ближайших квартир и сортирует по близости.
    В первую очередь по городу.
    Во вторую очередь по широте и долготе.
    Если не указать город и координаты, то вернет просто список квартир.
    """

    if my_apartments:
        apartments = crud.get_my_apartments(db, extract_email_data(request))

        return apartments

    apartments_query = ApartmentsQuery(
        limit=limit,
        offset=offset,
        city_name=city_name,
        radius=radius,
        latitude=latitude,
        longitude=longitude
    )

    apartments = crud.get_apartments(db, apartments_query)

    return PaginatedApartmentResponse(**apartments)


@app.post(
    "/apartments",
    status_code=201,
    response_model=Apartment,
    summary='Добавляет apartment в базу',
    tags=['apartments']
)
async def add_apartment(
        request: Request,
        apartment: BaseApartment,
        db: Session = Depends(get_db)
    ) -> Apartment:
    apartment_item_create = ApartmentCreate(**apartment.dict(), publisher_email=extract_email_data(request))
    return crud.add_apartment(db, apartment_item_create)


@app.patch(
    "/apartments/{apartment_id}",
    summary='Обновляет информацию об apartment',
    tags=['apartments']
)
async def update_apartment(
        request: Request,
        apartment_id: int,
        updated_item: BaseApartment,
        db: Session = Depends(get_db)
    ) -> Apartment:
    apartment_item_updated = ApartmentUpdate(**updated_item.dict(), publisher_email=extract_email_data(request))
    item = crud.update_apartment(db, apartment_id, apartment_item_updated)
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


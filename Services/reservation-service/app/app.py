from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse
from .schemas import Reservation, ReservationUpdate, ReservationCreate, PaginatedReservation
from sqlalchemy.orm import Session
from . import crud, config
import typing
import logging
from pydantic import EmailStr

from .database import DB_INITIALIZER
from . import broker
from fastapi.middleware.cors import CORSMiddleware


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

message_producer = broker.MessageProducer(
    dsn=cfg.RABBITMQ_DSN.unicode_string(),
    exchange_name=cfg.EXCHANGE_NAME,
    queue_name='notification apartment rental',
)


app = FastAPI(
    title='reservations service'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[cfg.FRONT],
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

@app.get(
    "/reservations/{reservation_id}", status_code=201, response_model=Reservation,
    summary='По айди получить Reservation',
    tags=['reservations']
)
async def get_reservation(
        reservation_id: int,
        db: Session = Depends(get_db)
    ) -> Reservation:
    item = crud.get_reservation_item(db, reservation_id)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/reservations",
    summary='Возвращает список reservations',
    response_model=PaginatedReservation,
    tags=['reservations']
)
async def get_reservations(
        user_email: EmailStr,
        limit: int = 1,
        offset: int = 0,
        db: Session = Depends(get_db)
) -> typing.List[Reservation]:
    return crud.get_reservation_items(db, user_email, limit=limit, offset=offset)


@app.post(
    "/reservations",
    status_code=201,
    response_model=Reservation,
    summary='Добавляет Reservation в базу',
    tags=['reservations']
)
async def add_reservation(
        Reservation: ReservationCreate,
        db: Session = Depends(get_db)
    ) -> Reservation:
    item = await crud.add_reservation_item(db, Reservation, message_producer)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Элемент с id {Reservation.id} уже существует в списке."})


@app.patch(
    "/reservations/{reservation_id}",
    summary='Обновляет информацию об Reservation',
    tags=['reservations']
)
async def update_reservation(
        reservation_id: int,
        updated_item: ReservationUpdate,
        db: Session = Depends(get_db)
    ) -> Reservation:
    item = crud.update_reservation_item(db, reservation_id, updated_item)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete(
    "/reservations/{reservation_id}",
    summary='Удаляет favorite item из базы',
    tags=['reservations']
)
async def delete_reservation(
        reservation_id: int,
        db: Session = Depends(get_db)
    ) -> Reservation:
    if crud.delete_reservation_item(db, reservation_id):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


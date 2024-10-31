from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse
from .schemas import Reservation, ReservationUpdate, ReservationCreate, PaginatedReservation, BaseReservation
from sqlalchemy.orm import Session
from . import crud, config
import typing
import logging
from pydantic import EmailStr
from fastapi import FastAPI, Depends, Request
import jwt
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
        request: Request,
        limit: int = 1,
        offset: int = 0,
        db: Session = Depends(get_db)
) -> typing.List[Reservation]:
    return crud.get_reservation_items(db, extract_email_data(request), limit=limit, offset=offset)


@app.post(
    "/reservations",
    status_code=201,
    response_model=Reservation,
    summary='Добавляет Reservation в базу',
    tags=['reservations']
)
async def add_reservation(
        request: Request,
        reservation: BaseReservation,
        db: Session = Depends(get_db)
    ) -> Reservation:
    reservation_item_create = ReservationCreate(**reservation.dict(), email=extract_email_data(request))
    item = await crud.add_reservation_item(db, reservation_item_create, message_producer)
    if item is not None:
        return item
    return JSONResponse(status_code=404, content={"message": f"Элемент уже существует в списке."})


# @app.patch(
#     "/reservations/{reservation_id}",
#     summary='Обновляет информацию об Reservation',
#     tags=['reservations']
# )
# async def update_reservation(
#         request: Request,
#         reservation_id: int,
#         updated_item: BaseReservation,
#         db: Session = Depends(get_db)
#     ) -> Reservation:
#     reservation_item_update = ReservationUpdate(**updated_item.dict(), email=extract_email_data(request))
#     item = crud.update_reservation_item(db, reservation_id, reservation_item_update)
#     if item is not None:
#         return item
#     return JSONResponse(status_code=404, content={"message": "Item not found"})

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


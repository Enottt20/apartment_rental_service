import typing, logging

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from . import database, config, schemas, crud

from .auth import AuthInitializer, include_routers

##===============##
## Инициализация ##
##===============##
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=20,
    format="%(levelname)-9s %(message)s"
)

logger.info("Configuration loading...")
cfg: config.Config = config.load_config()
logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.model_dump_json(by_alias=True, indent=4)}'
)

# Создание приложения FastAPI
app = FastAPI(
    version='0.0.1',
    title='User service'
)

auth = AuthInitializer()
auth.initializer(cfg.jwt_secret)

include_routers(app, auth.get_auth_backend(), auth.get_fastapi_users())


@app.on_event("startup")
async def on_startup():
    await database.DB_INITIALIZER.init_db(
        str(cfg.POSTGRES_DSN)
    )


@app.post(
    "/groups", status_code=201, response_model=schemas.GroupRead,
    summary='Создает новую группу'
)
async def add_group(
        group: schemas.GroupCreate,
        session: AsyncSession = Depends(database.get_async_session)
):
    return await crud.create_group(group, session)


@app.get(
    "/groups",
    summary='Возвращает список групп',
    response_model=list[schemas.GroupRead]
)
async def get_groups(
        session: AsyncSession = Depends(database.get_async_session),
        skip: int = 0,
        limit: int = 100
) -> typing.List[schemas.GroupRead]:
    return await crud.get_groups(session, skip, limit)


@app.get("/groups/{group_id}", summary='Возвращает информацию о группе')
async def get_group(
        group_id: int, session: AsyncSession = Depends(database.get_async_session)
) -> schemas.GroupRead:
    group = await crud.get_group(session, group_id)
    if group != None:
        return group
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.put("/groups/{group_id}", summary='Обновляет информацию о группе')
async def update_group(
        group_id: int,
        group: schemas.GroupUpdate,
        session: AsyncSession = Depends(database.get_async_session)
) -> schemas.GroupRead:
    group = await crud.update_group(session, group_id, group)
    if group != None:
        return group
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.delete("/groups/{group_id}", summary='Удаляет информацию о группе')
async def delete_group(
        group_id: int,
        session: AsyncSession = Depends(database.get_async_session)
) -> schemas.GroupRead:
    if await crud.delete_group(session, group_id):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})



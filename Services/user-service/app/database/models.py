from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, relationship

from app.database import database

class Group(database.BASE):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)


class User(SQLAlchemyBaseUserTableUUID, database.BASE):
    __table_args__ = {'schema':  database.SCHEMA}

    username = Column(String(length=128), nullable=True)
    group_id = mapped_column(ForeignKey("group.id"))
    group = relationship("Group", uselist=False)


async def get_user_db(session: AsyncSession = Depends(database.get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
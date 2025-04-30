from datetime import datetime

from sqlalchemy import Integer, ForeignKey, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


engine = create_async_engine("sqlite+aiosqlite:///tkrs.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class WellOrm(Model):
    """Модель для Скважины"""
    __tablename__ = "wells"

    id: Mapped[int] = mapped_column(primary_key=True)
    num: Mapped[int]
    name: Mapped[str]

    brig: Mapped["BrigOrm"] = relationship("BrigOrm", back_populates="well", cascade="all, delete-orphan")


class BrigOrm(Model):
    """Модель для Бригады"""
    __tablename__ = "brigs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    well_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wells.id"))  # FK на Скважину
    date_start: Mapped[datetime | None] #= mapped_column(server_default=func.now())
    date_end: Mapped[datetime | None]

    well = relationship("WellOrm", back_populates="brig")  # Отношение. Зависимость от Скважины


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

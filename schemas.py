from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SWellAdd(BaseModel):
    """Модель скважины для добавления"""
    num: int
    name: str


class SWell(SWellAdd):
    """Модель скважины"""
    id: int

    model_config = ConfigDict(from_attributes=True)


class SWellId(BaseModel):
    ok: bool = True
    well_id: int


class SBrigAdd(BaseModel):
    """Модель бригады для добавления"""
    name: str
    well_id: int | None #SWellAdd
    date_start: datetime | None
    date_end: datetime | None


class SBrig(SBrigAdd):
    """Модель бригады"""
    id: int

    model_config = ConfigDict(from_attributes=True)


class SBrigId(BaseModel):
    ok: bool = True
    brig_id: int

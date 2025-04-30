from datetime import datetime
from typing import Optional
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
    well_id: SWellAdd
    date_start: datetime
    date_end: Optional[datetime] = None


class SBrig(SBrigAdd):
    """Модель бригады"""
    id: int

    model_config = ConfigDict(from_attributes=True)


class SBrigId(BaseModel):
    ok: bool = True
    brig_id: int

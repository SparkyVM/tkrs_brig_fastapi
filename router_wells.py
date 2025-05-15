from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse
from repository import WellRepository
from schemas import SWell, SWellId, SWellAdd

router = APIRouter(
    prefix="/wells",
    tags=["Скважины"],
)


@router.post("")
async def add_well(well: Annotated[SWellAdd, Depends()],) -> SWellId:
    """Функция добавления Скважины"""
    well_id = await WellRepository.add_one(well)
    return {"ok": True, "well_id": well_id}


@router.post("/{count}")
async def add_some_wells(count: int) -> JSONResponse:
    """Функция добавления заданного кол-ва Скважин"""
    result = await WellRepository.add_some(count)
    return result


@router.get("")
async def get_wells(well_id: int = None) -> list[SWell]:
    """Функция получения списка Скважин"""
    if well_id:
        wells = await WellRepository.show_all_wells(well_id)
        return wells
    wells = await WellRepository.show_all_wells()
    return wells


@router.get("/work")
async def get_busy_wells() -> list[SWell]:
    """Функция получения списка Скважин с Бригадами"""
    wells = await WellRepository.show_busy_wells()
    return wells


@router.put("/{well_id}")
async def update_well(well_id: int, well: Annotated[SWellAdd, Depends()],) -> JSONResponse:
    """Функция изменения данных Скважины"""
    result = await WellRepository.update_well(well_id, well)
    return result

@router.delete("/{well_id}")
async def delete_well(well_id: int) -> JSONResponse:
    """Функция удаления Скважины"""
    result = await WellRepository.delete_one(well_id)
    return result

from typing import Annotated

from fastapi import APIRouter, Depends

from repository import WellRepository, BrigRepository
from schemas import SWell, SWellId, SWellAdd, SBrig, SBrigId, SBrigAdd

router = APIRouter(
    prefix="/brigs",
    tags=["Бригады"],
)


@router.post("")
async def add_brig(brig: Annotated[SBrigAdd, Depends()],) -> SBrigId:
    """Функция добавления Бригады"""
    brig_id = await BrigRepository.add_one(brig)
    return {"ok": True, "brig_id": brig_id}


@router.post("/{count}")
async def add_some_brigs(count: int) -> str:
    """Функция добавления заданного кол-ва Бригад"""
    result = await BrigRepository.add_some(count)
    return result


@router.get("")
async def get_brigs() -> list[SBrig]:
    """Функция получения списка Бригад"""
    brigs = await BrigRepository.show_all_brigs()
    return brigs


@router.put("{brig_id}")
async def update_brig(brig_id: int, brig: Annotated[SBrigAdd, Depends()],) -> dict:
    """Функция изменения данных Бригады"""
    result = await BrigRepository.update_brig(brig_id, brig)
    return {"message": result}


@router.delete("{brig_id}")
async def delete_brig(brig_id: int) -> str:
    """Функция удаления Бригады"""
    result = await BrigRepository.delete_one(brig_id)
    return result

import datetime

from sqlalchemy import select, update, delete, and_, func
from fastapi.responses import JSONResponse

from database import new_session, WellOrm, BrigOrm
from schemas import SWell, SWellAdd, SBrig, SBrigAdd
from random import choice


class WellRepository:
    """Класс для работы с моделями Скважин"""
    @classmethod
    async def add_one(cls, data: SWellAdd) -> int:
        """Функция добавления Скважины"""
        async with new_session() as session:
            well_dict = data.model_dump()

            well = WellOrm(**well_dict)
            session.add(well)
            await session.flush()
            await session.commit()
            return well.id

    @classmethod
    async def add_some(cls, count: int) -> JSONResponse:
        """Функция добавления нескольних скважин"""
        async with new_session() as session:
            if count <= 10:
                for item in range(count):
                    well = WellOrm(num=item, name=f'well_{item}')
                    session.add(well)
                    await session.flush()
                    await session.commit()
                return JSONResponse(content={"message": f"Add {count} wells"})
            else:
                return JSONResponse(content={"message": "Count must be less or equal 10"}, status_code=400)

    @classmethod
    async def show_all_wells(cls, well_id: int = None) -> list[SWell]:
        """Функция отображения всех Скважин"""
        async with new_session() as session:
            if well_id:
                query = select(WellOrm).filter_by(id=well_id)
            else:
                query = select(WellOrm)
            result = await session.execute(query)
            well_models = result.scalars().all()
            well_schemas = [SWell.model_validate(well_model) for well_model in well_models]
            return well_schemas

    @classmethod
    async def show_busy_wells(cls) -> list[SWell] | None:
        """Функция отображения всех Скважин с Бригадами"""
        async with new_session() as session:
            query = select(BrigOrm.well_id).filter(and_(BrigOrm.well_id != None), (BrigOrm.date_end == None))
            result_brig = await session.execute(query)
            brig_models = result_brig.scalars().all()
            if brig_models:
                query = select(WellOrm).where(WellOrm.id.in_(brig_models))
                result_well = await session.execute(query)
                well_models = result_well.scalars().all()
                well_schemas = [SWell.model_validate(well_model) for well_model in well_models]
                return well_schemas

    @classmethod
    async def update_well(cls, well_id: int, new_well: SWellAdd) -> JSONResponse:
        """Функция обновления Скважины """
        async with new_session() as session:
            query = select(WellOrm).filter_by(id=well_id)
            result = await session.execute(query)
            well = result.scalars().one()
            if well:
                query = update(WellOrm).values(**new_well.model_dump()).filter_by(id=well_id)
                await session.execute(query)
                await session.commit()
                return JSONResponse(content={"message": f"Updated well №{well_id}"})
            return JSONResponse(content={"message": "Well Not Found"}, status_code=404)

    @classmethod
    async def delete_one(cls, well_id: int) -> JSONResponse:
        """Функция удаления Скважины """
        async with new_session() as session:
            query = select(WellOrm).filter_by(id=well_id)
            result = await session.execute(query)
            well = result.scalars().one_or_none()
            if well:
                query = delete(WellOrm).filter_by(id=well_id)
                await session.execute(query)
                await session.commit()
                return JSONResponse(content={"message": f"Deleted well №{well_id}"})
            return JSONResponse(content={"message": "Well Not Found"}, status_code=404)

    @classmethod
    async def delete_all(cls) -> str:
        """Функция удаления всех Скважин """
        async with new_session() as session:
            query = delete(WellOrm)
            await session.execute(query)
            await session.commit()
            return f'Deleted all wells'

    @classmethod
    async def count_well(cls) -> int:
        """Функция подсчета Скважин """
        async with new_session() as session:
            query = select(func.count(WellOrm.id)).select_from(WellOrm)
            wells_count = await session.execute(query)
            return wells_count.scalar()


class BrigRepository:
    """Класс для работы с моделями Бригад"""
    @classmethod
    async def add_one(cls, data: SBrigAdd) -> int:
        """Функция добавления Бригады """
        async with new_session() as session:
            brig_dict = data.model_dump()
            brig = WellOrm(**brig_dict)
            session.add(brig)
            await session.flush()
            await session.commit()
            return brig.id


    @classmethod
    async def show_all_brigs(cls) -> list[SBrig]:
        """Функция отображения всех Бригад"""
        async with new_session() as session:
            query = select(BrigOrm)
            result = await session.execute(query)
            brig_models = result.scalars().all()
            brig_schemas = [SBrig.model_validate(brig_model) for brig_model in brig_models]
            return brig_schemas

    @classmethod
    async def update_brig(cls, brig_id: int, new_brig: SBrigAdd) -> JSONResponse:
        """Функция обновления Бригады """
        async with new_session() as session:
            query = select(BrigOrm).filter_by(id=brig_id)
            result = await session.execute(query)
            brig = result.scalars().one_or_none()
            if brig:
                query = update(BrigOrm).values(**new_brig.model_dump()).filter_by(id=brig_id)
                result = await session.execute(query)
                await session.commit()
                return JSONResponse(content={"message": f"Updated brigade №{brig_id}"})
            return JSONResponse(content={"message": "Brigade Not Found"}, status_code=404)


    @classmethod
    async def add_some(cls, count: int) -> JSONResponse:
        """Функция добавления нескольких Бригад """
        if count <= 10:
            for item in range(count):
                brig = None
                is_busy = choice([0,1])
                if is_busy == 0:
                    brig = BrigOrm(name=item)
                else:
                    random_well = None
                    async with new_session() as session:
                        query = select(WellOrm)
                        result = await session.execute(query)
                        well_list = result.scalars().all()
                        random_well = choice(well_list)
                        random_well_id = SWell.model_validate(random_well).id
                        brig = BrigOrm(name=item, well_id=random_well_id, date_start=datetime.datetime.today())
                async with new_session() as session:
                    session.add(brig)
                    await session.flush()
                    await session.commit()

            return JSONResponse(content={"message": f"Add {count} brigs"})
        else:
            return JSONResponse(content={"message": "Count must be less or equal 10"}, status_code=400)

    @classmethod
    async def delete_one(cls, brig_id: int) -> JSONResponse:
        """Функция удаления Бригады"""
        async with new_session() as session:
            query = select(BrigOrm).filter_by(id=brig_id)
            result = await session.execute(query)
            brig = result.scalars().one_or_none()
            if brig:
                query = delete(BrigOrm).filter_by(id=brig_id)
                await session.execute(query)
                await session.commit()
                return JSONResponse(content={"message": f"Deleted brigade №{brig_id}"})
            return JSONResponse(content={"message": "Brigade Not Found"}, status_code=404)

    @classmethod
    async def delete_all(cls) -> JSONResponse:
        """Функция удаления всех Бригад """
        async with new_session() as session:
            query = delete(BrigOrm)
            await session.execute(query)
            await session.commit()
            return JSONResponse(content={"message": "Deleted all brigades"})
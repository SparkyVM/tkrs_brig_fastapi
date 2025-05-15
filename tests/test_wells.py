import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from repository import WellRepository


class TestWells:
    @pytest.mark.asyncio
    async def test_add_some(self):
        """Проверка на количество добавленных скважин"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", ) as acl:
            await WellRepository.delete_all()
            response = await acl.post("/wells/2")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == 'Add 2 wells'

    @pytest.mark.asyncio
    async def test_get_wells_all(self):
        """Проверка на количество полученных скважин"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", ) as acl:
            response = await acl.get("/wells")
            assert response.status_code == 200
            data = len(response.json())
            assert data == 2

    @pytest.mark.asyncio
    async def test_get_wells_one(self):
        """Проверка на получение скважины по ID"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", ) as acl:
            response = await acl.get("/wells?well_id=1")
            assert response.status_code == 200
            data = len(response.json())
            assert data == 1
            data = response.json()[0]
            assert data["id"] == 1

    @pytest.mark.asyncio
    async def test_get_wells_data(self):
        """Проверка полей добавленной скважины"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", ) as acl:
            response = await acl.get("/wells")
            assert response.status_code == 200
            data = response.json()[0]
            assert data["id"] == 1
            assert data["num"] == 0
            assert data["name"] == "well_0"

    @pytest.mark.asyncio
    async def test_delete_well(self):
        """Проверка удаления скважины"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", ) as acl:
            response = await acl.delete("/wells/1")
            assert response.status_code == 200
            response = await acl.get("/wells")
            assert response.status_code == 200
            len_data = len(response.json())
            assert len_data == 1
            data = response.json()[0]
            assert data["id"] == 2
            assert data["num"] == 1
            assert data["name"] == "well_1"

    @pytest.mark.asyncio
    async def test_add_one(self):
        """Проверка на добавление скважины"""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", ) as acl:
            response = await acl.post("/wells?num=5&name=test_well")
            assert response.status_code == 200
            response = await acl.get("/wells?well_id=3")
            data = response.json()[0]
            assert data["num"] == 5
            assert data["name"] == "test_well"

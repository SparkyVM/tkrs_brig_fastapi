import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables, delete_tables
from router_wells import router as well_router
from router_brigs import router as brig_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #await delete_tables()
    #print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(well_router)
app.include_router(brig_router)


if __name__ == "__main__":
    uvicorn.run("main:app")
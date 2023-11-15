from contextlib import asynccontextmanager

from fastapi import FastAPI

from .repository import ListRepository
from .router import router, set_repository


@asynccontextmanager
async def init_app(app: FastAPI):
    repo = ListRepository()
    set_repository(repo)
    yield


app = FastAPI(lifespan=init_app)

app.include_router(router=router)

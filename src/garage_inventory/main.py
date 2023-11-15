from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base, DatabaseRepository
from .router import router, set_repository


@asynccontextmanager
async def init_app(app: FastAPI):
    engine = create_engine("sqlite://///home/daniel/dev/python/garage-inventory/my.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    repo = DatabaseRepository(Session)
    set_repository(repo)
    yield


app = FastAPI(lifespan=init_app)

app.include_router(router=router)

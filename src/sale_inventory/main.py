from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .database import Base, DatabaseRepository
from .router import router, set_repository


@asynccontextmanager
async def init_app(app: FastAPI):
    engine = create_engine("sqlite:///my.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    repo = DatabaseRepository(Session)
    set_repository(repo)
    yield


app = FastAPI(lifespan=init_app)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(router=router)

app.mount("/", StaticFiles(directory="inventory-frontend/build", html=True), name="frontend")

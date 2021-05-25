from fastapi import FastAPI
from . import models
from .database import engine
from app.routers import message

app = FastAPI()

models.Message.__table__.drop(engine)

models.Base.metadata.create_all(bind=engine)

app.include_router(message.router)

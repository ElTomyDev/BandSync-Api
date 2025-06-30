from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_mongo_database, close_mongo_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta antes de que inicie la API
    await connect_mongo_database()
    yield
    # Esto se ejecuta antes de que se cierre la API
    await close_mongo_database()

app = FastAPI(title="BandSync API", lifespan=lifespan)



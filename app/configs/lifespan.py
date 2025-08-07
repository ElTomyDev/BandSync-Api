from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import connect_mongo_database, close_mongo_database, db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Funcion asincronica que gestina el ciclo de vida de la aplicacion, se ejecuta una vez al inicio
    y una vez al final.
    """
    # Esto se ejecuta durante el inicio de la app
    await connect_mongo_database(app) # Espera a conectar la base de datos de MongoDB
    yield
    # Esto se ejecuta durante el cierre de la app
    await close_mongo_database() # Espera a desconectar la base de datos de MongoDB
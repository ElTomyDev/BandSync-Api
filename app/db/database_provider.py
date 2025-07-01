from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase

def get_mongo_db(request: Request) -> AsyncIOMotorDatabase:
    """
    Retorna una instancia de la base de datos guardada anteriormente al momento de conectarla
    """
    return request.app.state.db
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .configs.db_config import MONGO_URI, MONGO_DB_NAME

client: AsyncIOMotorClient | None = None # Futura instancia del cliente de mongo
db: AsyncIOMotorDatabase | None = None # Futura representacion de la base de datos

async def connect_mongo_database() -> None:
    """
    Funcion asincronica que se encarga de establecer la conexion con el cliente de Mongo y obtener
    guardar una referencia de la base de datos en `db`
    """
    global client, db # Se utilizan las variables globales declaradas arriba
    client = AsyncIOMotorClient(MONGO_URI) # Crea una nueva instancia del cliente de Mongo
    db = client[MONGO_DB_NAME] # Obtiene una referencia a la base de datos especificada en [MONGO_DB_NAME]
    try:
        await db.command("ping") # Prueba si la conexion esta activa con un 'Ping'
        print("Base de Datos conectada.")
    except Exception as e:
        print("Error al conectar con la Base de Datos:", e)

async def close_mongo_database() -> None:
    """
    Funcion asincronica que se encarga de desconectar el cliente de Mongo. Cerrando asi, la conexion
    con la base de datos.
    """
    global client # Se utiliza la variable global 'client' declarada arriba
    if client:
        client.close() # Cierra la coneccion con el ciente de Mongo.
        print("La conexion con la Base de Datos fue desconectada.")


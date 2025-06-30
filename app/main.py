from fastapi import FastAPI
from app.configs.lifespan import lifespan

app = FastAPI(title="BandSync API", lifespan=lifespan)




from fastapi import FastAPI
from app.features.users.route import user_router
from app.configs.lifespan import lifespan

app = FastAPI(title="BandSync API", lifespan=lifespan)


app.include_router(user_router)


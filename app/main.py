from fastapi import FastAPI
from app.routes.user_route import UserRoute
from app.configs.lifespan import lifespan

app = FastAPI(title="BandSync API", lifespan=lifespan)

user_route = UserRoute()
app.include_router(user_route.router)


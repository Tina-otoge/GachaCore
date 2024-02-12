from fastapi import FastAPI

from modules.azur_lane.api import router

app = FastAPI()
app.include_router(router, prefix="/azur_lane")

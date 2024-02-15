from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from gacha.webui import webui
from modules.azur_lane.api import router

app = FastAPI()
app.include_router(router, prefix="/azur_lane")
app.mount("/", WSGIMiddleware(webui))

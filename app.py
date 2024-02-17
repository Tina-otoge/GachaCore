import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from gachacore.webui import webui
from plugins.azur_lane.api import router

app = FastAPI()
app.include_router(router, prefix="/azur_lane")
app.mount("/", WSGIMiddleware(webui))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_includes=["*.j2"],
    )

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import base_path
from .routers import api
from .routers import web

app = FastAPI()

app.mount('/', web.router)
app.mount('/api', api.router)

app.mount('/static', StaticFiles(
    directory=base_path / 'static'), name='static')

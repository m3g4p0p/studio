from fastapi import FastAPI

from .routers import api
from .routers import web

app = FastAPI()

app.mount('/', web.router)
app.mount('/api', api.router)

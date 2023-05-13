
from urllib.error import HTTPError

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import PlainTextResponse

from .routers import api
from .routers import web

app = FastAPI()

app.mount('/', web.router)
app.mount('/api', api.router)


@app.exception_handler(HTTPError)
def handle_http_error(request: Request, exc: HTTPError):
    return PlainTextResponse(f'{exc.reason} 💀', exc.code)

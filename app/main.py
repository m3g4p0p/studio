from urllib.error import HTTPError

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from .handlers import handle_http_error
from .handlers import handle_http_exception
from .handlers import handle_unprocessable_entity
from .routers import api
from .routers import web

app = FastAPI()

app.mount('/api', api.router)
app.mount('/', web.router)

app.add_exception_handler(HTTPError, handle_http_error)
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_unprocessable_entity)


@app.exception_handler(IntegrityError)
def handle_integrity_error(request, exc):
    raise HTTPException(409)


from urllib.error import HTTPError

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .handlers import handle_http_error
from .handlers import handle_http_exception
from .handlers import handle_unprocessable_entity
from .routers import api
from .routers import web

app = FastAPI()

app.mount('/', web.router)
app.mount('/api', api.router)

app.add_exception_handler(HTTPError, handle_http_error)
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_unprocessable_entity)

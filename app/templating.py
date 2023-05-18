import os

from fastapi import Request
from fastapi.templating import Jinja2Templates

from . import base_path


def env_context(request: Request):
    return {'env': os.environ}


templates = Jinja2Templates(
    directory=base_path / 'templates',
    context_processors=[env_context],
)

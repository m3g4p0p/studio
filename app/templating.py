import os
from calendar import day_name
from datetime import date

from fastapi import Request
from fastapi.templating import Jinja2Templates

from . import base_path


def env_context(request: Request):
    return {'env': os.environ}


def route_context(request: Request):
    if 'route' not in request.scope:
        return {'route': ''}

    return {'route': request.scope['route'].name}


def date_context(request: Request):
    return {'today': date.today(), 'day_name': day_name}


def version_context(request: Request):
    return {'version': os.getenv(
        'DETA_SPACE_APP_VERSION', str(date.today()),
    )}


templates = Jinja2Templates(
    directory=base_path / 'templates',
    context_processors=[
        env_context,
        route_context,
        date_context,
        version_context,
    ],
)

import os
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


def today_context(request: Request):
    return {'today': date.today()}


templates = Jinja2Templates(
    directory=base_path / 'templates',
    context_processors=[
        env_context,
        route_context,
        today_context,
    ],
)

templates.env.filters['strftime'] = date.strftime

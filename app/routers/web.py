import typing as t
from calendar import Calendar
from calendar import day_name
from datetime import date

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .. import base_path
from ..dependencies import Reservation
from ..dependencies import db

router = APIRouter(default_response_class=HTMLResponse)
templates = Jinja2Templates(directory=base_path / 'templates')


router.mount('/static', StaticFiles(
    directory=base_path / 'static'), name='static',
)


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.jinja', {
        'request': request,
    })


@router.get('/calendar')
async def calendar(
    request: Request,
    year: t.Optional[int] = None,
    month: t.Optional[int] = None,
):
    today = date.today()

    reservations = dict(map(
        Reservation.from_item, db.fetch().items),
    )

    return templates.TemplateResponse('calendar.jinja', {
        'request': request,
        'today': today,
        'month': month or today.month,
        'year': year or today.year,
        'day_name': day_name,
        'calendar': Calendar(),
        'reservations': reservations,
    })

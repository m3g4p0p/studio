from calendar import Calendar
from calendar import day_name
from datetime import date

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .. import base_path
from ..dependencies import Reservation
from ..dependencies import db

router = APIRouter(default_response_class=HTMLResponse)
templates = Jinja2Templates(directory=base_path / 'templates')


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.jinja', {
        'request': request,
    })


@router.get('/calendar')
async def calendar(request: Request):
    today = date.today()

    return templates.TemplateResponse('calendar.jinja', {
        'request': request,
        'today': today,
        'reservations': list(map(
            Reservation.from_dict, db.fetch().items,
        )),
        'calendar': Calendar().monthdatescalendar(
            today.year, today.month,
        ),
        'day_name': day_name,
    })

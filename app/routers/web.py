import enum
from calendar import Calendar
from calendar import day_name
from datetime import date as pydate

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .. import base_path
from ..dependencies import CalendarMonth
from ..dependencies import Reservation
from ..dependencies import db


class Action(str, enum.Enum):

    PUT = 'put'
    DELETE = 'delete'
    CANCEL = 'cancel'


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
async def calendar_today(request: Request):
    today = pydate.today()

    return RedirectResponse(request.url_for(
        'calendar', year=today.year, month=today.month,
    ))


@router.get('/calendar/{year}/{month}')
async def calendar(
    request: Request,
    current: CalendarMonth = Depends(),
):
    today = pydate.today()

    reservations = dict(map(
        Reservation.as_pair, db.fetch().items),
    )

    return templates.TemplateResponse('calendar.jinja', {
        'request': request,
        'today': today,
        'current': current,
        'day_name': day_name,
        'calendar': Calendar(),
        'reservations': reservations,
    })


@router.get('/reservation/{date}')
async def get_form(
    request: Request,
    reservation: Reservation = Depends(Reservation.get),
):
    return templates.TemplateResponse('form.jinja', {
        'request': request,
        'reservation': reservation,
    })


@router.post('/reservation/{date}')
async def post_form(
    request: Request,
    date: pydate,
    action: Action = Form(),
    reservation: Reservation = Depends(Reservation.form),
):
    redirect_date = date

    if action is Action.PUT and reservation.band:
        data = jsonable_encoder(reservation)
        key = str(reservation.date)
        redirect_date = reservation.date

        if date != reservation.date:
            db.insert(data, key)
        else:
            db.put(data, key)

    if action is Action.DELETE or \
            not reservation.band or \
            date != reservation.date:
        db.delete(key=str(date))

    return RedirectResponse(request.url_for(
        'calendar',
        year=redirect_date.year,
        month=redirect_date.month,
    ), status_code=302)

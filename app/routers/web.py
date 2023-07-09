import enum
import typing as t
from calendar import IllegalMonthError
from datetime import date as pydate

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Query
from fastapi import Request
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .. import base_path
from ..auth import authenticate
from ..dependencies import CalendarMonth
from ..dependencies import Reservation
from ..dependencies import db
from ..patches import PatchedRoute
from ..templating import templates


class Action(str, enum.Enum):

    PUT = 'put'
    DELETE = 'delete'
    CANCEL = 'cancel'


router = APIRouter(
    route_class=PatchedRoute,
    default_response_class=HTMLResponse,
    dependencies=[Depends(authenticate)],
)

router.mount('/static', StaticFiles(
    directory=base_path / 'static'), name='static',
)


@router.get('/')
def index(
    request: Request,
    limit: int = Query(default=10, ge=0, le=20),
):
    query = jsonable_encoder({
        'date?gte': pydate.today(),
    })

    reservations = map(
        Reservation.parse_obj,
        db.fetch(query, limit=limit).items,
    )

    return templates.TemplateResponse('index.jinja', {
        'request': request,
        'reservations': reservations,
    })


@router.get('/calendar')
async def calendar_today(request: Request):
    today = pydate.today()

    return RedirectResponse(request.url_for(
        'calendar', year=today.year, month=today.month,
    ))


@router.get('/calendar/{date}')
async def calendar_date(request: Request, date: pydate):
    return RedirectResponse(request.url_for(
        'calendar', year=date.year, month=date.month,
    ).include_query_params(highlight=date.day))


@router.get('/calendar/{year}/{month}')
async def calendar(
    request: Request,
    current: CalendarMonth = Depends(),
    highlight: t.Optional[int] = None,
):
    try:
        month_dates = current.month_dates()
    except IllegalMonthError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e)

    query = jsonable_encoder({
        'date?gte': month_dates[0][0],
        'date?lte': month_dates[-1][-1],
    })

    reservations = dict(map(
        Reservation.by_date,
        db.fetch(query).items,
    ))

    return templates.TemplateResponse('calendar.jinja', {
        'request': request,
        'current': current,
        'highlight': highlight,
        'month_dates': month_dates,
        'reservations': reservations,
    })


@router.get('/reservation/{date}', name='reservation')
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
    reservation: Reservation = Depends(Reservation.from_form),
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
        db.delete(key=reservation.key)

    return RedirectResponse(request.url_for(
        'calendar',
        year=redirect_date.year,
        month=redirect_date.month,
    ), status_code=302)


@router.get('/inspect')
async def inspect(request: Request):
    return templates.TemplateResponse('inspect.jinja', {
        'request': request,
    })

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
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .. import base_path
from ..auth import authenticate
from ..crud import CRUDUtil
from ..dependencies import CalendarMonth
from ..dependencies import Reservation
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
async def index(
    request: Request,
    crud: t.Annotated[CRUDUtil, Depends()],
    limit: t.Annotated[int, Query(ge=0, le=20)] = 10,
):
    result = await crud.get_from_date(pydate.today(), limit)
    reservations = map(Reservation.model_validate, result)

    return templates.TemplateResponse(request, 'index.jinja', {
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
    crud: t.Annotated[CRUDUtil, Depends()],
    current: t.Annotated[CalendarMonth, Depends()],
    highlight: t.Optional[int] = None,
):
    try:
        month_dates = current.month_dates()
    except IllegalMonthError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, e)

    result = await crud.get_in_date_range(
        from_date=month_dates[0][0],
        to_date=month_dates[-1][-1],
    )

    reservations = dict(map(
        Reservation.by_date, result,
    ))

    return templates.TemplateResponse(request, 'calendar.jinja', {
        'current': current,
        'highlight': highlight,
        'month_dates': month_dates,
        'reservations': reservations,
    })


@router.get('/reservation/{date}', name='reservation')
async def get_form(
    request: Request,
    crud: t.Annotated[CRUDUtil, Depends()],
    date: pydate,
):
    result = await crud.get_for_date(date)

    if result is None:
        reservation = Reservation(date=date)
    else:
        reservation = Reservation.model_validate(result)

    return templates.TemplateResponse(request, 'form.jinja', {
        'reservation': reservation,
    })


@router.post('/reservation/{date}')
async def post_form(
    request: Request,
    crud: t.Annotated[CRUDUtil, Depends()],
    action: t.Annotated[Action, Form()],
    reservation: t.Annotated[
        Reservation, Depends(Reservation.from_form)],
):
    if action is Action.PUT and reservation.band:
        if reservation.id is None:
            await crud.insert(reservation)
        else:
            await crud.update(reservation)

    if action is Action.DELETE or not reservation.band:
        await crud.delete(reservation)

    return RedirectResponse(request.url_for(
        'calendar',
        year=reservation.date.year,
        month=reservation.date.month,
    ), status_code=302)


@router.get('/inspect')
async def inspect(request: Request):
    return templates.TemplateResponse(request, 'inspect.jinja')

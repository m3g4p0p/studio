from datetime import date
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_409_CONFLICT

from ..crud import CRUD
from ..dependencies import Reservation

router = APIRouter()


@router.get('/dates/', response_model=list[Reservation])
async def get_reservations(crud: Annotated[CRUD, Depends()]):
    return await crud.get_from_date(date.today())


@router.post('/dates/', response_model=Reservation)
async def create_reservation(
    item: Reservation,
    crud: Annotated[CRUD, Depends()],
):
    try:
        return await crud.insert(item)
    except IntegrityError as e:
        raise HTTPException(HTTP_409_CONFLICT, str(e.orig))

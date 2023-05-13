from datetime import date
from urllib.error import HTTPError

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from ..dependencies import Reservation
from ..dependencies import db

router = APIRouter()


@router.get('/dates/')
def get_reservations():
    today = date.today().isoformat()
    return db.fetch({'date?gte': today}).items


@router.post('/dates/')
def create_reservation(item: Reservation):
    try:
        return db.insert(jsonable_encoder(item), str(item.date))
    except HTTPError as e:
        raise HTTPException(e.code, f'{e.reason} 💀')

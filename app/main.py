from datetime import date
from urllib.error import HTTPError

from deta import Deta
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()
deta = Deta()
db = deta.Base('reservations')


class Reservation(BaseModel):

    band: str
    date: date


@app.get("/")
def root():
    return "Space 🚀 Fuck"


@app.get('/dates/')
def get_reservations():
    today = date.today().isoformat()
    return db.fetch({'date?gte': today}).items


@app.post('/dates/')
def create_reservation(item: Reservation):
    try:
        return db.insert(jsonable_encoder(item), str(item.date))
    except HTTPError as e:
        raise HTTPException(e.code, f'{e.reason} 💀')

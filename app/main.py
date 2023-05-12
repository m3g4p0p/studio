from datetime import date

from deta import Deta
from fastapi import FastAPI
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
    return "Hello from Space! 🚀"


@app.post('/dates/')
def create_reservation(item: Reservation):
    db.insert(jsonable_encoder(item))

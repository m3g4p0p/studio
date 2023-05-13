from datetime import date

from deta import Deta
from pydantic import BaseModel

deta = Deta()
db = deta.Base('reservations')


class Reservation(BaseModel):

    band: str
    date: date

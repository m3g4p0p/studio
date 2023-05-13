import typing as t
from datetime import date

from deta import Deta
from pydantic import BaseModel

deta = Deta()
db = deta.Base('reservations')


class Reservation(BaseModel):

    band: str
    date: date
    key: t.Optional[str] = None

    @classmethod
    def from_item(cls, kwargs):
        instance = cls(**kwargs)
        return instance.date, instance

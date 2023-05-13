import typing as t
from datetime import date as pydate

from deta import Deta
from pydantic import BaseModel

deta = Deta()
db = deta.Base('reservations')


class Reservation(BaseModel):

    date: pydate
    band: str = ''
    key: t.Optional[str] = None

    @classmethod
    def from_item(cls, item):
        return cls(**item)

    @classmethod
    def as_pair(cls, item):
        instance = cls.from_item(item)
        return instance.date, instance

    @classmethod
    def fetch(cls, date: pydate):
        items = db.fetch({
            'date': str(date),
        }).items

        if not items:
            return cls(date=date)

        return cls.from_item(items[-1])

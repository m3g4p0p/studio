import os
import typing as t
from calendar import Calendar
from datetime import date as pydate
from datetime import time

from deta import Deta
from fastapi import Request
from pydantic import BaseModel
from pydantic import validator

from .util import parse_mapping

deta = Deta()
name = os.getenv('DETA_BASE_NAME', 'reservations')
db = deta.Base(name)


class TimeFrame(BaseModel):

    start: t.Optional[time] = None
    end: t.Optional[time] = None

    @validator('start', 'end', pre=True)
    def to_none(cls, value):
        return value or None


class Reservation(BaseModel):

    date: pydate
    time: TimeFrame = TimeFrame()

    band: str = ''
    key: str = ''

    @validator('key', always=True)
    def key_from_date(cls, value, values):
        return value or values['date']

    @validator('band', always=True)
    def strip_band(cls, value: str):
        return value.strip()

    @classmethod
    async def from_form(cls, request: Request):
        form = await request.form()
        data = parse_mapping(form)

        return cls.parse_obj(data)

    @classmethod
    def by_date(cls, data):
        instance = cls.parse_obj(data)
        return instance.date, instance

    @classmethod
    def get(cls, date: pydate):
        item = db.get(key=str(date))

        if not item:
            return cls(date=date)

        return cls.parse_obj(item)

    def split_bands(self):
        return self.band.encode().decode(
            'unicode_escape',
        ).splitlines()


class CalendarMonth(t.NamedTuple):

    year: int
    month: int

    def __add__(self, value: int):
        month = self.month + value

        return self._replace(
            year=self.year + (month - 1) // 12,
            month=month % 12 or 12,
        )

    def __sub__(self, value: int):
        return self.__add__(-value)

    def __str__(self) -> str:
        return f'{self.year}-{self.month:02}'

    def month_dates(self):
        return Calendar().monthdatescalendar(
            self.year, self.month,
        )

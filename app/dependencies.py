import os
import typing as t
from calendar import Calendar
from datetime import date as pydate

from deta import Deta
from fastapi import Request
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator

deta = Deta()
name = os.getenv('DETA_BASE_NAME', 'reservations')
db = deta.Base(name)


class Reservation(BaseModel):

    date: pydate
    band: str = ''
    key: str = ''
    id: t.Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

    @field_validator('band')
    def validate_band(cls, value: str):
        return value.strip()

    @classmethod
    async def from_form(cls, request: Request):
        data = dict(await request.form())
        return cls.model_validate(data)

    @classmethod
    def by_date(cls, data):
        instance = cls.model_validate(data)
        return instance.date, instance

    @classmethod
    def get(cls, date: pydate):
        item = db.get(key=str(date))

        if not item:
            return cls(date=date)

        return cls.model_validate(item)

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

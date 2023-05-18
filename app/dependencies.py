import typing as t
from datetime import date as pydate

from deta import Deta
from fastapi import Request
from pydantic import BaseModel
from pydantic import validator

deta = Deta()
db = deta.Base('reservations')


class Reservation(BaseModel):

    date: pydate
    band: str = ''
    key: t.Optional[str] = None

    @validator('band', always=True)
    def strip_band(cls, value: str):
        return value.strip()

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def as_pair(cls, data):
        instance = cls.from_dict(data)
        return instance.date, instance

    @classmethod
    def get(cls, date: pydate):
        item = db.get(key=str(date))

        if not item:
            return cls(date=date)

        return cls.from_dict(item)

    @classmethod
    async def form(cls, request: Request):
        data = dict(await request.form())
        return cls.from_dict(data)


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

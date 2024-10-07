from dataclasses import dataclass
from datetime import date as pydate
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .dependencies import Reservation as ReservationModel
from .models import Reservation


@dataclass
class CRUD:

    session: Annotated[AsyncSession, Depends(get_db)]

    def get_for_date(self, date: pydate):
        query = select(Reservation).filter(
            Reservation.date == date
        )

        return self.session.scalar(query)

    def get_from_date(self, date: pydate, limit: int = 10):
        query = select(Reservation).filter(
            Reservation.date >= date
        ).order_by(Reservation.date).limit(limit)

        return self.session.scalars(query)

    def get_by_date(self, from_date: pydate, to_date: pydate):
        query = select(Reservation).filter(
            Reservation.date >= from_date,
            Reservation.date <= to_date,
        )

        return self.session.scalars(query)

    async def insert(self, model: ReservationModel):
        reservation = Reservation(
            band=model.band,
            date=model.date,
        )

        self.session.add(reservation)
        await self.session.flush()
        await self.session.refresh(reservation)

        return reservation

    def update(self, model: ReservationModel):
        query = update(Reservation).where(
            Reservation.id == model.id
        ).values(model.model_dump())

        return self.session.execute(query)

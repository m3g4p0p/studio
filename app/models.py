from datetime import date as pydate

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Reservation(Base):

    __tablename__ = 'reservation'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[pydate] = mapped_column(unique=True)
    band: Mapped[str]

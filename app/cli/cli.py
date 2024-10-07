from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import FileType
from datetime import date as pydate
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import TypeAdapter
from pydantic import ValidationError
from rich.console import Console

from app.database import async_session
from app.database import engine
from app.models import Base
from app.models import Reservation


class ReservationImport(BaseModel):

    band: str
    date: pydate


class ParserModel(BaseModel):

    drop: bool
    json: Optional[list[ReservationImport]]
    model_config = ConfigDict(from_attributes=True)


class JSONType(FileType):

    adapter = TypeAdapter(list[ReservationImport])

    def __call__(self, string: str):
        file = super().__call__(string)

        try:
            return self.adapter.validate_json(file.read())
        except ValidationError as e:
            raise ArgumentTypeError(e)


parser = ArgumentParser()
parser.add_argument('--json', type=JSONType())
parser.add_argument('--drop', action='store_true')


async def main():
    args = ParserModel.model_validate(
        parser.parse_args())
    console = Console(highlight=True)

    async with engine.begin() as conn:
        if args.drop:
            await conn.run_sync(Base.metadata.drop_all)

        await conn.run_sync(Base.metadata.create_all)

    if not args.json:
        return

    async with async_session() as session:
        for model in args.json:
            reservation = Reservation(
                date=model.date,
                band=model.band,
            )

            session.add(reservation)
            console.print(f'{reservation.date} {reservation.band}')

        await session.commit()

from pathlib import Path
from textwrap import indent

from pydantic import TypeAdapter
from pydantic import ValidationInfo
from pydantic import field_validator
from sqlalchemy import select

from app.cli.commands.base import BaseCommand
from app.database import async_session
from app.dependencies import Reservation as ReservationModel
from app.models import Reservation


class ExportCommand(BaseCommand):

    force: bool = False
    filename: Path

    @field_validator('filename')
    def validate_filename(cls, value: Path, info: ValidationInfo):
        if value.is_dir():
            raise ValueError('is a directory')

        if value.exists() and not info.data['force']:
            raise ValueError('exists')

        return value

    async def invoke(self):
        query = select(Reservation)

        async with async_session() as session:
            result = await session.scalars(query)

        adapter = TypeAdapter(list[ReservationModel])
        reservations = adapter.validate_python(result)

        for reservation in reservations:
            self.console.print(reservation)

        json_data = adapter.dump_json(reservations, indent=2)
        self.filename.write_bytes(json_data)

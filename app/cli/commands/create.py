import json
from datetime import date as pydate
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import FilePath
from pydantic import ValidationInfo
from pydantic import field_validator

from app.cli.commands.base import BaseCommand
from app.database import async_session
from app.database import engine
from app.models import Base
from app.models import Reservation


class ReservationImport(BaseModel):

    band: str
    date: pydate


class CreateCommand(BaseCommand):

    drop: bool = False
    jsonfile: Optional[FilePath] = None

    import_data: Optional[list[ReservationImport]] = Field(
        init=False, default=None, validate_default=True,
    )

    @field_validator('import_data', mode='before')
    def read_import_data(cls, _, info: ValidationInfo):
        file_path = info.data['jsonfile']

        if file_path is None:
            return None

        with open(file_path) as f:
            return json.load(f)

    async def invoke(self):
        async with engine.begin() as conn:
            if self.drop:
                await conn.run_sync(Base.metadata.drop_all)

            await conn.run_sync(Base.metadata.create_all)

        if not self.import_data:
            return

        async with async_session() as session:
            for model in self.import_data:
                reservation = Reservation(
                    date=model.date,
                    band=model.band,
                )

                session.add(reservation)

                self.console.print(
                    f'{reservation.date} {reservation.band}')

            await session.commit()

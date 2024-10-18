from argparse import ArgumentParser
from datetime import date as pydate
from typing import Optional

from pydantic import BaseModel
from pydantic import FilePath
from pydantic import TypeAdapter
from pydantic_settings import BaseSettings
from pydantic_settings import CliSettingsSource
from pydantic_settings import CliSubCommand
from pydantic_settings import get_subcommand
from rich.console import Console

from app.database import async_session
from app.database import engine
from app.models import Base
from app.models import Reservation


class ReservationImport(BaseModel):

    band: str
    date: pydate


class BaseCommand(BaseModel):

    async def invoke(self):
        raise NotImplementedError


class CreateCommand(BaseCommand):

    drop: bool = False
    jsonfile: Optional[FilePath] = None

    async def invoke(self):
        async with engine.begin() as conn:
            if self.drop:
                await conn.run_sync(Base.metadata.drop_all)

            await conn.run_sync(Base.metadata.create_all)

        if not self.jsonfile:
            return

        adapter = TypeAdapter(list[ReservationImport])

        with open(self.jsonfile) as f:
            data = adapter.validate_json(f.read())

        async with async_session() as session:
            for model in data:
                reservation = Reservation(
                    date=model.date,
                    band=model.band,
                )

                session.add(reservation)
                console.print(f'{reservation.date} {reservation.band}')

            await session.commit()


class CliSettings(BaseSettings):

    create: CliSubCommand[CreateCommand]


console = Console(highlight=True)
parser = ArgumentParser()

source = CliSettingsSource(
    CliSettings,
    root_parser=parser,
    cli_implicit_flags=True,
)


async def main():
    args = parser.parse_args()

    model = source.settings_cls(
        _cli_settings_source=source(parsed_args=args),
    )

    command: BaseCommand = get_subcommand(model)
    await command.invoke()

from argparse import ArgumentParser

from pydantic_settings import BaseSettings
from pydantic_settings import CliSettingsSource
from pydantic_settings import CliSubCommand
from pydantic_settings import get_subcommand

from app.cli.commands.base import BaseCommand
from app.cli.commands.create import CreateCommand
from app.cli.commands.export import ExportCommand


class CliSettings(BaseSettings):

    create: CliSubCommand[CreateCommand]
    export: CliSubCommand[ExportCommand]


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

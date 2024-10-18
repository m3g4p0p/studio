from pathlib import Path

from pydantic import ValidationInfo
from pydantic import field_validator

from app.cli.commands.base import BaseCommand


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

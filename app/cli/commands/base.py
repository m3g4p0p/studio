from typing import ClassVar

from pydantic import BaseModel
from rich.console import Console


class BaseCommand(BaseModel):

    console: ClassVar = Console(highlight=True)

    async def invoke(self):
        raise NotImplementedError

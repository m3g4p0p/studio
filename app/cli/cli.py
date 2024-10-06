import json
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import FileType
from datetime import date as pydate

from pydantic import BaseModel
from pydantic import TypeAdapter
from pydantic import ValidationError


class Reservation(BaseModel):

    band: str
    date: pydate


ReservationList = TypeAdapter(list[Reservation])


class JSONType(FileType):

    def __call__(self, string: str):
        file = super().__call__(string)

        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ArgumentTypeError(*e.args)

        try:
            return ReservationList.validate_python(data)
        except ValidationError as e:
            raise ArgumentTypeError(e)


parser = ArgumentParser()
parser.add_argument('--json', type=JSONType())
parser.add_argument('--drop', action='store_true')


async def main():
    args_ = parser.parse_args()
    return args_

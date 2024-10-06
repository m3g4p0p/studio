import json
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from argparse import FileType


class JSONType(FileType):

    def __call__(self, string: str):
        file = super().__call__(string)

        try:
            return json.load(file)
        except json.JSONDecodeError as e:
            raise ArgumentTypeError(*e.args)


parser = ArgumentParser()
parser.add_argument('--json', type=JSONType())
parser.add_argument('--drop', action='store_true')


async def main():
    args_ = parser.parse_args()
    return args_

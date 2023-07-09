import datetime
import typing as t
import urllib.parse
from functools import reduce


def with_query(url: str, **query_params):
    query = urllib.parse.urlencode(query_params)
    split_result = urllib.parse.urlsplit(url)
    query_index = split_result._fields.index('query')
    parts = list(split_result)
    parts[query_index] = query

    return urllib.parse.urlunsplit(parts)


def update_month(date: datetime.date, delta: int):
    new_month = date.month + delta

    return date.replace(
        year=date.year + new_month // 12,
        month=new_month % 12,
    )


def init_dict(data: dict, key: str):
    return data.setdefault(key, {})


def set_item(data: dict, item: tuple[str, str]):
    key, value = item
    path = key.split('.')
    target_key = path.pop()
    target = reduce(init_dict, path, data)
    target[target_key] = value

    return data


def parse_mapping(mapping: t.Mapping):
    return reduce(set_item, mapping.items(), {})

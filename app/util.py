import datetime
import urllib.parse


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

import urllib.parse


def with_query(url: str, **query_params):
    query = urllib.parse.urlencode(query_params)
    split_result = urllib.parse.urlsplit(url)
    query_index = split_result._fields.index('query')
    parts = list(split_result)
    parts[query_index] = query

    return urllib.parse.urlunsplit(parts)

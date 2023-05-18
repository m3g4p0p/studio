import typing as t
from functools import update_wrapper
from urllib.error import HTTPError

from fastapi import Request
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException

from .templating import templates


def html_only(handler: t.Callable):
    async def wrapper(request: Request, exc: Exception):
        if 'text/html' in request.headers.get('accept', '').split(','):
            return handler(request, exc)

        if isinstance(exc, HTTPException):
            return await http_exception_handler(request, exc)

        raise exc

    return update_wrapper(wrapper, handler)


@html_only
def handle_http_error(request: Request, exc: HTTPError):
    return templates.TemplateResponse('error.jinja', {
        'request': request,
        'reason': exc.reason,
    }, exc.code)


@html_only
def handle_http_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse('error.jinja', {
        'request': request,
        'reason': exc.detail,
    }, exc.status_code, exc.headers)

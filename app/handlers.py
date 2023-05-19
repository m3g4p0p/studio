import typing as t
from functools import update_wrapper
from http import HTTPStatus
from urllib.error import HTTPError

from fastapi import Request
from fastapi import status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .patches import PatchedRequest
from .templating import templates


def html_only(handler: t.Callable):
    async def wrapper(request: Request, exc: Exception):
        if 'text/html' in request.headers.get('accept', '').split(','):
            return handler(request, exc)

        if isinstance(exc, HTTPException):
            return await http_exception_handler(request, exc)

        if isinstance(exc, RequestValidationError):
            return await request_validation_exception_handler(request, exc)

        raise exc

    return update_wrapper(wrapper, handler)


def patch(request: Request):
    return PatchedRequest(request.scope, request.receive)


def reason(code: int):
    return HTTPStatus(code).phrase


@html_only
def handle_http_error(request: Request, exc: HTTPError):
    return templates.TemplateResponse('error.jinja', {
        'request': patch(request),
        'reason': exc.reason,
    }, exc.code)


@html_only
def handle_http_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse('error.jinja', {
        'request': patch(request),
        'reason': reason(exc.status_code),
        'errors': [exc.detail],
    }, exc.status_code, exc.headers)


@html_only
def handle_unprocessable_entity(
        request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    return templates.TemplateResponse('error.jinja', {
        'request': patch(request),
        'reason': reason(status_code),
        'errors': exc.errors(),
    }, status_code)

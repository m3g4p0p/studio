import typing as t
from functools import update_wrapper
from http import HTTPStatus
from urllib.error import HTTPError

from fastapi import Request
from fastapi import status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
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


def render_error(request, status_code, headers=None, **context):
    return templates.TemplateResponse('error.jinja', {
        'request': patch(request),
        'reason': reason(status_code),
        **context,
    }, status_code, headers)


@html_only
def handle_http_error(request: Request, exc: HTTPError):
    return render_error(request, exc.code, reason=exc.reason)


@html_only
def handle_http_exception(request: Request, exc: HTTPException):
    return render_error(
        request, exc.status_code, exc.headers, detail=exc.detail,
    )


@html_only
def handle_unprocessable_entity(request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return render_error(request, status_code, errors=exc.errors())


def handle_validation_error(request: Request, exc: ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    return render_error(request, status_code, errors=exc.errors())

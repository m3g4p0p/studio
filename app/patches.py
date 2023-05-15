from typing import Any
from typing import Callable
from typing import Coroutine

from fastapi import Request
from fastapi.routing import APIRoute
from starlette.datastructures import URL
from starlette.requests import Request
from starlette.responses import Response


class PatchedRequest(Request):

    def url_for(self, __name, **path_params) -> URL:
        url = super().url_for(__name, **path_params)
        return url.replace(scheme='')


class PatchedRoute(APIRoute):

    def get_route_handler(self) -> Callable[[
            Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def patched_route_handler(request: Request) -> Response:
            request = PatchedRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return patched_route_handler

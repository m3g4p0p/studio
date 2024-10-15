import os

from fastapi import Request
from fastapi.responses import RedirectResponse


async def redirect_middleware(request: Request, call_next):
    redirect_url = os.getenv('GLOBAL_REDIRECT_URL')

    if not redirect_url:
        return await call_next(request)

    return RedirectResponse(redirect_url + request.scope['path'])
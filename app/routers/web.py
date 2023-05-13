from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .. import base_path

router = APIRouter(default_response_class=HTMLResponse)
templates = Jinja2Templates(directory=base_path / 'templates')


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.jinja', {
        'request': request
    })

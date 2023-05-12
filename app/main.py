from datetime import date
from pathlib import Path
from urllib.error import HTTPError

from deta import Deta
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
deta = Deta()

db = deta.Base('reservations')
base_path = Path(__file__).parent

templates = Jinja2Templates(directory=base_path / 'templates')
app.mount('/static', StaticFiles(directory=base_path / 'static'), name='static')


class Reservation(BaseModel):

    band: str
    date: date


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.jinja', {
        'request': request
    })


@app.get('/dates/')
def get_reservations():
    today = date.today().isoformat()
    return db.fetch({'date?gte': today}).items


@app.post('/dates/')
def create_reservation(item: Reservation):
    try:
        return db.insert(jsonable_encoder(item), str(item.date))
    except HTTPError as e:
        raise HTTPException(e.code, f'{e.reason} 💀')

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from random import randint

from fastapi import FastAPI
from httpx import AsyncClient

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

async def health_check(app: FastAPI):
    external_url = os.getenv('RENDER_EXTERNAL_URL')

    if not external_url:
        return

    path = app.url_path_for('health_check')
    ping_url = external_url + path
    logger.info(ping_url)

    while True:
        async with AsyncClient() as client:
            response = await client.get(ping_url)

        logger.info(response.json())
        delay = randint(60, 600)
        await asyncio.sleep(delay)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(health_check(app))

    try:
        yield
    finally:
        task.cancel()
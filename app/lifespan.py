import asyncio
from contextlib import asynccontextmanager
import logging
import os
import sys

from fastapi import FastAPI
from httpx import URL, AsyncClient

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

async def health_check(app: FastAPI, delay: int):
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
        await asyncio.sleep(delay)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(health_check(app, 10))

    try:
        yield
    finally:
        task.cancel()
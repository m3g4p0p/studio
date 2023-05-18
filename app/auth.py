import os
import secrets

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

security = HTTPBasic()


def authenticate(
    credentials: HTTPBasicCredentials = Depends(security),
):
    is_authenticated = True

    for key, value in credentials.dict().items():
        env_key = f'basic_auth_{key}'.upper()

        is_authenticated = is_authenticated and secrets.compare_digest(
            value.encode('utf-8'), os.environ[env_key].encode('utf-8'),
        )

    if not is_authenticated:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

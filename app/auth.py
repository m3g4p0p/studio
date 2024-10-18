import secrets

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
from pydantic import SecretStr

from .settings import settings

security = HTTPBasic()


def authenticate(
    credentials: HTTPBasicCredentials = Depends(security),
):
    is_authenticated = True

    for key, value in credentials.model_dump().items():
        settings_value = getattr(settings.basic_auth, key)

        if isinstance(settings_value, SecretStr):
            settings_value = settings_value.get_secret_value()

        is_authenticated = is_authenticated and secrets.compare_digest(
            value.encode('utf-8'), settings_value.encode('utf-8'),
        )

    if not is_authenticated:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )

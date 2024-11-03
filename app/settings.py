import re

from pydantic import SecretStr
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

DRIVERS = {
    'sqlite': 'aiosqlite',
    'postgresql': 'asyncpg',
}


class BasicAuthSettings(BaseSettings):

    username: str
    password: SecretStr


class AppSettings(BaseSettings):

    sqlalchemy_database_url: str
    basic_auth: BasicAuthSettings
    develop: bool = False

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file_encoding='utf-8',
        env_file='.env',
        extra='ignore',
    )

    @field_validator('sqlalchemy_database_url', mode='after')
    def validate_driver(cls, value: str):
        for name, driver in DRIVERS.items():
            if re.match(name + ':', value):
                return re.sub(name, f'{name}+{driver}', value, 1)

        if not re.match(r'\w+\+\w+:', value):
            raise ValueError('missing driver')

        return value


settings = AppSettings.model_validate({})

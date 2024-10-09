from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class BasicAuthSettings(BaseSettings):

    username: str
    password: SecretStr


class AppSettings(BaseSettings):

    sqlalchemy_database_url: str
    basic_auth: BasicAuthSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file_encoding='utf-8',
        env_file='.env',
        extra='ignore',
    )


settings = AppSettings.model_validate({})

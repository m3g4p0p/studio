from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class AppSettings(BaseSettings):

    sqlalchemy_database_url: str

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
    )


settings = AppSettings.model_validate({})

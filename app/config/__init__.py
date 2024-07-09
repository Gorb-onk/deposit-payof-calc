from pydantic_settings import BaseSettings, SettingsConfigDict

from .logging import LoggingConf


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__', case_sensitive=False)
    logging: LoggingConf


settings = Settings()

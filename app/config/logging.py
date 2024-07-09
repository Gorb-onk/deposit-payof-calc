import logging
import os

from pydantic import BaseModel


class LoggingConf(BaseModel):
    disable_existing_loggers: bool = False

    CONSOLE_LOG_LEVEL: str | None = None
    LOGS_ROOT: str = '/var/log/depo-calc'

    SENTRY_DSN: str | None = None
    SENTRY_ENVIRONMENT: str | None = None

    formatters: dict = {
        'default': {
            'format': '{levelname: <8} | {asctime} | {pathname} |    {message}',
            'style': '{',
        },
        "terminal": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s | %(message)s",
        },
    }

    @computed_field  # type: ignore[misc]
    @property
    def handlers(self) -> dict:
        return {
            "console": {
                "level": self.CONSOLE_LOG_LEVEL,
                "formatter": "terminal",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "info_file": {
                "level": logging.INFO,
                "class": 'logging.handlers.RotatingFileHandler',
                "formatter": "default",
                "filename": os.path.join(self.LOGS_ROOT, 'info.log'),
                "maxBytes": 1024 ** 3 * 5,
                "backupCount": 5,
            },
            "error_file": {
                "level": logging.ERROR,
                "class": 'logging.handlers.RotatingFileHandler',
                "formatter": "default",
                "filename": os.path.join(self.LOGS_ROOT, 'error.log'),
                "maxBytes": 1024 ** 3 * 5,
                "backupCount": 5,
            },
        }

    @computed_field  # type: ignore[misc]
    @property
    def loggers(self) -> dict:
        return {
            "root": {
                "handlers": ["info_file", "error_file"] + (["console"] if self.CONSOLE_LOG_LEVEL else []),
                "level": "DEBUG",
            },
        }

from logging.config import dictConfig

import sentry_sdk

from app.config import settings

dictConfig(settings.logging.model_dump())

if settings.logging.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.logging.SENTRY_DSN,
        environment=settings.logging.SENTRY_ENVIRONMENT
    )

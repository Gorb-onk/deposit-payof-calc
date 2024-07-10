import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    loc = exc.args[0][0]['loc']
    tp = exc.args[0][0]['type']
    if tp == 'missing' and len(loc) == 1:
        msg = f"Missing {loc[0]}"
    elif tp == 'json_invalid':
        msg = f"{loc[0]} {exc.args[0][0]['msg']}"
    else:
        msg = f"{exc.args[0][0]['msg']}: {'.'.join(loc)} "
    logger.debug('Request validation error: %s', msg)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": msg}),
    )


from .endpoints import *


import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
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


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title="Sber deposit calculator",
            version="1.0.0",
            openapi_version=app.openapi_version,
            description="Сервис, для подсчета начислений по депозиту",
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']
                    responses['400'] = {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Error",
                                    "type": "object",
                                    "properties": {
                                        "error": {
                                            "title": "Error",
                                            "type": "string"
                                        }
                                    }
                                }
                            }
                        }
                    }
    return app.openapi_schema


app.openapi = custom_openapi

from .endpoints import *

from fastapi import FastAPI, Request, Response, exceptions
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from functions import *
import logging
import models
import uuid

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Freight Class Density Calculator",
    description="""This API helps calculate freight class based on density. 
    Freight class is a major factor in shipping cost, and is based on several features of the freight being shipped.""",
    docs_url=None,
    redoc_url="/docs",
    openapi_url="/docs/openapi.json",
    contact={"email":"calicojackdev@gmail.com"},
    license_info={"name":"The Unlicense"}
)

@app.post('/calculate')
async def calculate_class(items:models.Request):
    request_id = str(uuid.uuid4())
    load_items = items.items
    log_data(request_id,load_items)
    try:
        validate_density_payload(load_items)
    except (ValueError,TypeError) as err:
        timestamp = get_timestamp()
        logging.exception(f"{timestamp} -- {request_id}")
        res = models.ErrorResponse(
            error=err.args[0]
        )
        log_data(request_id,res)
        return JSONResponse(content=jsonable_encoder(res),status_code=422)
    try:
        load_cubed,load_weight,load_density,load_class = calculate_density_class(load_items)
        res = models.CalculatedResponse(
            cubicDimensions=load_cubed,
            totalWeight=load_weight,
            totalDensity=load_density,
            freightClass=load_class,
            unitType="standard"
        )
        log_data(request_id,res)
        return JSONResponse(content=jsonable_encoder(res),status_code=200)
    except Exception:
        timestamp = get_timestamp()
        logging.exception(f"{timestamp} -- {request_id}")
        res = models.ErrorResponse(
            error="Something went wrong, this error has been reported."
        )
        log_data(request_id,res)
        return JSONResponse(content=jsonable_encoder(res),status_code=500)

@app.exception_handler(exceptions.RequestValidationError)
async def validation_exception_handler(request,exc):
    request_id = str(uuid.uuid4())
    log_data(request_id,request)
    timestamp = get_timestamp()
    logging.exception(f"{timestamp} -- {request_id}")
    error_res = build_error_from_pydantic(exc.errors())
    res = models.ErrorResponse(
        error=error_res
    )
    log_data(request_id,res)
    return JSONResponse(content=jsonable_encoder(res),status_code=422)
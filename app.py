from fastapi import FastAPI, Request, Response, exceptions
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from functions import *
import logging
import models
import uuid

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Freight Density Calculator",
    description="""This API helps calculate freight class based on density. Here's how it works...""",
    docs_url=None,
    redoc_url="/docs",
    openapi_url="/docs/openapi.json",
    contact={"email":"freightconjugate@gmail.com"},
    license_info={"name":"The Unlicense"}
)

@app.post('/density/class')
async def calculate_class(items:models.Request):
    request_id = str(uuid.uuid4())
    load_items = items.items
    log_data(request_id,load_items)
    try:
        validate_density_payload(load_items)
    except (ValueError,TypeError) as err:
        timestamp = get_timestamp()
        logging.exception(f"{timestamp} -- {request_id}")
        res = {
            "status_code":422,
            "message":{
                "error":err.args[0]
            }
        }
        log_data(request_id,res)
        return JSONResponse(status_code=res['status_code'],content=res['message'])
    try:
        load_cubed,load_weight,load_density,load_class = calculate_density_class(load_items)
        res = models.CalculatedResponse(cubicDimensions=load_cubed,
            totalWeight=load_weight,
            totalDensity=load_density,
            freightClass=load_class,
            unitType="standard"
        )
        # res = {
        #     "status_code":200,
        #     "message":{
        #         "cubicDimensions":load_cubed,
        #         "totalWeight":load_weight,
        #         "totalDensity":load_density,
        #         "freightClass":load_class,
        #         "unitType":"standard"
        #     }
        # }
        print(jsonable_encoder(res))
        return JSONResponse(content=jsonable_encoder(res))
        #return JSONResponse(status_code=res['status_code'],content=res['message'])
    except Exception:
        timestamp = get_timestamp()
        logging.exception(f"{timestamp} -- {request_id}")
        res = {
            "status_code":500,
            "message":{
                "error":"something went wrong"
            }
        }
        return JSONResponse(status_code=res['status_code'],content=res['message'])
    finally:
        log_data(request_id,res)

@app.exception_handler(exceptions.RequestValidationError)
async def validation_exception_handler(request,exc):
    request_id = str(uuid.uuid4())
    log_data(request_id,request)
    timestamp = get_timestamp()
    logging.exception(f"{timestamp} -- {request_id}")
    error_res = build_error_from_pydantic(exc.errors())
    res = {
        "status_code":422,
        "message":{
            "error":error_res
        }
    }
    log_data(request_id,res)
    return JSONResponse(status_code=res['status_code'],content=res['message'])
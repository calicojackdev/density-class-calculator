from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    length:int
    width:int
    height:int
    weight:int

    class Config:
        schema_extra = {
            "example":{
                "length":40,
                "width":48,
                "height":48,
                "weight":500
            }
        }

class Request(BaseModel):
    items:List[Item]

class ErrorResponse(BaseModel):
    error:str

class CalculatedResponse(BaseModel):
    cubicDimensions:float
    totalWeight:float
    totalDensity:float
    freightClass:int
    unitType:str

    class Config:
        schema_extra = {
            "example":{
                "cubicDimensions": 53.33,
                "totalWeight": 500,
                "totalDensity": 9.38,
                "freightClass": 100,
                "unitType": "standard"
            }
        }

responses = {
    200: {
        "description": "Computed class",
        "content": {
            "application/json"
        },
        "model":CalculatedResponse
    },
    422: {
        "description": "Invalid input",
        "model": ErrorResponse, 
    }
    
}
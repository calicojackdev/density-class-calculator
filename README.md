# Density Calculator  
The Freight Class Density Calculator is a simple API to calculate freight class for an LTL load.  
Freight class depends on several features of a load, including:  
* Density  
* Liability  
* Stowability  
* Ease of handling  

This API was built using FastAPI.  

# Running the API  
This app has not been dockerized, so more primitive methods may be employed.  
Getting started may look like:  
* Clone this repo into your local dev environment  
* Start the server: `uvicorn app:app`  

# Using the API  
1. Send a POST request to the `/calculate` endpoint:  
```
{
    "items":[
        {
            "length":48,
            "width":48,
            "height":48,
            "weight":500
        }
    ]
}
```
2. Receive a response:
```
{
    "cubicDimensions": 64.0,
    "totalWeight": 500.0,
    "totalDensity": 7.81,
    "freightClass": 125,
    "unitType": "standard"
}
```
This API expects "standard" units for input and does not support metric units. 

# Contact
Shoot me a note at calicojackdev@gmail.com with any comments/questions.
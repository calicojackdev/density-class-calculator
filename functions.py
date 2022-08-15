import datetime
import logging

def log_data(request_id,data) -> None:
    timestamp = (datetime.datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"{timestamp} -- {request_id} -- {data}")
    return

def get_timestamp() -> str:
    timestamp = (datetime.datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

def build_error_from_pydantic(exc_list:list):
    exc_msg = exc_list[0]['msg']
    exc_loc = exc_list[0]['loc']
    exc_type = exc_list[0]['type']
    error_string = None
    if len(exc_loc) == 2:
        exc_field = f"{exc_loc[1]}"
        error_string = f"{exc_field} {exc_msg}"
    if len(exc_loc) == 4:
        exc_field = f"{exc_loc[1]}[{exc_loc[2]}]['{exc_loc[3]}']"
        error_string = f"{exc_field} {exc_msg}"
    if  exc_type == "value_error.jsondecode":
        error_string = exc_msg
    return error_string

def validate_density_payload(load_items) -> None: 
    if len(load_items) > 100:
        raise ValueError("items array too long")
    for index,item in enumerate(load_items):
        if (type(item.length) != int or
            type(item.width) != int or
            type(item.height) != int or
            type(item.weight) != int
            ):
            dim_type_error_string = f"please enter valid integer dims in items[{index}]"
            raise ValueError(dim_type_error_string)
        if (item.length <= 0 or
            item.width <= 0 or 
            item.height <= 0 or 
            item.weight <= 0
            ):
            negative_dim_error_string = f"please enter postivite integer dims in items[{index}]"
            raise ValueError(negative_dim_error_string)
    return

def calculate_density_class(load_items):
    load_weight,load_cubed = dim_sum(load_items)
    load_density = calculate_density(load_weight,load_cubed)
    load_class = calculate_class(load_density)
    return round(load_cubed,2),round(load_weight,2),round(load_density,2),round(load_class,2)

def dim_sum(load_items): 
    load_weight = 0
    load_cubed = 0
    for item in load_items:
        load_weight += item.weight
        load_cubed += cube_item(item.length,item.width,item.height)
    return load_weight,load_cubed

def cube_item(length,width,height):
    item_cubed = (length*width*height)/1728
    return item_cubed

def calculate_density(load_weight,load_cubed):
    load_density = load_weight/load_cubed
    return load_density

def calculate_class(load_density):
    if (load_density >= 50):
        load_class = 50
    elif (load_density >= 35) and (load_density < 50):
        load_class = 55
    elif (load_density >= 30) and (load_density < 35):
        load_class = 60
    elif (load_density >= 22.5) and (load_density < 30):
        load_class = 65
    elif (load_density >= 15) and (load_density < 22.5):
        load_class = 70
    elif (load_density >= 13) and (load_density < 15):
        load_class = 77.5
    elif (load_density >= 12) and (load_density < 13):
        load_class = 85
    elif (load_density >= 10.5) and (load_density < 12):
        load_class = 92.5
    elif (load_density >= 9) and (load_density < 10.5):
        load_class = 100
    elif (load_density >= 8) and (load_density < 9):
        load_class = 110
    elif (load_density >= 7) and (load_density < 8):
        load_class = 125
    elif (load_density >= 6) and (load_density < 7):
        load_class = 150
    elif (load_density >= 5) and (load_density < 6):
        load_class = 175
    elif (load_density >= 4) and (load_density < 5):
        load_class = 200
    elif (load_density >= 3) and (load_density < 4):
        load_class = 250
    elif (load_density >= 2) and (load_density < 3):
        load_class = 300
    elif (load_density >= 1) and (load_density < 2):
        load_class = 400
    elif (load_density >= 0) and (load_density < 1):
        load_class = 500
    else:
        load_class = 0
        #raise an error if we get here?
    return load_class


def unsupported_method():
    res = {
        "error":"You invoked an unsupported method. Here's a link to our documentation:"
    }
    return res
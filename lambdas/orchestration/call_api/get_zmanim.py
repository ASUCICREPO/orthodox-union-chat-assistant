from datetime import datetime 
import requests
from call_api.get_location_bot import user_location
from call_api.location_api import get_location_api

import re

def get_zmanim(user_message:str):
    response = user_location(user_message)
    response=response.strip(" ")
    response=response.split(",")
    location=response[0].strip('"')
    zipcode = ""
    if location != "":
        zipcode = get_zipcode()
    day = response[1].replace('"', '')
    day=day.replace(" ", "")
    day=day.replace("\n", "")
    lat_long = get_location_api(location)
    latitude, longitude, timezone = lat_long
    if day == "":
        date = datetime.now() # type: ignore
        date = date.strftime("%m/%d/%Y")
    else:
        date=day
    
    if zipcode:
        url = "https://db.ou.org/zmanim/getCalendarData.php"+"?mode=day" + f"&dateBegin={date}" + f"&zipCode={zipcode}"
    else:
        url= "https://db.ou.org/zmanim/getCalendarData.php"+"?mode=day" +  f"&timezone={timezone}" +f"&dateBegin={date}" + f"&lat={latitude}" + f"&lng={longitude}" 
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        zmanim_data = response.json()  # Parse JSON response
        results = {
            "metadata": {'x-amz-bedrock-kb-source-uri': 'zmanim_api'},
            "content": {'text': f"These are the zmanim for {location}: {zmanim_data}"},
        }
        
        return results
        
    except requests.exceptions.RequestException as e:
        zmanim_data = "Here's a link to myzmanim you can use: https://www.myzmanim.com/search.aspx"
        results = {
            "metadata": {'x-amz-bedrock-kb-source-uri': 'zmanim_api_error'},
            "content": {'text': zmanim_data},
        }
        return results
    
def get_zipcode():
    input_message = "Please enter the zipcode for the location: "
    zipcode = input(input_message)
    return zipcode

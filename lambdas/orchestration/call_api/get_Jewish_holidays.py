from datetime import datetime 
import requests
from call_api.get_holiday_info_bot import user_holiday_info

import re

def get_Jewish_holidays(user_message:str):
    response = user_holiday_info(user_message)
    response=response.strip(" ")
    response=response.split(",")
    holiday_date=response[0].strip('"')
    
    url = "https://db.ou.org/zmanim/getHolidayCalData.php"+f"?year={holiday_date}"

    try:
        current_date = datetime.now()
        current_date= current_date.strftime("%m/%d/%Y")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        holiday_data = response.json()  # Parse JSON response
        results = {
            "metadata": {'x-amz-bedrock-kb-source-uri': 'holiday_api'},
            "content": {'text': f"Todays date is {current_date}. These are a list of the Jewish holidays and their dates for {holiday_date}: {holiday_data}"},
        }
        return results
        
    except requests.exceptions.RequestException as e:
        holiday_data = "I'm sorry. I couldn't get the information you requested."
        results = {
            "metadata": {'x-amz-bedrock-kb-source-uri': 'holiday_api_error'},
            "content": {'text': holiday_data},
        }
        return results
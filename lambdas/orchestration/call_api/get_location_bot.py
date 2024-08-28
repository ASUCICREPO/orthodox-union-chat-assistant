from datetime import datetime
import os

from bedrock_orchestration.generate_response import generate_response
from call_api.location_api import get_location_api


def user_location(user_input):
    user_prompt = generate_prompt(user_input)
    model_id = os.environ["SOURCE_EXTRACTION_BOT_ID"]
    assistant_prompt = '['
    location = generate_response(model_id, user_prompt, assistant_prompt)
    location = location.strip("\"\'] \n")
    location = location[0].upper() + location[1:]
    return location

def generate_prompt(user_input):
    #date=datetime.now()
    #print(date)
    prompt = f"""Given a user query, extract the location and day mentioned and return it as an Array object with with fields called "location" and "day".
    For the day, return the date of that day. Calucuate the date using how far it is from todays date.
    If no location is found, set the value to "". If no day is found or the user asks for today, set the value to "". Only return the Array object, without any 
    additional explanation or text.

    Example inputs and outputs:
    Input: "What time is sunset in Lakewood on Wednesday?"
    Output: ["Lakewood","08/07/2024"]

    Input: "What's the weather like in Paris?"
    Output: ["Paris", ""]
    Ensure that the Array object contains only the 'location' and 'day' fields. Do not include any explanations, code, or additional text in your response. Only return the Array object.

    Input: {user_input}
    """

    return prompt

# response = user_location("What time is sunset in Far Rockaway on Wednesday?")
# response=response.strip(" ")
# response=response.split(",")
# location=response[0].strip('"')
# day = response[1].replace('"', '')
# day=day.replace(" ", "")
# day=day.replace("\n", "")
# print("location: " + location + " day: "+ day)
# location_api = get_location_api(location)

# zmanin = get_zmanim(location_api, day)
# print(zmanin)
# # print(location)
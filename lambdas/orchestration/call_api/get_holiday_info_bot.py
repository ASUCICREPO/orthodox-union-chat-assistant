from datetime import datetime
import os

from bedrock_orchestration.generate_response import generate_response


def user_holiday_info(user_input):
    user_prompt = generate_prompt(user_input)
    model_id = os.environ["SOURCE_EXTRACTION_BOT_ID"]
    assistant_prompt = '['
    holiday_date = generate_response(model_id, user_prompt, assistant_prompt)
    holiday_date = holiday_date.strip("\"\'] \n")
    holiday_date = holiday_date[0].upper() + holiday_date[1:]
    return holiday_date

def generate_prompt(user_input):
    current_year = datetime.now().year
    prompt = f"""Given a user query, if a date is mentioned, use the year mentioned and return it as an Array object.

    If the user asks for next year or last year, in three years etc., calculate the year based on this years date. If no date is found or the user asks for this year, 
    set the value to the current year{current_year}.  Only return the Array object, without any 
    additional explanation or text. Keep in mind that the Jewish calendar begins with Rosh Hashanah as the Jewish New Year. 

    Example inputs and outputs:
    Input: "When is Pesach in 2025?"
    Output: ["2025"]

    Input: "When is Purim this year?"
    Output: ["{current_year}"]
    Do not include any explanations, code, or additional text in your response. Only return the Array object.
   
    Input: {user_input}
    """

    return prompt
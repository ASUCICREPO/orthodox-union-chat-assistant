from bedrock_orchestration.generate_response import generate_response
import os

def get_title_of_text(user_input):
    user_prompt = generate_prompt(user_input)
    model_id = os.environ["SOURCE_EXTRACTION_BOT_ID"]
    assistant_prompt = '['
    title = generate_response(model_id, user_prompt, assistant_prompt)
    title = title.strip("\"\'] \n")
    title = title[0].upper() + title[1:]
    return title

def generate_prompt(user_input):
    prompt = f"""Given a user query, extract the name of the text they are searching for and return it's english name as an Array object. The query may be in 
    English or Hebrew and may use various formats to specify the source. Account for and correct common typos, including keyboard adjacency errors 
    in both English and Hebrew. Standardize the source name to match Sefaria's convention, using English names for books and tractates. Correct 
    common misspellings and keyboard typos in both English and Hebrew (e.g., 'kidushin' to 'kiddushin', 'brochos' to 'berakhot', 'דוטה' to 'סוטה'). 
    For Talmud, use 'tractate page letter'. For Torah/Tanakh, use 'book chapter'. For Mishnah and other sources, use the appropriate format without
    letter suffixes. Examples of inputs and their corrected outputs:

    -How many pesukim are in berachos 5a' or ' ברכות ה.' should return ['berakhot']
    -How many pesukim are in chulin daf 81b' or ' חולין דף פא:' should return ['chullin']
    -How many pesukim are in bereishis perek alef' or 'בראשית א' should return ['genesis']
    -How many perakim are in pirkei avot ' should return ['pirkei avot']
    -How many pesukim are in kidushin 41a' (typo) should return ['kiddushin']
    -How many pesukim are in דוטה דף ב' (Hebrew keyboard typo) should return ['sotah']
    -How many sefarim are in gemara should return ['Talmud']

    If no text name is found, set the value to "". Only return the Array object, without any additional explanation or text.

    Ensure that the Array object contains only the text name. Do not include any explanations, code, or additional text in your response. Only return the Array object.

    Input: {user_input}
    """

    return prompt

# title=get_title_of_text("How many parshiot are in sefer shemos?")
# url=get_size_of_jewish_text(title)
# print(url)
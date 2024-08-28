from bedrock_orchestration.results_from_kb import get_results_from_kb
from bedrock_orchestration.generate_response import generate_response
import os


def get_kb_results_for_source(user_input):
    source = f's3://testshimonus/sefaria_sources/'
    kb_results = get_results_from_kb(user_input, source)
    return kb_results['retrievalResults']

def extract_source(user_input):
    user_prompt = generate_prompt(user_input)
    model_id = os.environ["SOURCE_EXTRACTION_BOT_ID"]
    assistant_prompt = '{"source": "'
    source = generate_response(model_id, user_prompt, assistant_prompt)
    source = source.strip("\"\'} \n")
    source = source[0].upper() + source[1:]
    return source

def generate_prompt(user_input):
    # prompt_template = f"""For any user query asking about a textual source, respond with a JSON object containing a single field called 'source'. The value of this field should be the exact textual source as mentioned in the query, without translation or modification. For example, if the query is 'what does rav moshe say in igros moshe chelek 4 siman 62', your response should be {{'source':'igros moshe chelek 4 siman 62'}}. Only include the JSON object in your response, without any additional text or explanation. Do not translate or modify the source text in any way; use it exactly as it appears in the query.
    # Input: {user_input}
    # """
    prompt_template = f"""Given a user query to summarize a text source, extract the text source, correct it to a valid Sefaria source, and return a JSON object with one field called 'source'. The query may be in English or Hebrew and may use various formats to specify the source. Account for and correct common typos, including keyboard adjacency errors in both English and Hebrew. Examples:

- 'summarize berachos 5a' or 'summarize ברכות ה.' should return {{'source': 'berakhot 5a'}}
- 'summarize chulin daf 81b' or 'summarize חולין דף פא:' should return {{'source': 'chullin 81b'}}
- 'summarize bereishis perek alef' or 'summarize בראשית א' should return {{'source': 'genesis 1'}}
- 'summarize pirkei avot 1:1' should return {{'source': 'pirkei avot 1:1'}}
- 'summarize kidushin 41a' (typo) should return {{'source': 'kiddushin 41a'}}
- 'summarize דוטה דף ב' (Hebrew keyboard typo) should return {{'source': 'sotah 2a'}}

Standardize the source name to match Sefaria's convention, using English names for books and tractates. Correct common misspellings and keyboard typos in both English and Hebrew (e.g., 'kidushin' to 'kiddushin', 'brochos' to 'berakhot', 'דוטה' to 'סוטה'). For Talmud, use 'tractate page letter'. For Torah/Tanakh, use 'book chapter'. For Mishnah and other sources, use the appropriate format without letter suffixes.

When Hebrew letters are used for numbers, convert them accurately to their numerical equivalents (e.g., פא = 81). For Talmud references, use 'a' for . (or no symbol) and 'b' for : in Hebrew queries.

Ensure that the JSON object contains only the 'source' field with the corrected and standardized source reference. Do not include any explanations, code, or additional text in your response. Only return the JSON object.
    Input: {user_input}
    """
#     prompt_template = f"""Given a user query to summarize a text source, extract the text source, correct it to a valid Sefaria source, and return a JSON object with one field called 'source'. The query may be in English or Hebrew and may use various formats to specify the source. Examples:

# - 'summarize berachos 5a' or 'summarize ברכות ה.' should return {{'source': 'berakhot 5a'}}
# - 'summarize חולין דף פא:' should return {{'source': 'chullin 81b'}}
# - 'summarize bereishis perek alef' or 'summarize בראשית א' should return {{'source': 'genesis 1'}}
# - 'summarize pirkei avot 1:1' should return {{'source': 'pirkei avot 1:1'}}

# Standardize the source name to match Sefaria's convention, using English names for books and tractates. For Talmud, use 'tractate page letter'. For Torah/Tanakh, use 'book chapter'. For Mishnah and other sources, use the appropriate format without letter suffixes.

# When Hebrew letters are used for numbers, convert them accurately to their numerical equivalents (e.g., פא = 81). For Talmud references, use 'a' for . (or no symbol) and 'b' for : in Hebrew queries.

# Ensure that the JSON object contains only the 'source' field with the corrected and standardized source reference. Do not include any explanations, code, or additional text in your response. Only return the JSON object.
#     Input: {user_input}
#     """

   
    return prompt_template

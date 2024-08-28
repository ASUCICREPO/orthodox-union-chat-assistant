from call_api.get_zmanim import get_zmanim
from call_api.get_Jewish_holidays import get_Jewish_holidays
from call_api.source_extraction_bot import get_kb_results_for_source
from call_api.get_size_of_Jewish_texts import get_size_of_jewish_text

def get_Number_lectures(author):
    return [] # TODO implement

def call_api(api_id:str, user_message):
    dictionary = {
        "1": get_zmanim,
        "2": get_Jewish_holidays,
        "3": get_size_of_jewish_text,
        "4": get_Number_lectures,
        "5": get_kb_results_for_source
    }
    api = dictionary.get(api_id)
    if api:
        api_results = api(user_message) # type: ignore
        if not isinstance(api_results, list):
            # todo format properly
            api_results = [api_results]
        return api_results
    else:
        return []

def get_additional_sources(user_message, query_classification):
    return call_api(query_classification, user_message)
    

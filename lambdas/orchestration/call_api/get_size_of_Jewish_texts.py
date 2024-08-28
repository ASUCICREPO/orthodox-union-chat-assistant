import requests
from call_api.get_title_of_text import get_title_of_text


def get_size_of_jewish_text(user_message):
    title=get_title_of_text(user_message)
    url=f'https://www.sefaria.org/api/shape/{title}'

    try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP error responses
            sefaria_data = response.json()  # Parse JSON response
            results = {
                "metadata": {'x-amz-bedrock-kb-source-uri': 'sefaria_api'},
                "content": {'text': f"Here is the information for {title}, the field 'length' is the amount of pesukim and the field 'chapters' is the length of each perek: {sefaria_data}"},
            }
            return results
            
    except requests.exceptions.RequestException as e:
        sefaria_data = ""
        results = {
            "metadata": {'x-amz-bedrock-kb-source-uri': 'sefaria_api_error'},
            "content": {'text': sefaria_data},
        }
        return results
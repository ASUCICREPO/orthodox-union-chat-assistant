import re

def generate_sources(sources):
    prompt_sources = ""
    for source_key in sources:
        source_text = sources.get(source_key).get("text")
        prompt_sources += f"<{source_key}>\n   {source_text}\n</{source_key}>\n\n"
    
    return prompt_sources

def replace_source(sources, text):
    match = re.search(r'SOURCE\d', text)
    if match:
        source_key = match.group()    
        text = text.replace(source_key, "(https://alldaf.org/p/" + sources.get(source_key).get('name') + ")")
    return text

def generate_history(history):

    print("History transfers")
    print(history)

    chat_history_formatted = "<Previous_Convo>\n"

    for message in history:
        if message["sentBy"] == "USER":
            chat_history_formatted += f"<User>{message['message']}</User>\n"
        elif message["sentBy"] == "BOT" and message["state"] == "FINISHED":
            chat_history_formatted += f"<AI>{message['message']}</AI>\n"
        else:
            chat_history_formatted += ""

    chat_history_formatted += "</Previous_Convo>"
            
    return chat_history_formatted

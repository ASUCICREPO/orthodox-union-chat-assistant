from bedrock_orchestration.chatbot_prompt import first_prompt, second_prompt, third_prompt
from bedrock_orchestration.insert_sources import generate_sources, replace_source, generate_history
from bedrock_orchestration.results_from_kb import get_results_from_kb, extract_sources
from bedrock_orchestration.generate_response import converse_stream
import os
import boto3
import json
import datetime




def talk_to_LLM(user_input, additional_sources, connectionId, history):

    kb_results = get_results_from_kb(user_input)
    sources = extract_sources(kb_results, additional_sources)
    
    prompt = generate_prompt(user_input, sources, history)
    model_id = os.environ["ORCHESTRATION_MODEL_ID"]
    temperature = float(os.environ["TEMPERATURE"])
    print("TESTINNNNG")

    complete_text = generate_response_final(sources, model_id, prompt, connectionId, temperature)
    
    return complete_text

def generate_response_final(sources, model_id, prompt_template, connectionId, temperature):

    #create the model client to call, the RAG agent, and gateway connection for response
    apiGatewayURL = "https" + os.environ['WEBSOCKET_URL'][3:] + "/prod"    #https URL for the api gateway websocket
    gateway = boto3.client("apigatewaymanagementapi", endpoint_url=apiGatewayURL)
    bedrock = boto3.client(service_name="bedrock-runtime")

    #Create the prompt API call to bedrock, includes: Model, content type, how the call is formatted, and the model specific info (tokens, prompt, etc)
    kwargs = {
        "modelId": model_id,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": prompt_template
                }
                ]
            }
            ],
            "temperature": temperature,
        })
    }

    #Call the model with a response stream (creates an iterable object when converted)
    response = bedrock.invoke_model_with_response_stream(**kwargs)
    

    #Convert the model specific API response into general packet with start/stop info, here converts from Claude API response (Could be done for any model)
    temp_holder = ""
    stream = response.get('body')
    if stream:

        #for each returned token from the model:
        for token in stream:

            #The "chunk" contains the model-specific response
            chunk = token.get('chunk')
            if chunk:
                
                #Decode the LLm response body from bytes
                chunk_text = json.loads(chunk['bytes'].decode('utf-8'))
                
                #Construct the response body based on the LLM response, (Where the generated text starts/stops)
                if chunk_text['type'] == "content_block_start":
                    block_type = "start"
                    message_text = ""
                    
                elif chunk_text['type'] == "content_block_delta":
                    block_type = "delta"
                    message_text = chunk_text['delta']['text']

                    if "SOURCE" in message_text:
                        temp_holder = message_text
                        message_text = ""
                    else:
                        message_text = temp_holder + message_text
                        temp_holder = ""      
                    
                elif chunk_text['type'] == "content_block_stop":
                    block_type = "end"
                    message_text = ""

                else:
                    block_type = "blank"
                    message_text = ""
                    

                if "SOURCE" in message_text:
                    message_text = source_replace(sources, message_text)

                
                #Send the response body back through the gateway to the client    
                data = {
                    'statusCode': 200,
                    'type': block_type,
                    'text': message_text,
                }
                gateway.post_to_connection(ConnectionId=connectionId, Data=json.dumps(data))
    
    return "Success"

def source_replace(sources, text):
    num_source = int(os.environ["NUM_KB_RESULTS"])
    for i in range(num_source):
        if "SOURCE" + str(i) in text:
            #https://alldaf.org/p/82980
            text = text.replace("SOURCE" + str(i), "(https://alldaf.org/p/" + sources["SOURCE" + str(i)]["name"] + ")")
            print("REPLACED" + "SOURCE" + str(i))
    return text


def generate_prompt(user_input, sources, history):

    time = datetime.datetime.now().strftime("%A, %m/%d/%Y")

    prompt_template = first_prompt(time)

    second_prompt_template = second_prompt()

    third_prompt_template = third_prompt()

    prompt_sources = generate_sources(sources)

    chat_history = generate_history(history)
    
    prompt_template += f"{chat_history}\n{second_prompt_template}\n{prompt_sources}\n{third_prompt_template}\n\n<Query>\n{user_input}\n</Query>\n\n\n"
    return prompt_template

def generate_response(sources, model_id, prompt_template):
    assistant_prompt = 'To answer your question,'
    response = converse_stream(model_id, prompt_template, assistant_prompt)
   
    prev_text = ""
    complete_text = ""
    stream = response.get('stream')
    if stream:
        for event in stream:
            if 'contentBlockDelta' in event:
                delta = event['contentBlockDelta']['delta']
                text = delta.get('text', '')
 
                if prev_text:
                    text = prev_text + text
                    text = replace_source(sources, text)
                    complete_text += text
                    print(text, end='')
                    prev_text = ''
                elif 'SOURCE' in text:
                    prev_text = text
                else:
                    complete_text += text
                    print(text, end='')
               
    return complete_text.strip()



import boto3
import os

def generate_response(model_id, user_prompt, assistant_prompt):
    stream = converse_stream(model_id, user_prompt, assistant_prompt)
    return get_response(stream)

def converse_stream(model_id, user_prompt, assistant_prompt):
    bedrock = boto3.client(service_name="bedrock-runtime")
    response = bedrock.converse_stream(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": user_prompt
                    }
                ]
            },
            {"role": "assistant","content":[{"text": assistant_prompt }]},
        ],
        inferenceConfig={"temperature": float(os.environ["TEMPERATURE"])},
    )
    
    return response

def get_response(response):
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

                    complete_text += text
                    prev_text = ''
                else:
                    complete_text += text
                #print(text, end='')   

            # if 'metadata' in event:
            #     print(event['metadata'])   

    return complete_text

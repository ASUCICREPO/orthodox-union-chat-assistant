from bedrock_orchestration.generate_response import generate_response
import os


def classify_user_query(user_query):

    user_prompt = generate_prompt(user_query)

    model_id = os.environ["CLASSIFICATION_MODEL_ID"]
    assistant_prompt = '{"category":'
    query_classification = generate_response(model_id, user_prompt, assistant_prompt)
    return query_classification.strip("} \n")


def generate_prompt(user_input):
    prompt_template = f"""
    You are a classification bot. Your task is to categorize the given input into one of the following categories:

        1. Jewish time 
        2. Jewish holidays 
        3. Size of Jewish texts 
        4. Number of lectures for a speaker
        5. Summarization of Jewish texts
        6. None of the above

    After analyzing the input, respond with a JSON object in the following format:
    {{"category": X}}

    Where X is the number (1-6) corresponding to the most appropriate category. Use 6 if none of the categories apply.

    Input: {user_input}

    Classify the input and provide your response in the specified JSON format.
    """   
    return prompt_template

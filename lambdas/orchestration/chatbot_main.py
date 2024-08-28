from bedrock_orchestration.bedrock_orchestration import talk_to_LLM
from classification_bot.classification_bot import classify_user_query
from call_api.call_api import get_additional_sources

def lambda_handler(event, context):

  user_message = event["prompt"]
  connectionId = event["connectionId"]
  history = event["history"]

  query_classification = classify_user_query(user_message)
  print(f"Category: {query_classification}")
  additional_sources = get_additional_sources(user_message, query_classification)
  talk_to_LLM(user_message, additional_sources, connectionId, history)
  
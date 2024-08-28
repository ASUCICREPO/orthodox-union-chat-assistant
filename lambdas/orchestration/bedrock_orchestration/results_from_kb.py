import re
import boto3
import os

def get_results_from_kb(prompt, filter=None):
    agent = boto3.client('bedrock-agent-runtime')
    knowledge_base_id = os.environ["KNOWLEDGE_BASE_ID"]
    query = {
       'text': prompt
    }
    retrieval_configuration={
        'vectorSearchConfiguration': {
            'numberOfResults': int(os.environ["NUM_KB_RESULTS"]),
        }
    }
    if filter:
        retrieval_configuration['vectorSearchConfiguration']['filter'] = { # type: ignore
                 'stringContains': {
                    'key': 'x-amz-bedrock-kb-source-uri',
                    'value': filter
                }
            }
    kb_results = agent.retrieve(knowledgeBaseId=knowledge_base_id, retrievalQuery=query, retrievalConfiguration=retrieval_configuration)
    return kb_results

def extract_sources(kb_results, additional_sources):
    processed_sources = {}
    source_num = 0
    for sources in [additional_sources, kb_results['retrievalResults']]:
        for source in sources:
            source_key = get_source_key(source_num)
            processed_sources[source_key] = process_source(source)
            source_num += 1        
    return processed_sources

def process_source(source):
    print("METADATA BELOW LOOK AT ME")
    print(source.get("metadata"))
    name = source.get("metadata").get('x-amz-bedrock-kb-source-uri')
    name = get_text_after_last_slash(name)

    # Strip the ".txt" extension and keep only the numbers
    name = name.rstrip('.txt')
    name = ''.join(filter(str.isdigit, name))
    
    text = source.get("content").get("text")
    return {"name": name, "text": text}

def get_text_after_last_slash(text):
    match = re.search(r'/([^/]+)/?$', text)
    return match.group(1) if match else text

def get_source_key(i):
    return "SOURCE" + str(i)
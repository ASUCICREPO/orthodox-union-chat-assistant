from __future__ import print_function
import boto3
import os
import json
import re
import zipfile
import io
import urllib3

replace_token = "WSS-URL"
bucket_name = os.environ['BUCKET_NAME']
api_url = os.environ['API_URL'] + "/prod"
s3 = boto3.client('s3')
http = urllib3.PoolManager()

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def lambda_handler(event, context):

    print("Event: ")
    print(event)
    try:
        request_type = event['RequestType']
        if request_type in ["Delete", "Update"]:
            send(event, context, SUCCESS, {})
            return

        # Unzip the contents of the zip file
        unzip_s3_file()

        folder_prefix = 'static/js/'
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        pattern1 = r'^static/js/main\.[a-zA-Z0-9]{8}\.js$'
        pattern2 = r'^static/js/main\.[a-zA-Z0-9]{8}\.js\.map$'
        
        matching_file1, matching_file2 = find_file((pattern1, pattern2), response)
        
        websocket_replace((matching_file1, matching_file2), bucket_name)
        
        response_data = {
            "file1": matching_file1,
            "file2": matching_file2
        }

        print(response_data)
        
        send(event, context, SUCCESS, {})
    except Exception as e:
        print(f"Error: {str(e)}")
        send(event, context, FAILED, {"Error": str(e)})

content_types = {
    ".html": "text/html",
    ".json": "application/json",
    ".ico": "image/vnd.microsoft.icon",
    ".txt": "text/plain",
    ".css": "text/css",
    ".svg": "image/svg+xml"
}

def unzip_s3_file():
    zip_file_key = "frontend_store_bucket.zip"
    # Download the zip file from S3
    zip_obj = s3.get_object(Bucket=bucket_name, Key=zip_file_key)
    zip_content = zip_obj['Body'].read()

    # Unzip the contents
    with zipfile.ZipFile(io.BytesIO(zip_content)) as zip_ref:
        for file_info in zip_ref.infolist():
            file_content = zip_ref.read(file_info.filename)
            _, file_extension = os.path.splitext(file_info.filename)
            
            # Determine content type based on file extension
            content_type = content_types.get(file_extension.lower())
            
            # If content type is found, include it in put_object
            if content_type:
                s3.put_object(Bucket=bucket_name, Key=file_info.filename, Body=file_content, ContentType=content_type)
            else:
                s3.put_object(Bucket=bucket_name, Key=file_info.filename, Body=file_content)
    
    # Delete the original zip file
    s3.delete_object(Bucket=bucket_name, Key=zip_file_key)

def websocket_replace(matching_files, bucket_name):
    for matching_file in matching_files:
        local_file_name = os.path.basename(matching_file)
        local_file_path = f'/tmp/{local_file_name}'
        
        s3.download_file(bucket_name, matching_file, local_file_path)
        print(f"File downloaded: {local_file_path}")
        
        with open(local_file_path, 'r') as file:
            content = file.read()
        
        new_content = content.replace(replace_token, api_url)
        with open(local_file_path, 'w') as file:
            file.write(new_content)
        
        s3.upload_file(local_file_path, bucket_name, matching_file)
        print("File Uploaded")
        
        os.remove(local_file_path)

def find_file(regx_tuple, response):
    matching_files = []
    for obj in response.get('Contents'):
        if any(re.match(regx, obj['Key']) for regx in regx_tuple):
            matching_files.append(obj['Key'])
            if len(matching_files) == len(regx_tuple):
                break
            
    return tuple(matching_files)

def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']
    print(responseUrl)
    responseBody = {
        'Status' : responseStatus,
        'Reason' : reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId' : physicalResourceId or context.log_stream_name,
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'LogicalResourceId' : event['LogicalResourceId'],
        'NoEcho' : noEcho,
        'Data' : responseData
    }
    json_responseBody = json.dumps(responseBody)
    print("Response body:")
    print(json_responseBody)
    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }
    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)
    except Exception as e:
        print("send(..) failed executing http.request(..):", e)
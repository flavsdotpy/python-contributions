import json

import boto3

BUCKET = 'ap3xx-configuration'
KEY = 'script-settings/sample.json'

resource = boto3.resource('s3')

try:
    result = resource.Object(BUCKET, KEY)
    decoded_body = result.get()["Body"].read().decode()
    json_obj = json.loads(decoded_body)
except Exception as e:
    print(e)

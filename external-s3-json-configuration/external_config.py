import json
import boto3


BUCKET = 'ap3xx-configuration'
KEY = 'script-settings/sample.json'

resource = boto3.resource('s3')

try:
    result = resource.Object(BUCKET, KEY)
    decoded_body = result.get()["Body"].read().decode()
except Exception as e:
    print(e)
    decoded_body = '{}'

configuration = json.loads(decoded_body)

for source in configuration.get('AthenaSources', []):
    print(source)
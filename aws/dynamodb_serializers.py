import json
import boto3
import base64
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

output = []

def lambda_handler(event, context):
    
    
    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8')
        

        row_w_newline = payload + "\n"
        
        print('row_w_newline type:', type(row_w_newline))
        x = parse_low_level_event(json.loads(row_w_newline))

        row_w_newline = base64.b64encode(str(x).encode('utf-8'))

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': row_w_newline
        }
        output.append(output_record)

    print('Processed {} records.'.format(len(event['records'])))

    return {'records': output}

def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    deserializer = TypeDeserializer()
    return {
        k: deserializer.deserialize(v)
        for k, v in dynamo_obj.items()
    }

def parse_low_level_event(event):
    print(type(event), " --> ", event)
    raw_records = []
    if event["eventName"] in ["MODIFY", "INSERT"]:
        raw_records = dynamo_obj_to_python_obj(event["dynamodb"]["NewImage"])
		
		
    return raw_records

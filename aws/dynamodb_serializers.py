from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    deserializer = TypeDeserializer()
    return {
        k: deserializer.deserialize(v) 
        for k, v in dynamo_obj.items()
    }  


def python_obj_to_dynamo_obj(python_obj: dict) -> dict:
    serializer = TypeSerializer()
    return {
        k: serializer.serialize(v)
        for k, v in python_obj.items()
    }


def main():
    p = {
        'a': 1,
        'b': 'b',
        'c': {
            'd': False
        },
        'e': [10, 20, 30]
    }
    print('Python object: ')
    print(p)
    print('Converted to DynamoDB object: ')
    print(python_obj_to_dynamo_obj(p))

    d = {
        'a': {'N': '1'}, 
        'b': {'S': 'b'}, 
        'c': {
            'M': {
                'd': {'BOOL': False}
            }
        }, 
        'e': {
            'L': [
                {'N': '10'}, 
                {'N': '20'}, 
                {'N': '30'}
            ]
        }
    }
    print('DynamoDB object: ')
    print(d)
    print('Converted to Python object: ')
    print(dynamo_obj_to_python_obj(d))


if __name__ == '__main__':
    main()

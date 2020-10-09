import json
import os

def handler(event, context):
    print(os.path.exists('/tmp/parameter-store'))
    with open('/tmp/parameter-store/secret.json', mode='r') as f:
        print(f.read())

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

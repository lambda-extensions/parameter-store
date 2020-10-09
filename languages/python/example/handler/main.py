import json

def load_secrets():
    data = None
    with open('/tmp/parameter-store/secret.json', mode='r') as f:
        data = json.loads(f.read())
    return data

def handler(event, context):
    secrets = load_secrets()
    print(secrets)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

#!/usr/bin/env python3

import json
import os
import boto3

from lef import Extension, EventType

client = None

def handler(event):
    global client
    if client is None:
        client = boto3.client('ssm')

    parameter_keys = [
        'test.extension'
    ]

    print(f'fetching parameters')

    parameters = {}
    for key in parameter_keys:
        parameters[key] = client.get_parameter(Name='test.extension')['Parameter'].get('Value')
    
    if not os.path.exists('/tmp/parameter-store'):
        print('created directory')
        os.mkdir('/tmp/parameter-store')

    with open('/tmp/parameter-store/secret.json', mode='w') as f:
        print(f'writing credential file')
        f.write(json.dumps(parameters))

def main():
    extension = Extension()
    extension.register([EventType.INVOKE], handler)

if __name__ == "__main__":
    main()

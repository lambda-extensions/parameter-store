#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import os
import boto3
import requests
import signal
import sys
from pathlib import Path


# global variables
# extension name has to match the file's parent directory name)
LAMBDA_EXTENSION_NAME = Path(__file__).parent.name


# custom extension code
def execute_custom_processing(event, client):
    # perform custom per-event processing here
    print(f"[{LAMBDA_EXTENSION_NAME}] Received event: {json.dumps(event)}", flush=True)
    os.environ['TEST_EXTENSION_VALUE'] = client.get_parameter(Name='test.extension')['Parameter']['Value']


# boiler plate code
def handle_signal(signal, frame):
    # if needed pass this signal down to child processes
    print(f"[{LAMBDA_EXTENSION_NAME}] Received signal={signal}. Exiting.", flush=True)
    sys.exit(0)


def register_extension():
    print(f"[{LAMBDA_EXTENSION_NAME}] Registering...", flush=True)
    headers = {
        'Lambda-Extension-Name': LAMBDA_EXTENSION_NAME,
    }
    payload = {
        'events': [
            'INVOKE',
            'SHUTDOWN'
        ],
    }
    response = requests.post(
        url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/register",
        json=payload,
        headers=headers
    )
    ext_id = response.headers['Lambda-Extension-Identifier']
    print(f"[{LAMBDA_EXTENSION_NAME}] Registered with ID: {ext_id}", flush=True)

    return ext_id


def process_events(ext_id, client):
    headers = {
        'Lambda-Extension-Identifier': ext_id
    }

    while True:
        print(f"[{LAMBDA_EXTENSION_NAME}] Waiting for event...", flush=True)

        response = requests.get(
            url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/event/next",
            headers=headers,
            timeout=None
        )
        event = json.loads(response.text)
        if event['eventType'] == 'SHUTDOWN':
            print(f"[{LAMBDA_EXTENSION_NAME}] Received SHUTDOWN event. Exiting.", flush=True)
            sys.exit(0)
        else:
            execute_custom_processing(event, client)

client = None

def main():
    global client
    if client is None:
        client = boto3.client('ssm')

    # handle signals
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # execute extensions logic
    extension_id = register_extension()
    process_events(extension_id, client)


if __name__ == "__main__":
    main()

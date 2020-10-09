#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from enum import Enum

from lef.utils import get, post


class EventType(Enum):
    INVOKE = "INVOKE"
    SHUTDOWN = "SHUTDOWN"


class Extension:
    def __init__(self, name=None, runtime_api_endpoint=None):
        self.handlers = {}
        self.name = name or Path(__file__).parent.name
        self.runtime_api_endpoint = (
            runtime_api_endpoint or os.environ["AWS_LAMBDA_RUNTIME_API"]
        )

    @staticmethod
    def handle_signal(signal, frame):
        sys.exit(0)

    def register(self, events, handler):
        print("called")
        response = post(
            url=f"https://{self.runtime_api_endpoint}/2020-01-01/extension/register",
            data={"events": [str(event) for event in events]},
            headers={
                "Lambda-Extension-Name": self.name,
            },
        )

        extension_id = response.headers["Lambda-Extension-Identifier"]
        return self.process_events(extension_id, handler)

    def process_events(self, extension_id, handler):
        while True:
            print("called")
            response = get(
                url=f"https://{self.runtime_api_endpoint}/2020-01-01/extension/event/next",
                headers={"Lambda-Extension-Identifier": extension_id},
            ).json()

            if response["eventType"] == "SHUTDOWN":
                sys.exit(0)
            else:
                handler(response)

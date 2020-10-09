import json
from urllib import request


class Response:
    def __init__(self, res):
        self.headers = res.headers
        self.text = res.read().decode()

    def json(self):
        return json.loads(self.text)


def get(url, headers=None):
    kwargs = {"url": url, "headers": headers or {}}

    req = request.Request(**kwargs)
    response = request.urlopen(req)
    return Response(response)


def post(url, headers=None, data=None):
    kwargs = {"url": url, "headers": headers or {}}

    if data:
        kwargs["data"] = json.dumps(data)
        kwargs["headers"]["Content-Type"] = "application/json"

    req = request.Request(**kwargs)
    response = request.urlopen(req)
    return Response(response)

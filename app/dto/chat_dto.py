import json


class ChatDTO:
    def __init__(self, name, body):
        self._json_data = json.dumps({"name": name, "body": body})
        self._name = name
        self._body = body

    def __str__(self):
        return f"{self._name} : {self._body}"

    @property
    def name(self):
        return self._name

    @property
    def body(self):
        return self._body

    @property
    def json_data(self):
        return self._json_data

    @staticmethod
    def covertFromByteCode(byte_code):
        json_data = json.loads(byte_code)
        return ChatDTO(json_data["name"], json_data["body"])

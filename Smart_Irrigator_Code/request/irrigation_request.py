import json


class IrrigationRequestDescriptor:

    IRRIGATION_TYPE_LOW = "low_irrigation"
    IRRIGATION_TYPE_MEDIUM = "medium_irrigation"
    IRRIGATION_TYPE_HIGH = "high_irrigation"

    def __init__(self, type):
        self.type = type

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

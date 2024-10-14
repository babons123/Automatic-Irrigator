import random
import json
import time


class HumiditySensorDescriptor:

    def __init__(self):
        self.humidity_value = 0.0
        self.unit = "%"
        self.timestamp = 0
        self.measure_humidity()

    def measure_humidity(self):
        self.humidity_value = random.uniform(0.0, 100.0)
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

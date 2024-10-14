import random
import json
import time


class RainSensorDescriptor:

    def __init__(self):
        self.rain_value = 0.0
        self.unit = "m^3"
        self.timestamp = 0
        self.measure_rain()

    def measure_rain(self):
        self.rain_value = random.uniform(0.0, 100.0)
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

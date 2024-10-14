import random
import json
import time


class TemperatureSensorDescriptor:

    def __init__(self):
        self.temperature_value = 0.0
        self.unit = "°C"
        self.timestamp = 0
        self.measure_temperature()

    def measure_temperature(self):
        self.temperature_value = random.uniform(0.0, 50.0)
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

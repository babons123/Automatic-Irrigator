import random
import json
import time


class BatterySensorDescriptor:

    def __init__(self):
        self.battery_value = 0.0
        self.unit = "%"
        self.timestamp = 0
        self.measure_battery()

    def measure_battery(self):
        self.battery_value = random.uniform(0.0, 100.0)
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

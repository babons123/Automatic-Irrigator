import json


class IrrigationHistoryDescriptor:

    def __init__(self):
        self.totalCount = 0
        self.lowCount = 0
        self.mediumCount = 0
        self.highCount = 0

    def increase_low_watering(self):
        self.totalCount += 1
        self.lowCount += 1

    def increase_medium_watering(self):
        self.totalCount += 1
        self.mediumCount += 1

    def increase_high_watering(self):
        self.totalCount += 1
        self.highCount += 1

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

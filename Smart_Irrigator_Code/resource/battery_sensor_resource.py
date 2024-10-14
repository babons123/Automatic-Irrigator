import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
from model.battery_sensor import BatterySensorDescriptor
from kpn_senml import *


class BatterySensorResource(resource.Resource):

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.battery_sensor = BatterySensorDescriptor()
        self.if_ = "core.s"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.sensor.battery"
        self.title = "Battery Sensor"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        temp = SenmlRecord("battery-sensor",
                           unit=SenmlUnits.SENML_UNIT_PERCENTAGE_REMAINING_BATTERY_LEVEL,
                           value=self.battery_sensor.battery_value,
                           time=int(time.time()))
        pack.add(temp)
        return pack.to_json()

    async def render_get(self, request):
        print("BatterySensorResource -> GET Request Received ...")
        print("BatterySensorResource -> Reading updated battery value ...")
        self.battery_sensor.measure_battery()
        print("BatterySensorResource -> Updated Battery Value: %f" % self.battery_sensor.battery_value)

        payload_string = self.build_senml_json_payload()

        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'],
                               payload=payload_string.encode('utf8'))

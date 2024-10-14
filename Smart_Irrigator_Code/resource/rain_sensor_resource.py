import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
from model.rain_sensor import RainSensorDescriptor
from kpn_senml import *


class RainSensorResource(resource.Resource):

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.rain_sensor = RainSensorDescriptor()
        self.if_ = "core.s"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.sensor.rain"
        self.title = "Rain Sensor"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        temp = SenmlRecord("rain-sensor",
                           unit=SenmlUnits.SENML_UNIT_CUBIC_METER,
                           value=self.rain_sensor.rain_value,
                           time=int(time.time()))
        pack.add(temp)
        return pack.to_json()

    async def render_get(self, request):
        print("RainSensorResource -> GET Request Received ...")
        print("RainSensorResource -> Reading updated rain value ...")
        self.rain_sensor.measure_rain()
        print("RainSensorResource -> Updated Rain Value: %f" % self.rain_sensor.rain_value)

        payload_string = self.build_senml_json_payload()

        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'],
                               payload=payload_string.encode('utf8'))
